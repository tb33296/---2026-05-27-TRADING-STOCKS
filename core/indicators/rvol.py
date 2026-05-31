# core/indicators/rvol.py

from collections import deque

from core.indicators.indicator_base import (
    IndicatorBase
)

from core.market_data.candle import (
    Candle
)


class RVOL(IndicatorBase):
    """
    Relative Volume.

    RVOL =
        Current Volume /
        Average Volume
    """

    def __init__(
        self,
        name: str,
        symbol: str,
        timeframe: str,
        period: int = 20
    ) -> None:

        super().__init__(
            name=name,
            symbol=symbol,
            timeframe=timeframe
        )

        self.period = period

        self.volume_history = deque(
            maxlen=period
        )

        self.rvol_value = 0.0

        self.ready = False

    def update(
        self,
        candle: Candle
    ) -> None:
        """
        Update RVOL using candle volume.
        """

        try:

            volume = float(
                candle.volume
            )

            self.volume_history.append(
                volume
            )

            if (
                len(self.volume_history)
                < self.period
            ):
                return

            average_volume = (
                sum(
                    self.volume_history
                )
                /
                self.period
            )

            if average_volume <= 0:

                self.rvol_value = 0.0

            else:

                self.rvol_value = (
                    volume
                    /
                    average_volume
                )

            self.ready = True

        except Exception:

            pass

    def get_value(
        self
    ) -> float:

        return round(
            self.rvol_value,
            4
        )

    def is_ready(
        self
    ) -> bool:

        return self.ready

    def reset(
        self
    ) -> None:

        self.volume_history.clear()

        self.rvol_value = 0.0

        self.ready = False