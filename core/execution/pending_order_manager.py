# core/execution/pending_order_manager.py

from threading import Lock

from core.logging_manager import LoggingManager

from core.execution.pending_order import PendingOrder


class PendingOrderManager:
    """
    Manages pending orders waiting for
    simulated execution latency.

    Responsibilities:
    - store pending orders
    - decrement tick counters
    - identify orders ready for execution
    - remove completed orders

    Does NOT:
    - execute orders
    - open positions
    - close positions
    """

    def __init__(self) -> None:

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.lock = Lock()

        self.pending_orders: dict[
            str,
            PendingOrder
        ] = {}

    def create_order(
        self,
        order: PendingOrder
    ) -> bool:
        """
        Register pending order.

        One pending order per symbol.
        """

        try:

            with self.lock:

                if (
                    order.symbol
                    in self.pending_orders
                ):

                    self.logger.warning(
                        f"Pending order already exists "
                        f"for {order.symbol}"
                    )

                    return False

                self.pending_orders[
                    order.symbol
                ] = order

            self.logger.info(
                f"[PENDING_ORDER_CREATED] "
                f"{order.symbol} "
                f"ticks={order.remaining_ticks}"
            )

            return True

        except Exception as error:

            self.logger.error(
                f"Failed to create pending order: "
                f"{error}"
            )

            return False

    def process_tick(
        self,
        symbol: str
    ) -> list[PendingOrder]:
        """
        Process a market tick.

        Decrements countdown for
        matching symbol.

        Returns:
            List of orders ready
            for execution.
        """

        ready_orders: list[
            PendingOrder
        ] = []

        try:

            with self.lock:

                order = (
                    self.pending_orders.get(
                        symbol
                    )
                )

                if order is None:
                    return ready_orders

                order.remaining_ticks -= 1

                self.logger.info(
                    f"[PENDING_ORDER_COUNTDOWN] "
                    f"{symbol} "
                    f"remaining="
                    f"{order.remaining_ticks}"
                )

                if (
                    order.remaining_ticks <= 0
                ):

                    ready_orders.append(
                        order
                    )

                    self.pending_orders.pop(
                        symbol,
                        None
                    )

                    self.logger.info(
                        f"[PENDING_ORDER_READY] "
                        f"{symbol}"
                    )

            return ready_orders

        except Exception as error:

            self.logger.error(
                f"Pending order processing "
                f"failed: {error}"
            )

            return ready_orders

    def cancel_order(
        self,
        symbol: str
    ) -> bool:
        """
        Remove pending order.
        """

        try:

            with self.lock:

                if (
                    symbol
                    not in self.pending_orders
                ):

                    return False

                self.pending_orders.pop(
                    symbol,
                    None
                )

            self.logger.info(
                f"[PENDING_ORDER_CANCELLED] "
                f"{symbol}"
            )

            return True

        except Exception as error:

            self.logger.error(
                f"Cancel order failed: "
                f"{error}"
            )

            return False

    def get_order(
        self,
        symbol: str
    ) -> PendingOrder | None:
        """
        Return pending order.
        """

        with self.lock:

            return self.pending_orders.get(
                symbol
            )

    def get_all_orders(
        self
    ) -> list[PendingOrder]:
        """
        Return all pending orders.
        """

        with self.lock:

            return list(
                self.pending_orders.values()
            )

    def get_pending_count(
        self
    ) -> int:
        """
        Return total pending orders.
        """

        with self.lock:

            return len(
                self.pending_orders
            )

    def clear(
        self
    ) -> None:
        """
        Clear all pending orders.
        """

        with self.lock:

            self.pending_orders.clear()

        self.logger.info(
            "Pending order manager cleared"
        )