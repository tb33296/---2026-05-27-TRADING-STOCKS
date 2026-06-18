# core/risk/risk_engine.py

from core.logging_manager import LoggingManager


from core.risk.risk_decision import RiskDecision


from config.config import (
    MAX_CONCURRENT_POSITIONS,
    MAX_DAILY_DRAWDOWN,
    MAX_CONSECUTIVE_LOSSES,
)


class RiskEngine:
    """
    Entry risk validation engine.

    Responsibilities:
    - max positions check
    - daily drawdown check
    - consecutive loss check

    Does NOT:
    - sizing
    - execution
    - stop loss management
    """

    def __init__(self, position_manager) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.position_manager = position_manager

    def evaluate(self, trade_decision) -> RiskDecision:
        """
        Determine whether a trade
        is allowed.
        """

        try:
            open_positions = self.position_manager.get_open_position_count()

            if open_positions >= MAX_CONCURRENT_POSITIONS:
                return RiskDecision(approved=False, reason=("MAX_CONCURRENT_TRADES_OPEN"))

            realized_pnl = self.position_manager.get_total_net_pnl()

            if realized_pnl <= -MAX_DAILY_DRAWDOWN:
                return RiskDecision(approved=False, reason=("MAX_DAILY_DRAWDOWN"))

            consecutive_losses = self.position_manager.get_consecutive_losses()
            self.logger.info(
                f"[RISK_DEBUG] "
                f"open_positions={open_positions} "
                f"realized_pnl={realized_pnl} "
                f"consecutive_losses={consecutive_losses}"
            )
            if consecutive_losses >= MAX_CONSECUTIVE_LOSSES:
                return RiskDecision(approved=False, reason=("MAX_CONSECUTIVE_LOSSES"))

            return RiskDecision(approved=True, reason="APPROVED")

        except Exception as error:
            self.logger.error(f"Risk evaluation failed: {error}")

            return RiskDecision(approved=False, reason="RISK_ENGINE_ERROR")
