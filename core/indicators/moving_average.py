# core/indicators/moving_average.py

from collections import deque
from typing import Deque

from core.indicators.indicator_base import IndicatorBase

from core.logging_manager import LoggingManager

from core.market_data.candle import Candle


class MovingAverage(IndicatorBase):
    """
    Supports:
    - SMA
    - EMA
    """

    VALID_TYPES = {"SMA", "EMA"}

    def __init__(
        self, name: str, symbol: str, timeframe: str, period: int, ma_type: str = "SMA"
    ) -> None:

        super().__init__(name=name, symbol=symbol, timeframe=timeframe)

        self.logger = LoggingManager.get_logger(__name__)

        self.period = period

        self.ma_type = ma_type.upper().strip()

        if self.ma_type not in self.VALID_TYPES:
            raise ValueError(f"Unsupported MA type: {self.ma_type}")

        self.values: Deque[float] = deque(maxlen=period)

        self.rolling_sum = 0.0

        self.multiplier = 2 / (period + 1)

    def update(self, candle: Candle) -> None:
        """
        Update moving average using
        closed candle.
        """

        try:
            close_price = candle.close

            self.increment_updates()

            # ================================
            # SMA UPDATE
            # ================================

            if self.ma_type == "SMA":
                self._update_sma(close_price)

            # ================================
            # EMA UPDATE
            # ================================

            elif self.ma_type == "EMA":
                self._update_ema(close_price)

        except Exception as error:
            self.logger.error(f"Moving average update failed: {error}")

    def _update_sma(self, close_price: float) -> None:
        """
        Incremental SMA update.
        """

        if len(self.values) == self.period:
            oldest = self.values[0]

            self.rolling_sum -= oldest

        self.values.append(close_price)

        self.rolling_sum += close_price

        if len(self.values) < self.period:
            return

        self.current_value = self.rolling_sum / self.period

        if not self.ready:
            self.mark_ready()

    def _update_ema(self, close_price: float) -> None:
        """
        Incremental EMA update.
        """

        self.values.append(close_price)

        # ====================================
        # INITIAL EMA SEED
        # ====================================

        if not self.ready:
            if len(self.values) < self.period:
                return

            self.current_value = sum(self.values) / self.period

            self.mark_ready()

            return

        # ====================================
        # EMA UPDATE
        # ====================================

        self.current_value = (close_price * self.multiplier) + (
            self.current_value * (1 - self.multiplier)
        )

    def reset(self) -> None:
        """
        Reset indicator state.
        """

        self.values.clear()

        self.current_value = 0.0

        self.rolling_sum = 0.0

        self.ready = False

        self.total_updates = 0

        self.logger.info(f"{self.name} reset")

    def get_period(self) -> int:
        """
        Return MA period.
        """

        return self.period

    def get_ma_type(self) -> str:
        """
        Return moving average type.
        """

        return self.ma_type
