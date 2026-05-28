
# core/websocket/tick_queue.py

from collections import deque
from threading import Lock
from typing import Any, Optional


class TickQueue:
    """
    Thread-safe bounded tick queue.

    Designed for:
    - low memory usage
    - high throughput
    - fixed-size buffering
    - websocket ingestion
    """

    def __init__(
        self,
        max_size: int
    ) -> None:

        self.queue = deque(maxlen=max_size)

        self.lock = Lock()

        self.dropped_ticks = 0

    def enqueue(
        self,
        tick: dict[str, Any]
    ) -> bool:
        """
        Add tick to queue.

        Returns:
            bool:
                True if added successfully.
        """

        try:

            with self.lock:

                max_length = self.queue.maxlen 
                if max_length is None: 
                    return False 
                if len(self.queue) >= max_length: 
                    self.dropped_ticks += 1 
                    return False

                self.queue.append(tick)

                return True

        except Exception:

            return False

    def dequeue(
        self
    ) -> Optional[dict[str, Any]]:
        """
        Remove oldest tick from queue.

        Returns:
            dict | None
        """

        try:

            with self.lock:

                if not self.queue:
                    return None

                return self.queue.popleft()

        except Exception:

            return None

    def size(self) -> int:
        """
        Return current queue size.
        """

        with self.lock:

            return len(self.queue)

    def is_empty(self) -> bool:
        """
        Check whether queue is empty.
        """

        with self.lock:

            return len(self.queue) == 0

    def clear(self) -> None:
        """
        Clear queue safely.
        """

        with self.lock:

            self.queue.clear()

    def get_dropped_tick_count(self) -> int:
        """
        Return dropped tick count.
        """

        return self.dropped_ticks

    def get_utilization_percent(self) -> float:
        """
        Return queue utilization percentage.
        """

        with self.lock:

            current_size = len(self.queue)

            max_size = self.queue.maxlen or 1

            utilization = (
                current_size / max_size
            ) * 100

            return round(utilization, 2)
