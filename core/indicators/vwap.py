
# core/indicators/vwap.py

from datetime import date

from core.indicators.indicator_base import (
    IndicatorBase
)

from core.logging_manager import LoggingManager

from core.market_data.candle import Candle

from core.market_data.market_clock import (
    MarketClock
)


class VWAP(IndicatorBase):
    """
    Session-based Volume Weighted Average Price.

    Formula:
        VWAP =
        sum(typical_price * volume)
        ---------------------------
              sum(volume)

    Typical Price:
        (high + low + close) / 3
    """

    def __init__(
        self,
        name: str,
        symbol: str,
        timeframe: str,
        market_clock: MarketClock
    ) -> None:

        super().__init__(
            name=name,
            symbol=symbol,
            timeframe=timeframe
        )

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.market_clock = market_clock

        self.cumulative_price_volume = 0.0

        self.cumulative_volume = 0

        self.current_session_date: (
            date | None
        ) = None

    def update(
        self,
        candle: Candle
    ) -> None:
        """
        Update VWAP using closed candle.
        """

        try:

            candle_date = (
                candle.start_time.date()
            )

            # ====================================
            # SESSION RESET
            # ====================================

            if (
                self.current_session_date
                is None
            ):

                self.current_session_date = (
                    candle_date
                )

            elif (
                candle_date
                != self.current_session_date
            ):

                self.logger.info(
                    f"{self.name} session "
                    f"reset triggered"
                )

                self.reset()

                self.current_session_date = (
                    candle_date
                )

            # ====================================
            # TYPICAL PRICE
            # ====================================

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
                typical_price * volume
            )

            self.cumulative_volume += (
                volume
            )

            # ====================================
            # SAFETY CHECK
            # ====================================

            if (
                self.cumulative_volume
                == 0
            ):

                self.logger.warning(
                    f"{self.name} cumulative "
                    f"volume is zero"
                )

                return

            # ====================================
            # VWAP CALCULATION
            # ====================================

            self.current_value = (
                self.cumulative_price_volume
                / self.cumulative_volume
            )

            if not self.ready:

                self.mark_ready()

        except Exception as error:

            self.logger.error(
                f"VWAP update failed: "
                f"{error}"
            )

    def reset(self) -> None:
        """
        Reset VWAP session state.
        """

        self.cumulative_price_volume = 0.0

        self.cumulative_volume = 0

        self.current_value = 0.0

        self.ready = False

        self.total_updates = 0

        self.current_session_date = None

        self.logger.info(
            f"{self.name} reset"
        )

    def get_session_date(
        self
    ) -> date | None:
        """
        Return active session date.
        """

        return self.current_session_date

    def get_cumulative_volume(
        self
    ) -> int:
        """
        Return cumulative session volume.
        """

        return self.cumulative_volume
