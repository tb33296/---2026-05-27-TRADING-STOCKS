# core/trade_management/trade_manager.py

from core.logging_manager import LoggingManager

from core.trade_management.exit_decision import ExitDecision

from runtime.trade_pipeline import TradePipeline

from core.positions.position_manager import PositionManager

from core.trade_management.exit_rules import ExitRules

from core.trade_management.trailing_stop_manager import TrailingStopManager


class TradeManager:
    """
    Manages open trade exits.

    Responsibilities:

    - stop loss exits
    - target exits

    Future:

    - trailing stop
    - time exit
    - EOD exit
    """

    def __init__(
        self, position_manager: PositionManager, trade_pipeline: TradePipeline
    ) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.position_manager = position_manager

        self.trade_pipeline = trade_pipeline

        self.trailing_stop_manager = TrailingStopManager()

    def evaluate_position(self, symbol: str, current_price: float) -> ExitDecision:
        """
        Evaluate exit conditions.
        """

        position = self.position_manager.get_open_positions().get(symbol)

        if position is None:
            return ExitDecision(should_exit=False, reason="POSITION_NOT_FOUND")

        # ----------------------------------
        # TRAILING STOP UPDATE
        # ----------------------------------

        self.trailing_stop_manager.update(
            position=position,
            current_price=current_price,
        )

        # ----------------------------------
        # STOP LOSS
        # ----------------------------------

        decision = ExitRules.stop_loss_hit(
            side=position.side,
            current_price=current_price,
            stop_loss=position.stop_loss,
        )

        if decision.should_exit:
            return decision

        # ----------------------------------
        # TARGET
        # ----------------------------------

        decision = ExitRules.target_hit(
            side=position.side, current_price=current_price, target=position.target
        )

        if decision.should_exit:
            return decision

        # ----------------------------------
        # FORCE EXIT
        # ----------------------------------

        decision = ExitRules.force_exit_time_hit()  # .force_exit_required()

        if decision.should_exit:
            return decision

        return ExitDecision(should_exit=False, reason="HOLD")

    def process_position(self, symbol: str, current_price: float) -> bool:
        """
        Process a single position.
        """

        try:
            decision = self.evaluate_position(
                symbol=symbol, current_price=current_price
            )

            if not decision.should_exit:
                return False

            self.logger.info(f"Exit Triggered: {symbol} ({decision.reason})")

            return self.trade_pipeline.close_trade(
                symbol=symbol, exit_price=current_price, exit_reason=decision.reason
            )

        except Exception as error:
            self.logger.error(f"Position processing failed: {error}")

            return False

    def process_all_positions(self, price_map: dict[str, float]) -> int:
        """
        Process all open positions.

        Returns:
            Number of positions closed.
        """

        closed_count = 0
        self.logger.info(
            f"[OPEN_POSITIONS] {len(self.position_manager.get_open_positions())}"
        )
        try:
            symbols = list(self.position_manager.get_open_positions().keys())

            for symbol in symbols:
                current_price = price_map.get(symbol)

                if current_price is None:
                    continue

                closed = self.process_position(
                    symbol=symbol, current_price=current_price
                )

                if closed:
                    closed_count += 1

            return closed_count

        except Exception as error:
            self.logger.error(f"Process all positions failed: {error}")

            return closed_count
