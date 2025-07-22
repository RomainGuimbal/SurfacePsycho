import os
import multiprocessing as mp
import time
from queue import Queue, Empty
from typing import Callable, Any, Optional, List, Tuple, Dict
from dataclasses import dataclass
from enum import Enum
import pickle
import traceback


class PipelineStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ERROR = "error"


@dataclass
class PipelineConfig:
    """Configuration for the pipeline processing"""

    compute_workers: Optional[int] = None
    batch_size: int = 1000
    poll_interval: float = 0.1
    shutdown_timeout: float = 5.0

    def __post_init__(self):
        cpu_count = os.cpu_count() or 1
        if self.compute_workers is None:
            self.compute_workers = cpu_count


class ProcessorRegistry:
    """Registry for processor functions that can be safely pickled"""

    _processors: Dict[str, Callable] = {}

    @classmethod
    def register(cls, name: str, func: Callable):
        """Register a processor function"""
        cls._processors[name] = func

    @classmethod
    def get(cls, name: str) -> Callable:
        """Get a registered processor function"""
        return cls._processors.get(name)


def _worker_compute_processor(
    compute_queue, result_queue, stop_event, processor_name, processor_args=None
):
    """Worker process function for compute processing"""
    # Get the processor function from registry
    compute_func = ProcessorRegistry.get(processor_name)
    if not compute_func:
        result_queue.put(("error", f"Processor {processor_name} not found in registry"))
        return

    while not stop_event.is_set():
        try:
            # Get work item with timeout
            work_item = compute_queue.get(timeout=0.1)
            if work_item is None:  # Poison pill
                break

            try:
                if processor_args:
                    result = compute_func(work_item, **processor_args)
                else:
                    result = compute_func(work_item)

                if result is not None:
                    result_queue.put(result)
            except Exception as e:
                error_msg = f"Compute error: {str(e)}\n{traceback.format_exc()}"
                result_queue.put(("error", error_msg))

        except Empty:
            continue
        except Exception as e:
            error_msg = f"Worker error: {str(e)}\n{traceback.format_exc()}"
            result_queue.put(("error", error_msg))


