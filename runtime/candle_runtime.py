# runtime/candle_runtime.py
from core.market_data.candle_builder import (
    CandleBuilder
)

from core.market_data.market_clock import (
    MarketClock
)

from config.config import (
    MARKET_HOLIDAY_FILE
)

from runtime.tick_processor import (
    TickProcessor
)


class CandleRuntime:

    def __init__(
        self,
        tick_processor: TickProcessor
    ) -> None:

        self.tick_processor = tick_processor

        self.market_clock = MarketClock(
            MARKET_HOLIDAY_FILE
        )

        self.candle_builder = CandleBuilder(
            self.market_clock
        )

    def process_ticks(self) -> int:
        """
        Convert processed ticks
        into live candles.
        """

        latest_ticks = (
            self.tick_processor
            .get_all_latest_ticks()
        )

        processed = 0

        for tick in latest_ticks.values():

            self.candle_builder.process_tick(
                tick=tick,
                timeframe="1m"
            )

            processed += 1

        return processed

    def get_current_candle(
        self,
        symbol: str
    ):

        return (
            self.candle_builder
            .get_current_candle(
                symbol=symbol,
                timeframe="1m"
            )
        )