from collections import deque
from threading import Lock
from core.logging_manager import LoggingManager

class TradeMonitor:

    def __init__(self, max_events: int = 100):

        self.lock = Lock()

        self.events = deque(maxlen=max_events)
        
        self.logger = LoggingManager.get_logger("trade_monitor")

    def add(self, category: str, message: str):

        with self.lock:

            self.events.appendleft(
                {
                    "category": category,
                    "message": message,
                }
            )
            self.logger.info(
            f"[{category}] {message}"
        )

    def get_events(self):

        with self.lock:

            return list(self.events)


trade_monitor = TradeMonitor()