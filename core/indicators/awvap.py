# core/indicators/awvap.py

from datetime import datetime

from core.indicators.indicator_base import (
    IndicatorBase
)

from core.logging_manager import (
    LoggingManager
)

from core.market_data.candle import (
    Candle
)


class AWVAP(IndicatorBase):
    """
    Anchored VWAP.

    VWAP calculation begins only after
    the specified anchor time.

    Formula:

        AWVAP =
        Σ(TypicalPrice × Volume)
        ------------------------
              Σ(Volume)
    """

    def __init__(
        self,
        name: str,
        symbol: str,
        timeframe: str,
        anchor_time: datetime
    ) -> None:

        super().__init__(
            name=name,
            symbol=symbol,
            timeframe=timeframe
        )

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.anchor_time = (
            anchor_time
        )

        self.cumulative_price_volume = 0.0

        self.cumulative_volume = 0

    def update(
        self,
        candle: Candle
    ) -> None:
        """
        Update AWVAP.
        """

        try:

            if (
                candle.start_time
                < self.anchor_time
            ):

                return

            typical_price = (
                (
                    candle.high
                    +
                    candle.low
                    +
                    candle.close
                ) / 3
            )

            volume = candle.volume

            self.increment_updates()

            self.cumulative_price_volume += (
                typical_price
                *
                volume
            )

            self.cumulative_volume += (
                volume
            )

            if (
                self.cumulative_volume
                == 0
            ):

                return

            self.current_value = (
                self.cumulative_price_volume
                /
                self.cumulative_volume
            )

            if not self.ready:

                self.mark_ready()

        except Exception as error:

            self.logger.error(
                f"AWVAP update failed: "
                f"{error}"
            )

    def reset(
        self
    ) -> None:

        self.cumulative_price_volume = 0.0

        self.cumulative_volume = 0

        self.current_value = 0.0

        self.ready = False

        self.total_updates = 0

    def get_anchor_time(
        self
    ) -> datetime:

        return self.anchor_time

    def get_cumulative_volume(
        self
    ) -> int:

        return self.cumulative_volume