class MultiStagePipeline:
    """Generic multi-stage processing pipeline with single-threaded I/O and multiprocess compute"""

    def __init__(self, config: PipelineConfig = None):
        self.config = config or PipelineConfig()

        # Multiprocessing components
        self.compute_processes: List[mp.Process] = []
        self.compute_queue: Optional[mp.Queue] = None
        self.result_queue: Optional[mp.Queue] = None
        self.stop_event: Optional[mp.Event] = None

        # Statistics and progress
        self.total_items = 0
        self.items_processed = 0
        self.status = PipelineStatus.IDLE
        self.error_message = ""

        # Callbacks and processors
        self.io_processor: Optional[Callable] = None
        self.compute_processor_name: Optional[str] = None
        self.compute_processor_args: Optional[Dict] = None
        self.result_handler: Optional[Callable] = None
        self.progress_callback: Optional[Callable] = None
        self.completion_callback: Optional[Callable] = None

        # I/O processing state
        self.io_items: List[Any] = []
        self.io_index = 0
        self.io_completed = False

    def set_processors(
        self,
        io_processor: Callable,
        compute_processor_name: str = None,
        compute_processor_args: Dict = None,
        result_handler: Callable = None,
    ):
        """Set the processing functions for each stage

        Args:
            io_processor: Function for I/O processing (runs in main process)
            compute_processor_name: Name of registered compute processor function
            compute_processor_args: Optional arguments to pass to compute processor
            result_handler: Function to handle final results
        """
        self.io_processor = io_processor
        self.compute_processor_name = compute_processor_name
        self.compute_processor_args = compute_processor_args or {}
        self.result_handler = result_handler

    def set_callbacks(
        self, progress_callback: Callable = None, completion_callback: Callable = None
    ):
        """Set optional callbacks for progress and completion"""
        self.progress_callback = progress_callback
        self.completion_callback = completion_callback

    def start(self, items: List[Any]) -> bool:
        """Start processing the given items"""
        if self.status == PipelineStatus.RUNNING:
            return False

        if not self.io_processor:
            raise ValueError("I/O processor must be set before starting")

        if not self.compute_processor_name:
            raise ValueError("Compute processor name must be set before starting")

        if not ProcessorRegistry.get(self.compute_processor_name):
            raise ValueError(
                f"Compute processor '{self.compute_processor_name}' not found in registry"
            )

        # Initialize
        self.io_items = items.copy()
        self.io_index = 0
        self.io_completed = False
        self.total_items = len(items)
        self.items_processed = 0
        self.status = PipelineStatus.RUNNING
        self.error_message = ""

        # Initialize multiprocessing components
        self.compute_queue = mp.Queue()
        self.result_queue = mp.Queue()
        self.stop_event = mp.Event()

        # Start compute worker processes
        self.compute_processes = []
        for i in range(self.config.compute_workers):
            process = mp.Process(
                target=_worker_compute_processor,
                args=(
                    self.compute_queue,
                    self.result_queue,
                    self.stop_event,
                    self.compute_processor_name,
                    self.compute_processor_args,
                ),
                name=f"Pipeline_Compute_{i}",
            )
            process.start()
            self.compute_processes.append(process)

        return True

    def poll(self) -> PipelineStatus:
        """Poll for progress and process results. Call this regularly."""
        if self.status != PipelineStatus.RUNNING:
            return self.status

        # Process I/O items (single-threaded)
        self._process_io_batch()

        # Process completed results
        self._process_results()

        # Check for completion
        if self._is_processing_complete():
            self._complete(PipelineStatus.COMPLETED)

        return self.status

    def cancel(self):
        """Cancel the processing"""
        if self.status == PipelineStatus.RUNNING:
            if self.stop_event:
                self.stop_event.set()
            self._complete(PipelineStatus.CANCELLED)

    def wait_for_completion(self, timeout: float = None) -> PipelineStatus:
        """Block until processing completes or times out"""
        start_time = time.time()

        while self.status == PipelineStatus.RUNNING:
            self.poll()

            if timeout and (time.time() - start_time) > timeout:
                self.cancel()
                break

            time.sleep(self.config.poll_interval)

        return self.status

    def get_progress(self) -> Tuple[int, int, float]:
        """Get current progress: (processed, total, percentage)"""
        if self.total_items == 0:
            return 0, 0, 0.0
        percentage = (self.items_processed / self.total_items) * 100
        return self.items_processed, self.total_items, percentage

    def _process_io_batch(self):
        """Process a batch of I/O items (single-threaded)"""
        if self.io_completed or self.stop_event.is_set():
            return

        batch_count = 0
        while (
            self.io_index < len(self.io_items) and batch_count < self.config.batch_size
        ):

            if self.stop_event.is_set():
                break

            item = self.io_items[self.io_index]
            self.io_index += 1
            batch_count += 1

            try:
                # Process I/O
                io_result = self.io_processor(item)
                if io_result is not None:
                    # Send to compute queue
                    self.compute_queue.put(io_result)

            except Exception as e:
                error_msg = f"I/O processing error: {str(e)}\n{traceback.format_exc()}"
                print(error_msg)
                self.error_message = str(e)
                self._complete(PipelineStatus.ERROR)
                return

        # Check if I/O processing is complete
        if self.io_index >= len(self.io_items):
            self.io_completed = True
            # Send poison pills to terminate worker processes
            for _ in self.compute_processes:
                self.compute_queue.put(None)

    def _process_results(self):
        """Process completed results from compute workers"""
        if not self.result_queue:
            return

        results_processed = 0
        while results_processed < self.config.batch_size:
            try:
                result_data = self.result_queue.get_nowait()

                # Check for error results
                if isinstance(result_data, tuple) and result_data[0] == "error":
                    print(f"Compute processing error: {result_data[1]}")
                    self.error_message = result_data[1]
                    self._complete(PipelineStatus.ERROR)
                    return

                # Handle result
                if self.result_handler:
                    self.result_handler(result_data)

                self.items_processed += 1
                results_processed += 1

                # Progress callback
                if self.progress_callback:
                    self.progress_callback(self.items_processed, self.total_items)

            except Empty:
                break

    def _is_processing_complete(self) -> bool:
        """Check if all processing is complete"""
        # All items processed and no more work in queues
        if not self.io_completed:
            return False

        if self.items_processed < self.total_items:
            return False

        # Check if compute processes are still alive
        alive_processes = [p for p in self.compute_processes if p.is_alive()]
        if alive_processes:
            return False

        # Check if there are still items in queues
        try:
            self.result_queue.get_nowait()
            return False  # Still has results to process
        except Empty:
            pass

        return True

    def _complete(self, status: PipelineStatus):
        """Complete the pipeline processing"""
        self.status = status
        self._cleanup()

        if self.completion_callback:
            self.completion_callback(status, self.items_processed, self.error_message)

    def _cleanup(self):
        """Resource cleanup"""
        # Signal all processes to stop
        if self.stop_event:
            self.stop_event.set()

        # Send poison pills to ensure processes terminate
        if self.compute_queue and not self.io_completed:
            for _ in self.compute_processes:
                try:
                    self.compute_queue.put(None)
                except:
                    pass

        # Wait for all compute processes to finish
        for process in self.compute_processes:
            if process.is_alive():
                process.join(timeout=self.config.shutdown_timeout)
                if process.is_alive():
                    process.terminate()
                    process.join(timeout=1.0)

        # Clean up queues
        if self.compute_queue:
            try:
                while not self.compute_queue.empty():
                    self.compute_queue.get_nowait()
            except:
                pass

        if self.result_queue:
            try:
                while not self.result_queue.empty():
                    self.result_queue.get_nowait()
            except:
                pass

        self.compute_processes.clear()


