# core/indicators/liquidity_delta.py

from core.indicators.indicator_base import (
    IndicatorBase
)

from core.logging_manager import (
    LoggingManager
)


class LiquidityDelta(IndicatorBase):
    """
    Level 2 Order Book Liquidity Delta.

    Delta:
        Bid Qty - Ask Qty

    Ratio:
        Bid Qty / (Bid Qty + Ask Qty)

    Interpretation:

        Ratio > 0.50
            Bullish

        Ratio < 0.50
            Bearish
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

        self.bid_quantity = 0

        self.ask_quantity = 0

        self.delta = 0

        self.ratio = 0.5

    def update(
        self,
        depth_data: dict
    ) -> None:
        """
        Update liquidity metrics.

        Expected:

        {
            "buy": [...],
            "sell": [...]
        }
        """

        try:

            buy_levels = (
                depth_data.get(
                    "buy",
                    []
                )
            )

            sell_levels = (
                depth_data.get(
                    "sell",
                    []
                )
            )

            self.bid_quantity = sum(
                level.get(
                    "quantity",
                    0
                )
                for level in buy_levels
            )

            self.ask_quantity = sum(
                level.get(
                    "quantity",
                    0
                )
                for level in sell_levels
            )

            self.delta = (
                self.bid_quantity
                -
                self.ask_quantity
            )

            total = (
                self.bid_quantity
                +
                self.ask_quantity
            )

            if total > 0:

                self.ratio = (
                    self.bid_quantity
                    / total
                )

            else:

                self.ratio = 0.5

            self.current_value = (
                self.delta
            )

            self.increment_updates()

            if not self.ready:

                self.mark_ready()

        except Exception as error:

            self.logger.error(
                f"LiquidityDelta update failed: "
                f"{error}"
            )

    def get_delta(
        self
    ) -> int:

        return self.delta

    def get_ratio(
        self
    ) -> float:

        return round(
            self.ratio,
            4
        )

    def get_bid_quantity(
        self
    ) -> int:

        return self.bid_quantity

    def get_ask_quantity(
        self
    ) -> int:

        return self.ask_quantity

    def is_bullish(
        self
    ) -> bool:

        return self.ratio > 0.50

    def is_bearish(
        self
    ) -> bool:

        return self.ratio < 0.50

    def reset(
        self
    ) -> None:

        self.bid_quantity = 0

        self.ask_quantity = 0

        self.delta = 0

        self.ratio = 0.5

        self.current_value = 0.0

        self.ready = False

        self.total_updates = 0