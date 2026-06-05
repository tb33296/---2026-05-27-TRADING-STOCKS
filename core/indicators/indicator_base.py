# core/indicators/indicator_base.py

from abc import ABC, abstractmethod

from core.market_data.candle import Candle


class IndicatorBase(ABC):
    """
    Base class for all indicators.

    Responsibilities:
    - indicator lifecycle contract
    - candle update interface
    - readiness tracking
    - value retrieval
    """

    def __init__(self, name: str, symbol: str, timeframe: str) -> None:

        self.name = name

        self.symbol = symbol

        self.timeframe = timeframe

        self.current_value: float = 0.0

        self.ready = False

        self.total_updates = 0

    @abstractmethod
    def update(self, candle: Candle) -> None:
        """
        Update indicator using closed candle.
        """

        pass

    @abstractmethod
    def reset(self) -> None:
        """
        Reset indicator state.
        """

        pass

    def get_value(self) -> float:
        """
        Return current indicator value.
        """

        return self.current_value

    def is_ready(self) -> bool:
        """
        Return indicator readiness state.
        """

        return self.ready

    def get_name(self) -> str:
        """
        Return indicator name.
        """

        return self.name

    def get_symbol(self) -> str:
        """
        Return indicator symbol.
        """

        return self.symbol

    def get_timeframe(self) -> str:
        """
        Return indicator timeframe.
        """

        return self.timeframe

    def get_total_updates(self) -> int:
        """
        Return update count.
        """

        return self.total_updates

    def mark_ready(self) -> None:
        """
        Mark indicator as ready.
        """

        self.ready = True

    def increment_updates(self) -> None:
        """
        Increment update counter.
        """

        self.total_updates += 1
