import multiprocessing as mp
import time
from queue import Empty
import logging
from typing import Any, Callable, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IOCPUPipeline:
    def __init__(self, 
                 io_function: Callable,
                 cpu_function: Callable,
                 io_workers: int = 3,
                 cpu_workers: Optional[int] = None,
                 queue_maxsize: int = 100):
        """
        Pipeline for processing I/O bound tasks followed by CPU bound tasks.
        
        Args:
            io_function: Function that performs I/O operation
            cpu_function: Function that performs CPU operation on I/O result
            io_workers: Number of I/O worker processes
            cpu_workers: Number of CPU worker processes (defaults to CPU count)
            queue_maxsize: Maximum size of internal queues
        """
        self.io_function = io_function
        self.cpu_function = cpu_function
        self.io_workers = io_workers
        self.cpu_workers = cpu_workers or mp.cpu_count()
        self.queue_maxsize = queue_maxsize
        
        # Queues for pipeline stages
        self.task_queue = mp.Queue(maxsize=queue_maxsize)
        self.io_results_queue = mp.Queue(maxsize=queue_maxsize)
        self.final_results_queue = mp.Queue()
        
        # Process pools
        self.io_processes = []
        self.cpu_processes = []
        
    def _io_worker(self):
        """Worker process for I/O operations."""
        while True:
            try:
                task = self.task_queue.get(timeout=1)
                if task is None:  # Sentinel value to stop
                    logger.debug(f"I/O worker {mp.current_process().pid} stopping")
                    break
                    
                logger.debug(f"I/O worker {mp.current_process().pid} processing task")
                try:
                    io_result = self.io_function(task)
                    self.io_results_queue.put((task, io_result))
                except Exception as e:
                    logger.error(f"I/O worker error: {e}")
                    # Put error result to maintain task order tracking if needed
                    self.io_results_queue.put((task, Exception(f"I/O Error: {e}")))
                    
            except Empty:
                continue
            except KeyboardInterrupt:
                break
                
    def _cpu_worker(self):
        """Worker process for CPU operations."""
        while True:
            try:
                item = self.io_results_queue.get(timeout=1)
                if item is None:  # Sentinel value to stop
                    logger.debug(f"CPU worker {mp.current_process().pid} stopping")
                    break
                    
                task, io_result = item
                logger.debug(f"CPU worker {mp.current_process().pid} processing task")
                
                try:
                    # Skip processing if I/O failed
                    if isinstance(io_result, Exception):
                        self.final_results_queue.put((task, io_result))
                        continue
                        
                    cpu_result = self.cpu_function(io_result)
                    self.final_results_queue.put((task, cpu_result))
                except Exception as e:
                    logger.error(f"CPU worker error: {e}")
                    self.final_results_queue.put((task, Exception(f"CPU Error: {e}")))
                    
            except Empty:
                continue
            except KeyboardInterrupt:
                break
    
    def start(self):
        """Start all worker processes."""
        logger.info(f"Starting pipeline with {self.io_workers} I/O workers and {self.cpu_workers} CPU workers")
        
        # Start I/O workers
        for i in range(self.io_workers):
            p = mp.Process(target=self._io_worker)
            p.start()
            self.io_processes.append(p)
            
        # Start CPU workers
        for i in range(self.cpu_workers):
            p = mp.Process(target=self._cpu_worker)
            p.start()
            self.cpu_processes.append(p)
    
    def stop(self):
        """Stop all worker processes gracefully."""
        logger.info("Stopping pipeline...")
        
        # Send stop signals to I/O workers
        for _ in range(self.io_workers):
            self.task_queue.put(None)
            
        # Wait for I/O workers to finish
        for p in self.io_processes:
            p.join(timeout=5)
            if p.is_alive():
                logger.warning(f"Force terminating I/O process {p.pid}")
                p.terminate()
                
        # Send stop signals to CPU workers
        for _ in range(self.cpu_workers):
            self.io_results_queue.put(None)
            
        # Wait for CPU workers to finish
        for p in self.cpu_processes:
            p.join(timeout=5)
            if p.is_alive():
                logger.warning(f"Force terminating CPU process {p.pid}")
                p.terminate()
                
        logger.info("Pipeline stopped")
    
    def process_tasks(self, tasks: List[Any]) -> List[Any]:
        """
        Process a list of tasks through the pipeline.
        
        Args:
            tasks: List of tasks to process
            
        Returns:
            List of results in the same order as input tasks
        """
        if not tasks:
            return []
            
        self.start()
        
        try:
            # Submit all tasks
            for task in tasks:
                self.task_queue.put(task)
            
            # Collect results
            results = {}
            completed = 0
            total_tasks = len(tasks)
            
            logger.info(f"Processing {total_tasks} tasks...")
            
            while completed < total_tasks:
                try:
                    task, result = self.final_results_queue.get(timeout=10)
                    results[id(task)] = result  # Use object id as key
                    completed += 1
                    
                    if completed % 100 == 0 or completed == total_tasks:
                        logger.info(f"Completed {completed}/{total_tasks} tasks")
                        
                except Empty:
                    logger.warning("Timeout waiting for results - some tasks may have failed")
                    break
            
            # Return results in original order
            ordered_results = []
            for task in tasks:
                task_result = results.get(id(task))
                ordered_results.append(task_result)
                
            return ordered_results
            
        finally:
            self.stop()

