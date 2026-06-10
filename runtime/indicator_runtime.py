# runtime/indicator_runtime.py

from core.indicators.indicator_manager import IndicatorManager

from core.market_data.candle import Candle
from core.logging_manager import LoggingManager

class IndicatorRuntime:
    def __init__(self) -> None:
        self.logger = LoggingManager.get_logger(__name__)
        self.indicator_manager = IndicatorManager()

    def register_indicator(self, indicator) -> bool:

        return self.indicator_manager.register_indicator(indicator)

    def process_closed_candle(self, candle: Candle) -> None:

        if not candle.is_closed:
            return

        self.indicator_manager.update_indicators(candle)
        self.logger.info(
            f"Indicator update: "
            f"{candle.symbol} "
            f"{candle.timeframe} "
            f"close={candle.close}"
        )

    def get_indicator_value(self, symbol: str, timeframe: str, indicator_name: str):

        return self.indicator_manager.get_indicator_value(
            symbol, timeframe, indicator_name
        )

    def get_indicator(self, symbol: str, timeframe: str, indicator_name: str):
        """
        Return indicator instance.
        """

        return self.indicator_manager.get_indicator(symbol, timeframe, indicator_name)
