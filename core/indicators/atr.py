# core/indicators/atr.py

from collections import deque

from core.indicators.indicator_base import IndicatorBase

from core.market_data.candle import Candle


class ATR(IndicatorBase):
    """
    Average True Range (ATR).

    Wilder ATR implementation.
    """

    def __init__(
        self, name: str, symbol: str, timeframe: str, period: int = 14
    ) -> None:

        super().__init__(name=name, symbol=symbol, timeframe=timeframe)

        self.period = period

        self.previous_close: float | None = None

        self.true_ranges = deque(maxlen=period)

        self.atr_value = 0.0

        self.ready = False

    def update(self, candle: Candle) -> None:
        """
        Update ATR using closed candle.
        """

        try:
            high = candle.high
            low = candle.low
            close = candle.close

            if self.previous_close is None:
                tr = high - low

            else:
                tr = max(
                    high - low,
                    abs(high - self.previous_close),
                    abs(low - self.previous_close),
                )

            self.true_ranges.append(tr)

            if len(self.true_ranges) < self.period:
                self.previous_close = close

                return

            # Initial ATR

            if not self.ready:
                self.atr_value = sum(self.true_ranges) / self.period

                self.ready = True

            else:
                self.atr_value = (
                    (self.atr_value * (self.period - 1)) + tr
                ) / self.period

            self.previous_close = close

        except Exception:
            pass

    def get_value(self) -> float:

        return round(self.atr_value, 4)

    def is_ready(self) -> bool:

        return self.ready

    def reset(self) -> None:

        self.previous_close = None

        self.true_ranges.clear()

        self.atr_value = 0.0

        self.ready = False
