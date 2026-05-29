# core/signals/signal.py

from dataclasses import dataclass, field

from datetime import datetime

from typing import Any


@dataclass(slots=True)
class Signal:
    """
    Standardized trading signal.
    """

    symbol: str

    timeframe: str

    signal_type: str

    strength: float

    timestamp: datetime

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def is_buy(self) -> bool:
        """
        Check BUY signal.
        """

        return (
            self.signal_type.upper()
            == "BUY"
        )

    def is_sell(self) -> bool:
        """
        Check SELL signal.
        """

        return (
            self.signal_type.upper()
            == "SELL"
        )

    def is_exit(self) -> bool:
        """
        Check EXIT signal.
        """

        return (
            self.signal_type.upper()
            == "EXIT"
        )

    def is_neutral(self) -> bool:
        """
        Check NEUTRAL signal.
        """

        return (
            self.signal_type.upper()
            == "NEUTRAL"
        )

    def to_dict(self) -> dict:
        """
        Convert signal to dictionary.
        """

        return {
            "symbol": self.symbol,

            "timeframe": self.timeframe,

            "signal_type": self.signal_type,

            "strength": self.strength,

            "timestamp": self.timestamp,

            "metadata": self.metadata
        }
