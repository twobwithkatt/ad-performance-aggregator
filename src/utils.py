import time
import os
import resource
from typing import Tuple

def get_peak_memory_mb() -> float:
    """Returns peak memory usage (Resident Set Size) in Megabytes."""
    # On Linux, ru_maxrss is in Kilobytes
    try:
        usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return usage / 1024.0
    except Exception:
        return 0.0

class Timer:
    """Context manager / helper for measuring elapsed wall-clock execution time."""
    def __init__(self):
        self.start_time: float = 0.0
        self.elapsed: float = 0.0

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start_time
