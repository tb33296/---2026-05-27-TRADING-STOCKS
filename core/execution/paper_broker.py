# core/execution/paper_broker.py

from datetime import datetime
from threading import Lock

from config.config import DEFAULT_ORDER_QUANTITY, SIMULATED_SLIPPAGE_PERCENT

from core.execution.order import Order

from core.execution.position import Position

from core.execution.tradebook import Tradebook

from core.logging_manager import LoggingManager


class PaperBroker:
    """
    Simulated execution engine.

    Responsibilities:
    - simulated order execution
    - slippage simulation
    - position management
    - trade persistence
    """

    def __init__(self, tradebook: Tradebook) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.tradebook = tradebook

        self.lock = Lock()

        self.open_positions: dict[str, Position] = {}

    def execute_order(self, order: Order) -> bool:
        """
        Execute simulated order.
        """

        try:
            symbol = order.symbol

            with self.lock:
                existing_position = self.open_positions.get(symbol)

                # ============================
                # BUY ORDER
                # ============================

                if order.is_buy():
                    if existing_position is not None:
                        self.logger.warning(f"Position already open for {symbol}")

                        return False

                    return self._open_position(order)

                # ============================
                # SELL ORDER
                # ============================

                if order.is_sell():
                    if existing_position is None:
                        self.logger.warning(f"No open position for {symbol}")

                        return False

                    return self._close_position(order, existing_position)

            return False

        except Exception as error:
            self.logger.error(f"Order execution failed: {error}")

            return False

    def _open_position(self, order: Order) -> bool:
        """
        Create simulated position.
        """

        try:
            fill_price = self._apply_slippage(price=order.price, side="BUY")

            position = Position(
                symbol=order.symbol,
                side=order.side,
                quantity=order.quantity,
                entry_price=fill_price,
                entry_time=datetime.now(),
                current_price=fill_price,
            )

            self.open_positions[order.symbol] = position

            self.logger.info(f"Opened position: {order.symbol} @ {fill_price:.2f}")

            return True

        except Exception as error:
            self.logger.error(f"Open position failed: {error}")

            return False

    def _close_position(self, order: Order, position: Position) -> bool:
        """
        Close simulated position.
        """

        try:
            fill_price = self._apply_slippage(price=order.price, side="SELL")

            position.close(exit_price=fill_price, exit_time=datetime.now())

            persisted = self.tradebook.add_trade(position)

            if not persisted:
                self.logger.error("Trade persistence failed")

                return False

            self.open_positions.pop(order.symbol, None)

            self.logger.info(
                f"Closed position: {order.symbol} PnL={position.realized_pnl:.2f}"
            )

            return True

        except Exception as error:
            self.logger.error(f"Close position failed: {error}")

            return False

    def update_market_price(self, symbol: str, price: float) -> None:
        """
        Update live position price.
        """

        with self.lock:
            position = self.open_positions.get(symbol)

            if position is None:
                return

            position.update_price(price)

    def get_open_position(self, symbol: str) -> Position | None:
        """
        Return open position.
        """

        with self.lock:
            return self.open_positions.get(symbol)

    def has_open_position(self, symbol: str) -> bool:
        """
        Check whether symbol has
        active position.
        """

        with self.lock:
            return symbol in self.open_positions

    def total_open_positions(self) -> int:
        """
        Return total active positions.
        """

        with self.lock:
            return len(self.open_positions)

    def _apply_slippage(self, price: float, side: str) -> float:
        """
        Apply simulated slippage.
        """

        normalized = side.upper().strip()

        if normalized == "BUY":
            return price * (1 + SIMULATED_SLIPPAGE_PERCENT)

        return price * (1 - SIMULATED_SLIPPAGE_PERCENT)

    @staticmethod
    def create_market_order(
        symbol: str, side: str, price: float, strategy_name: str
    ) -> Order:
        """
        Helper to create market order.
        """

        return Order(
            symbol=symbol,
            side=side,
            quantity=DEFAULT_ORDER_QUANTITY,
            price=price,
            order_type="MARKET",
            strategy_name=strategy_name,
            timestamp=datetime.now(),
        )
