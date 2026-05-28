import psutil
from typing import Dict


class SystemMonitor:
    """
    System resource monitoring.
    """

    @staticmethod
    def get_system_stats() -> Dict[str, float]:
        return {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent
        }