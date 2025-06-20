import os
import threading
import time
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum


class PipelineStatus(Enum):
    IDLE = "idle"
    RUNNING = "running" 
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ERROR = "error"


@dataclass
class PipelineConfig:
    """Configuration for the pipeline processing"""
    io_workers: Optional[int] = None
    compute_workers: Optional[int] = None
    batch_size: int = 1000
    poll_interval: float = 0.1
    shutdown_timeout: float = 5.0
    
    def __post_init__(self):
        cpu_count = os.cpu_count() or 1
        if self.io_workers is None:
            self.io_workers = cpu_count * 2
        if self.compute_workers is None:
            self.compute_workers = cpu_count


class MultiStagePipeline:
    """Generic multi-stage processing pipeline with I/O and compute stages"""
    
    def __init__(self, config: PipelineConfig = None):
        self.config = config or PipelineConfig()
        
        # Thread pools
        self.io_pool: Optional[ThreadPoolExecutor] = None
        self.compute_pool: Optional[ThreadPoolExecutor] = None
        
        # Queues for pipeline stages
        self.io_result_queue: Optional[Queue] = None
        self.compute_result_queue: Optional[Queue] = None
        
        # Control and state
        self.stop_event: Optional[threading.Event] = None
        self.pipeline_coordinator_thread: Optional[threading.Thread] = None
        
        # Statistics and progress
        self.total_items = 0
        self.items_processed = 0
        self.status = PipelineStatus.IDLE
        self.error_message = ""
        
        # Callbacks
        self.io_processor: Optional[Callable] = None
        self.compute_processor: Optional[Callable] = None
        self.result_handler: Optional[Callable] = None
        self.progress_callback: Optional[Callable] = None
        self.completion_callback: Optional[Callable] = None
        
    def set_processors(self, 
                      io_processor: Callable,
                      compute_processor: Callable = None,
                      result_handler: Callable = None):
        """Set the processing functions for each stage"""
        self.io_processor = io_processor
        self.compute_processor = compute_processor or self._default_compute_processor
        self.result_handler = result_handler
        
    def set_callbacks(self,
                     progress_callback: Callable = None,
                     completion_callback: Callable = None):
        """Set optional callbacks for progress and completion"""
        self.progress_callback = progress_callback
        self.completion_callback = completion_callback
    
    def start(self, items: List[Any]) -> bool:
        """Start processing the given items"""
        if self.status == PipelineStatus.RUNNING:
            return False
            
        if not self.io_processor:
            raise ValueError("I/O processor must be set before starting")
            
        # Initialize
        self.total_items = len(items)
        self.items_processed = 0
        self.status = PipelineStatus.RUNNING
        self.error_message = ""
        
        # Initialize queues and synchronization
        self.io_result_queue = Queue()
        self.compute_result_queue = Queue()
        self.stop_event = threading.Event()
        
        # Calculate worker counts based on workload
        io_workers = min(len(items), self.config.io_workers)
        compute_workers = self.config.compute_workers
        
        # Initialize thread pools
        self.io_pool = ThreadPoolExecutor(
            max_workers=io_workers,
            thread_name_prefix="Pipeline_IO"
        )
        self.compute_pool = ThreadPoolExecutor(
            max_workers=compute_workers,
            thread_name_prefix="Pipeline_Compute"
        )
        
        # Start pipeline coordinator
        self.pipeline_coordinator_thread = threading.Thread(
            target=self._pipeline_coordinator,
            name="Pipeline_Coordinator"
        )
        self.pipeline_coordinator_thread.start()
        
        # Submit all I/O work
        for item in items:
            self.io_pool.submit(self._safe_io_processor, item)
            
        return True
    
    def poll(self) -> PipelineStatus:
        """Poll for progress and process results. Call this regularly."""
        if self.status != PipelineStatus.RUNNING:
            return self.status
            
        if not self.compute_result_queue:
            return self.status
            
        # Process completed results
        results_processed = 0
        while (not self.compute_result_queue.empty() and 
               results_processed < self.config.batch_size):
            try:
                result_data = self.compute_result_queue.get_nowait()
                
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
        
        # Check for completion
        if (self.items_processed >= self.total_items and
            self.compute_result_queue.empty() and
            self.io_result_queue.empty()):
            
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
    
    def _safe_io_processor(self, item):
        """Safe wrapper for I/O processing"""
        if self.stop_event and self.stop_event.is_set():
            return
            
        try:
            result = self.io_processor(item)
            if result is not None:
                self.io_result_queue.put(result)
        except Exception as e:
            print(f"I/O processing error: {e}")
            self.error_message = str(e)
    
    def _pipeline_coordinator(self):
        """Coordinates between I/O and compute stages"""
        while not (self.stop_event and self.stop_event.is_set()):
            try:
                # Get I/O result
                io_data = self.io_result_queue.get(timeout=self.config.poll_interval)
                
                if io_data is not None:
                    # Submit to compute pool
                    self.compute_pool.submit(self._safe_compute_processor, io_data)
                    
            except Empty:
                # Check if we should continue waiting
                if self._are_io_threads_alive():
                    continue
                elif self._are_compute_threads_alive():
                    continue
                else:
                    break  # All work complete
    
    def _safe_compute_processor(self, io_data):
        """Safe wrapper for compute processing"""
        if self.stop_event and self.stop_event.is_set():
            return
            
        try:
            result = self.compute_processor(io_data)
            if result is not None:
                self.compute_result_queue.put(result)
        except Exception as e:
            print(f"Compute processing error: {e}")
            self.error_message = str(e)
    
    def _default_compute_processor(self, data):
        """Default pass-through compute processor"""
        return data
    
    def _are_io_threads_alive(self) -> bool:
        """Check if any I/O threads are still running"""
        if not self.io_pool or not hasattr(self.io_pool, '_threads'):
            return False
        return any(t.is_alive() for t in self.io_pool._threads)
    
    def _are_compute_threads_alive(self) -> bool:
        """Check if any compute threads are still running"""
        if not self.compute_pool or not hasattr(self.compute_pool, '_threads'):
            return False
        return any(t.is_alive() for t in self.compute_pool._threads)
    
    def _complete(self, status: PipelineStatus):
        """Complete the pipeline processing"""
        self.status = status
        self._cleanup()
        
        if self.completion_callback:
            self.completion_callback(status, self.items_processed, self.error_message)
    
    def _cleanup(self):
        """Resource cleanup"""
        # Signal all threads to stop
        if self.stop_event:
            self.stop_event.set()
        
        # Shutdown thread pools
        if self.io_pool:
            self.io_pool.shutdown(wait=True)
            
        if self.compute_pool:
            self.compute_pool.shutdown(wait=True)
        
        # Wait for pipeline coordinator
        if (self.pipeline_coordinator_thread and 
            self.pipeline_coordinator_thread.is_alive()):
            self.pipeline_coordinator_thread.join(timeout=self.config.shutdown_timeout)