# Utility functions for common processors
def simple_compute_processor(data):
    """Default pass-through compute processor"""
    return data


def heavy_compute_processor(data, multiplier=1):
    """Example CPU-intensive processor with configurable work"""
    import math

    # Simulate heavy computation
    result = 0
    for i in range(multiplier * 10000):
        result += math.sqrt(i + 1)
    return f"processed_{data}_result_{result:.2f}"


# Register default processors
ProcessorRegistry.register("simple", simple_compute_processor)
ProcessorRegistry.register("heavy", heavy_compute_processor)


# Example usage
if __name__ == "__main__":

    def io_processor(item):
        """Example I/O processor - simulate file reading"""
        time.sleep(0.01)  # Simulate I/O delay
        return f"loaded_{item}"

    def result_handler(result):
        """Example result handler"""
        print(f"Result: {result}")

    def progress_callback(processed, total):
        """Example progress callback"""
        percentage = (processed / total) * 100
        print(f"Progress: {processed}/{total} ({percentage:.1f}%)")

    # Create and configure pipeline
    config = PipelineConfig(compute_workers=4, batch_size=10)
    pipeline = MultiStagePipeline(config)

    pipeline.set_processors(
        io_processor=io_processor,
        compute_processor_name="heavy",
        compute_processor_args={"multiplier": 2},
        result_handler=result_handler,
    )

    pipeline.set_callbacks(progress_callback=progress_callback)

    # Process items
    items = list(range(20))
    pipeline.start(items)

    # Wait for completion
    final_status = pipeline.wait_for_completion(timeout=30)
    print(f"Pipeline completed with status: {final_status}")

    processed, total, percentage = pipeline.get_progress()
    print(f"Final progress: {processed}/{total} ({percentage:.1f}%)")
