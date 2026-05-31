# core/indicators/cvd.py

from core.indicators.indicator_base import (
    IndicatorBase
)

from core.logging_manager import (
    LoggingManager
)


class CVD(IndicatorBase):
    """
    Cumulative Volume Delta.

    Tick Rule Implementation:

    Price Up
        -> Buy Volume

    Price Down
        -> Sell Volume

    Price Unchanged
        -> Ignore
    """

    def __init__(
        self,
        name: str,
        symbol: str,
        timeframe: str
    ) -> None:

        super().__init__(
            name=name,
            symbol=symbol,
            timeframe=timeframe
        )

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.previous_price = None

        self.buy_volume = 0

        self.sell_volume = 0

        self.delta = 0

        self.cvd = 0

    def update(
        self,
        price: float,
        volume: int
    ) -> None:
        """
        Update CVD.
        """

        try:

            if (
                self.previous_price
                is None
            ):

                self.previous_price = (
                    price
                )

                return

            if (
                price
                >
                self.previous_price
            ):

                self.buy_volume += (
                    volume
                )

                self.delta = (
                    volume
                )

            elif (
                price
                <
                self.previous_price
            ):

                self.sell_volume += (
                    volume
                )

                self.delta = (
                    -volume
                )

            else:

                self.delta = 0

            self.cvd += (
                self.delta
            )

            self.previous_price = (
                price
            )

            self.current_value = (
                self.cvd
            )

            self.increment_updates()

            if not self.ready:

                self.mark_ready()

        except Exception as error:

            self.logger.error(
                f"CVD update failed: "
                f"{error}"
            )

    def get_cvd(
        self
    ) -> int:

        return self.cvd

    def get_delta(
        self
    ) -> int:

        return self.delta

    def get_buy_volume(
        self
    ) -> int:

        return self.buy_volume

    def get_sell_volume(
        self
    ) -> int:

        return self.sell_volume

    def is_bullish(
        self
    ) -> bool:

        return self.cvd > 0

    def is_bearish(
        self
    ) -> bool:

        return self.cvd < 0

    def reset(
        self
    ) -> None:

        self.previous_price = None

        self.buy_volume = 0

        self.sell_volume = 0

        self.delta = 0

        self.cvd = 0

        self.current_value = 0.0

        self.ready = False

        self.total_updates = 0