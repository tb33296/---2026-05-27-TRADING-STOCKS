# runtime/trading_cycle_engine.py

from core.logging_manager import LoggingManager

from runtime.tick_processor import TickProcessor

from runtime.candle_runtime import CandleRuntime

from runtime.indicator_runtime import IndicatorRuntime

from runtime.trading_runtime import TradingRuntime


class TradingCycleEngine:
    """
    Executes one complete market cycle.

    Responsibilities:

    - process queued ticks
    - update candles
    - update indicators
    - monitor open positions

    Future:

    - strategy evaluation
    - trade execution
    """

    def __init__(
        self,
        tick_processor: TickProcessor,
        candle_runtime: CandleRuntime,
        indicator_runtime: IndicatorRuntime,
        trading_runtime: TradingRuntime,
    ) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.tick_processor = tick_processor

        self.candle_runtime = candle_runtime

        self.indicator_runtime = indicator_runtime

        self.trading_runtime = trading_runtime

    def process_cycle(self) -> int:
        """
        Execute one market cycle.

        Returns:
            Number of positions closed.
        """

        self.tick_processor.process_all_available()

        closed_candles = self.candle_runtime.process_ticks()

        for candle in closed_candles:
            self.indicator_runtime.process_closed_candle(candle)

        return self.trading_runtime.process_market()
