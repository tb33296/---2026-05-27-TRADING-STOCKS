# core/execution/paper_execution_engine.py

from datetime import datetime

from core.execution.execution_result import (
    ExecutionResult
)

from core.logging_manager import (
    LoggingManager
)

from core.positions.position import (
    Position
)

from core.positions.position_manager import (
    PositionManager
)

from config.config import (
    SIMULATED_SLIPPAGE_PERCENT
)


class PaperExecutionEngine:
    """
    Simulated order execution engine.
    """

    def __init__(
        self,
        position_manager: PositionManager
    ) -> None:

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.position_manager = (
            position_manager
        )

    def execute_buy(
        self,
        symbol: str,
        segment: str,
        quantity: int,
        ltp: float,
        stop_loss: float,
        target: float
    ) -> ExecutionResult:
        """
        Execute simulated BUY.
        """

        try:

            fill_price = (
                ltp
                *
                (
                    1
                    +
                    SIMULATED_SLIPPAGE_PERCENT
                )
            )

            fill_price = round(
                fill_price,
                2
            )

            position = Position(
                symbol=symbol,
                segment=segment,
                side="LONG",
                quantity=quantity,
                entry_price=fill_price,
                entry_time=datetime.now(),
                stop_loss=stop_loss,
                target=target
            )

            success = (
                self.position_manager
                .open_position(
                    position
                )
            )

            if not success:

                return ExecutionResult(
                    success=False,
                    symbol=symbol,
                    side="BUY",
                    quantity=quantity,
                    fill_price=fill_price,
                    timestamp=datetime.now(),
                    message=(
                        "POSITION_OPEN_FAILED"
                    )
                )

            return ExecutionResult(
                success=True,
                symbol=symbol,
                side="BUY",
                quantity=quantity,
                fill_price=fill_price,
                timestamp=datetime.now(),
                message="FILLED",
                position_opened=True
            )

        except Exception as error:

            self.logger.error(
                f"BUY execution failed: "
                f"{error}"
            )

            return ExecutionResult(
                success=False,
                symbol=symbol,
                side="BUY",
                quantity=quantity,
                fill_price=0.0,
                timestamp=datetime.now(),
                message=str(error)
            )

    def execute_sell(
        self,
        symbol: str,
        exit_price: float
    ) -> bool:
        """
        Close existing position.
        """

        return (
            self.position_manager
            .close_position(
                symbol=symbol,
                exit_price=exit_price
                
            )
        )