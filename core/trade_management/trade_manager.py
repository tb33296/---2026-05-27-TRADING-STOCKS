# core/trade_management/trade_manager.py

from core.execution.paper_execution_engine import (
    PaperExecutionEngine
)

from core.logging_manager import (
    LoggingManager
)

from core.positions.position_manager import (
    PositionManager
)


class TradeManager:
    """
    Handles open trade lifecycle.

    Responsibilities:
    - stop loss monitoring
    - target monitoring
    - exit execution

    Does NOT:
    - generate entries
    - generate signals
    - manage risk
    """

    def __init__(
        self,
        position_manager: PositionManager,
        execution_engine: PaperExecutionEngine
    ) -> None:

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.position_manager = (
            position_manager
        )

        self.execution_engine = (
            execution_engine
        )

    def evaluate_position(
        self,
        symbol: str,
        current_price: float
    ) -> bool:
        """
        Evaluate a single position.

        Returns:
            True if position was closed.
        """

        try:

            position = (
                self.position_manager
                .get_open_positions()
                .get(symbol)
            )

            if position is None:

                return False

            # -------------------------
            # LONG POSITION
            # -------------------------

            if position.side == "LONG":

                # Stop Loss

                if (
                    current_price
                    <= position.stop_loss
                ):

                    self.logger.info(
                        f"SL hit: {symbol}"
                    )

                    return (
                        self.execution_engine
                        .execute_sell(
                            symbol=symbol,
                            exit_price=current_price
                        )
                    )

                # Target

                if (
                    current_price
                    >= position.target
                ):

                    self.logger.info(
                        f"Target hit: {symbol}"
                    )

                    return (
                        self.execution_engine
                        .execute_sell(
                            symbol=symbol,
                            exit_price=current_price
                        )
                    )

            return False

        except Exception as error:

            self.logger.error(
                f"Trade evaluation failed: "
                f"{error}"
            )

            return False

    def evaluate_all_positions(
        self,
        price_map: dict[str, float]
    ) -> int:
        """
        Evaluate all open positions.

        Returns:
            Number of positions closed.
        """

        closed_count = 0

        try:

            open_symbols = list(
                self.position_manager
                .get_open_positions()
                .keys()
            )

            for symbol in open_symbols:

                current_price = (
                    price_map.get(symbol)
                )

                if current_price is None:

                    continue

                closed = (
                    self.evaluate_position(
                        symbol=symbol,
                        current_price=current_price
                    )
                )

                if closed:

                    closed_count += 1

            return closed_count

        except Exception as error:

            self.logger.error(
                f"Trade evaluation failed: "
                f"{error}"
            )

            return closed_count