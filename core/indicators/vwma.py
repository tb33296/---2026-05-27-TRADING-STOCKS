# core/indicators/vwma.py

from collections import deque
from typing import Deque

from core.indicators.indicator_base import (
    IndicatorBase
)

from core.logging_manager import LoggingManager

from core.market_data.candle import Candle


class VWMA(IndicatorBase):
    """
    Volume Weighted Moving Average.

    Formula:
        VWMA =
        sum(price * volume)
        -------------------
            sum(volume)
    """

    def __init__(
        self,
        name: str,
        symbol: str,
        timeframe: str,
        period: int
    ) -> None:

        super().__init__(
            name=name,
            symbol=symbol,
            timeframe=timeframe
        )

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.period = period

        self.values: Deque[
            tuple[float, int]
        ] = deque(
            maxlen=period
        )

        self.price_volume_sum = 0.0

        self.volume_sum = 0

    def update(
        self,
        candle: Candle
    ) -> None:
        """
        Update VWMA using closed candle.
        """

        try:

            close_price = candle.close

            volume = candle.volume

            self.increment_updates()

            # ================================
            # REMOVE OLDEST VALUE
            # ================================

            if (
                len(self.values)
                == self.period
            ):

                old_price, old_volume = (
                    self.values[0]
                )

                self.price_volume_sum -= (
                    old_price * old_volume
                )

                self.volume_sum -= (
                    old_volume
                )

            # ================================
            # ADD NEW VALUE
            # ================================

            self.values.append(
                (
                    close_price,
                    volume
                )
            )

            self.price_volume_sum += (
                close_price * volume
            )

            self.volume_sum += volume

            # ================================
            # READINESS CHECK
            # ================================

            if (
                len(self.values)
                < self.period
            ):

                return

            if self.volume_sum == 0:

                self.logger.warning(
                    f"{self.name} volume sum "
                    f"is zero"
                )

                return

            self.current_value = (
                self.price_volume_sum
                / self.volume_sum
            )

            if not self.ready:

                self.mark_ready()

        except Exception as error:

            self.logger.error(
                f"VWMA update failed: "
                f"{error}"
            )

    def reset(self) -> None:
        """
        Reset VWMA state.
        """

        self.values.clear()

        self.current_value = 0.0

        self.price_volume_sum = 0.0

        self.volume_sum = 0

        self.ready = False

        self.total_updates = 0

        self.logger.info(
            f"{self.name} reset"
        )

    def get_period(self) -> int:
        """
        Return VWMA period.
        """

        return self.period
