# runtime/tick_processor.py
from threading import Lock
from typing import Any, Optional

from core.logging_manager import LoggingManager

from core.websocket.tick_queue import TickQueue

from runtime.orderflow_runtime import OrderFlowRuntime

from core.market_data.timeframe_manager import TimeframeManager

from runtime.indicator_runtime import IndicatorRuntime

from runtime.signal_runtime import SignalRuntime

from runtime.multifactor_runtime import MultiFactorRuntime


class TickProcessor:
    """
    Consumes ticks from TickQueue and maintains
    latest market state.

    Responsibilities:
    - consume queue
    - store latest tick per token
    - provide lookup access
    - track processing statistics

    Does NOT:
    - generate indicators
    - execute trades directly
    """

    def __init__(
        self,
        tick_queue: TickQueue,
        orderflow_runtime: OrderFlowRuntime,
        timeframe_manager: TimeframeManager,
        indicator_runtime: IndicatorRuntime,
        signal_runtime: SignalRuntime,
        multifactor_runtime: MultiFactorRuntime,
    ) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.tick_queue = tick_queue

        self.orderflow_runtime = orderflow_runtime

        self.timeframe_manager = timeframe_manager

        self.indicator_runtime = indicator_runtime

        self.signal_runtime = signal_runtime

        self.multifactor_runtime = multifactor_runtime

        self.lock = Lock()

        self.latest_ticks: dict[str, dict[str, Any]] = {}

        self.total_processed = 0

        self.invalid_ticks = 0

    def process_next_tick(self) -> bool:
        """
        Process a single tick.

        Returns:
            True if tick processed.
        """

        tick = self.tick_queue.dequeue()

        if tick is None:
            return False

        try:
            symbol = str(tick.get("symbol", ""))
            self.logger.info(f"[TICK] {symbol} {tick.get('ltp')}")
            if not symbol:
                self.invalid_ticks += 1

                return False

            with self.lock:
                self.latest_ticks[symbol] = tick

                self.total_processed += 1

            self.orderflow_runtime.process_tick(tick)

            closed_candles = self.timeframe_manager.process_tick(tick)

            for candle in closed_candles:
                self.logger.info(
                    f"[CANDLE] {candle.symbol} {candle.timeframe} C={candle.close}"
                )
                # ----------------------------------
                # Indicator Updates
                # ----------------------------------

                self.indicator_runtime.process_closed_candle(candle)
                self.logger.info(
                    f"[INDICATOR] "
                    f"{candle.symbol} "
                    f"{candle.timeframe} "
                    f"close={candle.close}"
                )

                # ----------------------------------
                # Legacy Signal Path
                # Keep alive during migration
                # ----------------------------------

                self.signal_runtime.evaluate_signals(candle)

                # ----------------------------------
                # New MultiFactor Path
                # ----------------------------------
                ema_fast = self.indicator_runtime.get_indicator(
                    candle.symbol, candle.timeframe, "EMA_FAST"
                )

                ema_slow = self.indicator_runtime.get_indicator(
                    candle.symbol, candle.timeframe, "EMA_SLOW"
                )

                if ema_fast and ema_slow:
                    self.logger.info(
                        f"[EMA] "
                        f"{candle.symbol} "
                        f"{candle.timeframe} "
                        f"FAST={ema_fast.get_value()} "
                        f"SLOW={ema_slow.get_value()}"
                        f"FAST_READY={ema_fast.is_ready()} "
                        f"SLOW_READY={ema_slow.is_ready()} "
                        f"FAST_UPDATES={ema_fast.get_total_updates()} "
                        f"SLOW_UPDATES={ema_slow.get_total_updates()}"
                        
                    )
                self.multifactor_runtime.process_trade_opportunity(
                    symbol=candle.symbol,
                    timeframe=candle.timeframe,
                    current_price=candle.close,
                    account_size=100000.0,
                )

            return True

        except Exception as error:
            self.logger.error(f"Tick processing failed: {error}")

            self.invalid_ticks += 1

            return False

    def process_all_available(self) -> int:
        """
        Process all queued ticks.

        Returns:
            Number of ticks processed.
        """

        processed = 0

        while self.process_next_tick():
            processed += 1

        return processed

    def get_latest_tick(
        self,
        token: str,
    ) -> Optional[dict[str, Any]]:
        """
        Return latest tick for token.
        """

        with self.lock:
            return self.latest_ticks.get(token)

    def get_all_latest_ticks(self) -> dict[str, dict[str, Any]]:
        """
        Return snapshot of latest ticks.
        """

        with self.lock:
            return dict(self.latest_ticks)

    def get_total_processed(self) -> int:
        """
        Return processed tick count.
        """

        return self.total_processed

    def get_invalid_tick_count(self) -> int:
        """
        Return invalid tick count.
        """

        return self.invalid_ticks

    def get_tracked_symbol_count(self) -> int:
        """
        Return unique token count.
        """

        with self.lock:
            return len(self.latest_ticks)

    def clear(self) -> None:
        """
        Reset processor state.
        """

        with self.lock:
            self.latest_ticks.clear()

            self.total_processed = 0

            self.invalid_ticks = 0
