# core/trade_management/exit_rules.py

from datetime import datetime

from config.config import FORCE_EXIT_TIME

from core.trade_management.exit_decision import ExitDecision


class ExitRules:
    """
    Centralized exit rule engine.

    Supports:

    - stop loss
    - target
    - force exit
    - manual exit
    """

    @staticmethod
    def stop_loss_hit(
        side: str,
        current_price: float,
        stop_loss: float,
    ) -> ExitDecision:
        """
        Check stop loss.
        """

        side = side.upper()

        # LONG
        if side == "LONG":

            if current_price <= stop_loss:

                return ExitDecision(
                    should_exit=True,
                    reason="STOP_LOSS",
                )

        # SHORT
        elif side == "SHORT":

            if current_price >= stop_loss:

                return ExitDecision(
                    should_exit=True,
                    reason="STOP_LOSS",
                )

        return ExitDecision(
            should_exit=False,
            reason="HOLD",
        )

    @staticmethod
    def target_hit(
        side: str,
        current_price: float,
        target: float,
    ) -> ExitDecision:
        """
        Check profit target.
        """

        side = side.upper()

        # LONG
        if side == "LONG":

            if current_price >= target:

                return ExitDecision(
                    should_exit=True,
                    reason="TARGET",
                )

        # SHORT
        elif side == "SHORT":

            if current_price <= target:

                return ExitDecision(
                    should_exit=True,
                    reason="TARGET",
                )

        return ExitDecision(
            should_exit=False,
            reason="HOLD",
        )

    @staticmethod
    def force_exit_time_hit() -> ExitDecision:
        """
        Exit all positions after configured time.
        """

        now = datetime.now().time()

        if now >= FORCE_EXIT_TIME:

            return ExitDecision(
                should_exit=True,
                reason="FORCE_EXIT",
            )

        return ExitDecision(
            should_exit=False,
            reason="HOLD",
        )

    @staticmethod
    def manual_exit_requested(
        requested: bool,
    ) -> ExitDecision:
        """
        Future GUI/manual exit hook.
        """

        if requested:

            return ExitDecision(
                should_exit=True,
                reason="MANUAL_EXIT",
            )

        return ExitDecision(
            should_exit=False,
            reason="HOLD",
        )