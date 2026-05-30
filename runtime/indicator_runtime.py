# runtime/indicator_runtime.py

from core.indicators.indicator_manager import (
    IndicatorManager
)

from core.market_data.candle import Candle


class IndicatorRuntime:

    def __init__(self) -> None:

        self.indicator_manager = (
            IndicatorManager()
        )

    def register_indicator(
        self,
        indicator
    ) -> bool:

        return (
            self.indicator_manager
            .register_indicator(
                indicator
            )
        )

    def process_closed_candle(
        self,
        candle: Candle
    ) -> None:

        if not candle.is_closed:
            return

        self.indicator_manager\
            .update_indicators(
                candle
            )

    def get_indicator_value(
        self,
        symbol: str,
        timeframe: str,
        indicator_name: str
    ):

        return (
            self.indicator_manager
            .get_indicator_value(
                symbol,
                timeframe,
                indicator_name
            )
        )