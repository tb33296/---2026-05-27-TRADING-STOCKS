# core/trade_management/exit_rules.py

from datetime import datetime

from config.config import FORCE_EXIT_TIME

from core.trade_management.exit_decision import (
    ExitDecision
)


class ExitRules:
    """
    Centralized exit rule engine.

    Responsibilities:

    - stop loss checks
    - target checks
    - force exit checks
    - manual exit checks
    """

    @staticmethod
    def stop_loss_hit(
        side: str,
        current_price: float,
        stop_loss: float
    ) -> ExitDecision:

        side = side.upper()

        if (
            side == "LONG"
            and
            current_price <= stop_loss
        ):

            return ExitDecision(
                should_exit=True,
                reason="STOP_LOSS"
            )

        if (
            side == "SHORT"
            and
            current_price >= stop_loss
        ):

            return ExitDecision(
                should_exit=True,
                reason="STOP_LOSS"
            )

        return ExitDecision(
            should_exit=False,
            reason="HOLD"
        )

    @staticmethod
    def target_hit(
        side: str,
        current_price: float,
        target: float
    ) -> ExitDecision:

        side = side.upper()

        if (
            side == "LONG"
            and
            current_price >= target
        ):

            return ExitDecision(
                should_exit=True,
                reason="TARGET"
            )

        if (
            side == "SHORT"
            and
            current_price <= target
        ):

            return ExitDecision(
                should_exit=True,
                reason="TARGET"
            )

        return ExitDecision(
            should_exit=False,
            reason="HOLD"
        )

    @staticmethod
    def force_exit_required() -> ExitDecision:

        if (
            datetime.now().time()
            >= FORCE_EXIT_TIME
        ):

            return ExitDecision(
                should_exit=True,
                reason="FORCE_EXIT"
            )

        return ExitDecision(
            should_exit=False,
            reason="HOLD"
        )

    @staticmethod
    def manual_exit() -> ExitDecision:

        return ExitDecision(
            should_exit=True,
            reason="MANUAL_EXIT"
        )