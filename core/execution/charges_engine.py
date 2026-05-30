# core/execution/charges_engine.py

from core.logging_manager import (
    LoggingManager
)


class ChargesEngine:
    """
    Trading charge calculator.

    V1 Rules:

    Equity Intraday:
        Lower of ₹20 or 0.1%
        Minimum ₹5

    F&O:
        ₹20 per executed order
    """

    def __init__(self) -> None:

        self.logger = LoggingManager.get_logger(
            __name__
        )

    def calculate_equity_intraday(
        self,
        turnover: float
    ) -> float:
        """
        Calculate equity intraday charges.

        Lower of:
            ₹20
            0.1% of turnover

        Minimum:
            ₹5
        """

        try:

            charges = min(
                20.0,
                turnover * 0.001
            )

            charges = max(
                5.0,
                charges
            )

            return round(
                charges,
                2
            )

        except Exception:

            return 0.0

    def calculate_fno(
        self
    ) -> float:
        """
        F&O charge.

        ₹20 per executed order.
        """

        return 20.0

    def calculate(
        self,
        segment: str,
        turnover: float
    ) -> float:
        """
        Generic charge calculator.
        """

        segment = (
            segment.upper().strip()
        )

        if segment == "EQUITY":

            return (
                self.calculate_equity_intraday(
                    turnover
                )
            )

        if segment == "FNO":

            return (
                self.calculate_fno()
            )

        self.logger.warning(
            f"Unknown segment: "
            f"{segment}"
        )

        return 0.0