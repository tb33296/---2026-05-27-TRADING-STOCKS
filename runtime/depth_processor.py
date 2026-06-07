# runtime/depth_processor.py
from threading import Lock
from typing import Any, Optional

from core.logging_manager import LoggingManager

from core.websocket.depth_queue import DepthQueue

from runtime.orderflow_runtime import OrderFlowRuntime


class DepthProcessor:
    """
    Consumes depth packets from DepthQueue and maintains
    latest market depth state.

    Responsibilities:
    - consume depth queue
    - store latest depth per symbol
    - update orderflow indicators
    - track processing statistics

    Does NOT:
    - build candles
    - calculate candle indicators
    - generate signals
    """

    def __init__(
        self,
        depth_queue: DepthQueue,
        orderflow_runtime: OrderFlowRuntime,
    ) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.depth_queue = depth_queue

        self.orderflow_runtime = orderflow_runtime

        self.lock = Lock()

        self.latest_depth: dict[str, dict[str, Any]] = {}

        self.total_processed = 0

        self.invalid_packets = 0

    def process_next_depth(self) -> bool:
        """
        Process a single depth packet.

        Returns:
            True if processed.
        """

        depth_packet = self.depth_queue.dequeue()

        if depth_packet is None:
            return False

        try:
            symbol = str(depth_packet.get("symbol", ""))

            if not symbol:
                self.invalid_packets += 1

                return False

            with self.lock:
                self.latest_depth[symbol] = depth_packet

                self.total_processed += 1

            self.orderflow_runtime.process_depth(depth_packet)

            return True

        except Exception as error:
            self.logger.error(f"Depth processing failed: {error}")

            self.invalid_packets += 1

            return False

    def process_all_available(self) -> int:
        """
        Process all queued depth packets.

        Returns:
            Number processed.
        """

        processed = 0

        while self.process_next_depth():
            processed += 1

        return processed

    def get_latest_depth(
        self,
        symbol: str,
    ) -> Optional[dict[str, Any]]:
        """
        Return latest depth snapshot.
        """

        with self.lock:
            return self.latest_depth.get(symbol)

    def get_all_latest_depth(
        self,
    ) -> dict[str, dict[str, Any]]:
        """
        Return snapshot of all depth.
        """

        with self.lock:
            return dict(self.latest_depth)

    def get_total_processed(
        self,
    ) -> int:

        return self.total_processed

    def get_invalid_packet_count(
        self,
    ) -> int:

        return self.invalid_packets

    def get_tracked_symbol_count(
        self,
    ) -> int:

        with self.lock:
            return len(self.latest_depth)

    def clear(self) -> None:
        """
        Reset processor state.
        """

        with self.lock:
            self.latest_depth.clear()

            self.total_processed = 0

            self.invalid_packets = 0
