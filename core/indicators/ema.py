# core/indicators/ema.py

from core.indicators.indicator_base import IndicatorBase

from core.market_data.candle import Candle


class EMA(IndicatorBase):
    """
    Exponential Moving Average.
    """

    def __init__(
        self,
        name: str,
        symbol: str,
        timeframe: str,
        period: int,
    ) -> None:

        super().__init__(
            name=name,
            symbol=symbol,
            timeframe=timeframe,
        )

        self.period = period

        self.multiplier = 2.0 / (period + 1)

        self.ema_value: float | None = None

    def update(self, candle: Candle) -> None:

        close_price = candle.close

        self.increment_updates()

        if self.ema_value is None:
            self.ema_value = close_price

            self.current_value = close_price

            self.mark_ready()

            return

        self.ema_value = (
            (close_price - self.ema_value) * self.multiplier
        ) + self.ema_value

        self.current_value = self.ema_value

    def reset(self) -> None:

        self.ema_value = None

        self.current_value = 0.0

        self.ready = False

        self.total_updates = 0

    def get_period(self) -> int:

        return self.period

    def get_value(self) -> float:

        return round(self.current_value, 4)
