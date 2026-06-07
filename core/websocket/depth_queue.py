# core/websocket/depth_queue.py

from collections import deque
from threading import Lock
from typing import Any, Optional


class DepthQueue:
    """
    Thread-safe bounded depth queue.

    Designed for:
    - low memory usage
    - high throughput
    - fixed-size buffering
    - websocket depth ingestion
    """

    def __init__(
        self,
        max_size: int
    ) -> None:

        self.queue = deque(maxlen=max_size)

        self.lock = Lock()

        self.dropped_depth_packets = 0

    def enqueue(
        self,
        depth_packet: dict[str, Any]
    ) -> bool:
        """
        Add depth packet to queue.

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

                    self.dropped_depth_packets += 1

                    return False

                self.queue.append(
                    depth_packet
                )

                return True

        except Exception:

            return False

    def dequeue(
        self
    ) -> Optional[dict[str, Any]]:
        """
        Remove oldest depth packet.

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

    def get_dropped_packet_count(
        self
    ) -> int:
        """
        Return dropped depth packet count.
        """

        return self.dropped_depth_packets

    def get_utilization_percent(
        self
    ) -> float:
        """
        Return queue utilization percentage.
        """

        with self.lock:

            current_size = len(
                self.queue
            )

            max_size = (
                self.queue.maxlen or 1
            )

            utilization = (
                current_size / max_size
            ) * 100

            return round(
                utilization,
                2
            )