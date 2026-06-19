# runtime/runtime_engine.py

from config.config import (
    INSTRUMENT_MASTER_PATH,
    DEFAULT_WATCHLIST_FILE,
    MAX_TICK_QUEUE_SIZE,
    MAX_DEPTH_QUEUE_SIZE,
)
from core.execution.pending_order_manager import PendingOrderManager

from config.config import ACTIVE_TIMEFRAMES

from config.config import WEBSOCKET_MODE_QUOTE, WEBSOCKET_MODE_DEPTH

from core.logging_manager import LoggingManager

from core.session.session_manager import SessionManager

from core.websocket.tick_queue import TickQueue

from core.websocket.depth_queue import DepthQueue

from core.websocket.websocket_manager import WebSocketManager

from core.instruments.instrument_manager import InstrumentManager

from core.instruments.token_resolver import TokenResolver

from core.instruments.symbol_registry import SymbolRegistry

from core.websocket.subscription_manager import SubscriptionManager

from utils.watchlist_loader import WatchlistLoader

from runtime.orderflow_runtime import OrderFlowRuntime

from runtime.tick_processor import TickProcessor

from runtime.depth_processor import DepthProcessor

from threading import Thread
import time

from config.config import MARKET_HOLIDAY_FILE

from core.market_data.market_clock import MarketClock

from core.market_data.timeframe_manager import TimeframeManager

from runtime.indicator_runtime import IndicatorRuntime

from runtime.signal_runtime import SignalRuntime

from runtime.indicator_registration import IndicatorRegistration

from runtime.orderflow_registration import OrderFlowRegistration

from runtime.signal_registration import SignalRegistration

from database.db_manager import DatabaseManager

from core.positions.position_manager import PositionManager

from core.execution.paper_execution_engine import PaperExecutionEngine

from core.risk.risk_engine import RiskEngine

from core.journal.trade_journal_manager import TradeJournalManager

from runtime.trade_pipeline import TradePipeline

from core.trade_management.trade_manager import TradeManager

from runtime.trading_runtime import TradingRuntime

from runtime.multifactor_runtime import MultiFactorRuntime

from core.strategy.trade_decision_engine import TradeDecisionEngine

from core.risk.position_sizing_engine import PositionSizingEngine

# from runtime.orderflow_runtime import OrderFlowRuntime

class RuntimeEngine:
    """
    Main runtime orchestrator.

    Responsibilities:
    - session startup
    - instrument loading
    - watchlist loading
    - symbol registration
    - subscription generation
    - websocket startup
    """

    def __init__(self) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.session_manager = SessionManager()
        
        self.instrument_manager = InstrumentManager(INSTRUMENT_MASTER_PATH)

        self.token_resolver = TokenResolver(self.instrument_manager)

        self.symbol_registry = SymbolRegistry(self.token_resolver)
        self.tick_queue = TickQueue(MAX_TICK_QUEUE_SIZE)
        self.depth_queue = DepthQueue(MAX_DEPTH_QUEUE_SIZE)
        
        

        self.orderflow_runtime = OrderFlowRuntime()

        self.indicator_runtime = IndicatorRuntime()

        self.signal_runtime = SignalRuntime()

        self.market_clock = MarketClock()

        self.timeframe_manager = TimeframeManager(self.market_clock)

        self.db_manager = DatabaseManager()

        self.db_manager.connect()

        self.position_manager = PositionManager()

        self.execution_engine = PaperExecutionEngine(self.position_manager)

        self.risk_engine = RiskEngine(self.position_manager)

        self.journal_manager = TradeJournalManager(self.db_manager)

        self.pending_order_manager = PendingOrderManager()
        
        self.trade_pipeline = TradePipeline(
            risk_engine=self.risk_engine,
            execution_engine=self.execution_engine,
            journal_manager=self.journal_manager,
            pending_order_manager=self.pending_order_manager,
        )

        self.trade_decision_engine = TradeDecisionEngine()

        self.position_sizing_engine = PositionSizingEngine()

        self.multifactor_runtime = MultiFactorRuntime(
            indicator_runtime=self.indicator_runtime,
            orderflow_runtime=self.orderflow_runtime,
            trade_decision_engine=self.trade_decision_engine,
            position_sizing_engine=self.position_sizing_engine,
            trade_pipeline=self.trade_pipeline,
            instrument_manager=self.instrument_manager,
        )

        # self.signal_runtime = SignalRuntime()
        self.tick_processor = TickProcessor(
            self.tick_queue,
            self.orderflow_runtime,
            self.timeframe_manager,
            self.indicator_runtime,
            self.signal_runtime,
            self.multifactor_runtime,
        )
        self.trade_manager = TradeManager(
            position_manager=self.position_manager,
            trade_pipeline=self.trade_pipeline,
        )

        self.trading_runtime = TradingRuntime(
            tick_processor=self.tick_processor,
            trade_manager=self.trade_manager,
        )
        self.depth_processor = DepthProcessor(
            self.depth_queue,
            self.orderflow_runtime,
        )

        self.websocket_manager = WebSocketManager(
            self.session_manager, self.tick_queue, self.depth_queue
        )

        

        # =====================================
        # REGISTRATIONS
        # =====================================

        self.indicator_registration = IndicatorRegistration(
            indicator_runtime=self.indicator_runtime,
            symbol_registry=self.symbol_registry,
            market_clock=self.market_clock,
        )

        self.orderflow_registration = OrderFlowRegistration(
            symbol_registry=self.symbol_registry,
            orderflow_runtime=self.orderflow_runtime,
        )

        self.signal_registration = SignalRegistration(
            signal_runtime=self.signal_runtime,
            indicator_runtime=self.indicator_runtime,
            symbol_registry=self.symbol_registry,
        )

        self.subscription_manager = SubscriptionManager(self.symbol_registry)

        self.watchlist_loader = WatchlistLoader()

        self.is_running = False

        self.tick_processor_thread: Thread | None = None

        self.depth_processor_thread: Thread | None = None

        self.trade_monitor_thread: Thread | None = None

    def _tick_processor_worker(self) -> None:
        """
        Continuously process tick queue.
        """

        self.logger.info("TickProcessor worker started")

        while self.is_running:
            processed = self.tick_processor.process_all_available()

            if processed == 0:
                time.sleep(0.01)

    def _depth_processor_worker(self) -> None:
        """
        Continuously process depth queue.
        """

        self.logger.info("DepthProcessor worker started")

        while self.is_running:
            processed = self.depth_processor.process_all_available()

            if processed == 0:
                time.sleep(0.01)

    def _trade_monitor_worker(self) -> None:
        """
        Continuously monitor open positions.
        """

        self.logger.info("TradeMonitor worker started")

        while self.is_running:

            self.logger.info("[TRADE_MONITOR_LOOP]")

            try:

                self.trading_runtime.process_market()

            except Exception as error:

                self.logger.error(
                    f"[TRADE_MONITOR_CRASH] {error}"
                )

            time.sleep(1)

    def start(self) -> bool:
        """
        Start trading runtime.
        """

        try:
            self.logger.info("Starting runtime engine")

            # -------------------------
            # Session
            # -------------------------

            if not (self.session_manager.start_session()):
                self.logger.error("Session startup failed")

                return False

            # -------------------------
            # Instruments
            # -------------------------

            if not (self.instrument_manager.load_instruments()):
                self.logger.error("Instrument loading failed")

                return False

            # -------------------------
            # Watchlist
            # -------------------------

            symbols = self.watchlist_loader.load(DEFAULT_WATCHLIST_FILE)

            if not symbols:
                self.logger.error("Watchlist empty")

                return False

            added = 0

            for symbol in symbols:
                if self.symbol_registry.add_symbol(symbol):
                    added += 1

            self.logger.info(f"Registered {added} symbols")
            # =====================================
            # INDICATOR REGISTRATION
            # =====================================

            indicator_count = self.indicator_registration.register_all()

            strategy_count = 0
            orderflow_count = self.orderflow_registration.register_all()
            for symbol in self.symbol_registry.get_all_symbols():
                for timeframe in ACTIVE_TIMEFRAMES:
                    if self.multifactor_runtime.register_strategy(
                        symbol=symbol,
                        timeframe=timeframe,
                    ):
                        strategy_count += 1

            self.logger.info(f"Registered {strategy_count} strategies")

            self.logger.info(f"Registered {indicator_count} indicators")

            # =====================================
            # ORDERFLOW REGISTRATION
            # =====================================

            

            self.logger.info(f"Registered {orderflow_count} orderflow indicators")

            # =====================================
            # SIGNAL REGISTRATION
            # =====================================

            signal_count = self.signal_registration.register_all()

            self.logger.info(f"Registered {signal_count} signals")

            token_symbol_map = self.symbol_registry.get_token_symbol_map(exchange="NSE")

            self.websocket_manager.register_token_mappings(token_symbol_map)
            # -------------------------
            # Subscription Payload
            # -------------------------

            payload = self.subscription_manager.build_subscription_payload(
                exchange="NSE"
            )

            if payload is None:
                self.logger.error("Subscription payload failed")

                return False

            # -------------------------
            # WebSocket
            # -------------------------

            if not (self.websocket_manager.connect()):
                self.logger.error("WebSocket connection failed")

                return False

            # -------------------------
            # Subscribe
            # -------------------------

            # -------------------------
            # Mode 2 Subscription
            # -------------------------

            if not (
                self.websocket_manager.subscribe(
                    correlation_id="mode2_quote",
                    mode=WEBSOCKET_MODE_QUOTE,
                    token_list=payload,
                )
            ):
                self.logger.error("Mode 2 subscription failed")

                return False

            # -------------------------
            # Mode 4 Subscription
            # -------------------------

            if not (
                self.websocket_manager.subscribe(
                    correlation_id="mode4_depth",
                    mode=WEBSOCKET_MODE_DEPTH,
                    token_list=payload,
                )
            ):
                self.logger.error("Mode 4 subscription failed")

                return False

            self.is_running = True

            self.tick_processor_thread = Thread(
                target=self._tick_processor_worker,
                daemon=True,
                name="TickProcessorThread",
            )

            self.depth_processor_thread = Thread(
                target=self._depth_processor_worker,
                daemon=True,
                name="DepthProcessorThread",
            )

            self.trade_monitor_thread = Thread(
                target=self._trade_monitor_worker,
                daemon=True,
                name="TradeMonitorThread",
            )

            self.depth_processor_thread.start()

            self.tick_processor_thread.start()
            
            self.trade_monitor_thread.start()
            self.logger.info("TradeMonitor worker started")

            self.logger.info("Runtime engine started successfully")
            self.logger.info("Mode 2 Quote stream active")

            self.logger.info("Mode 4 Depth stream active")

            return True

        except Exception as error:
            self.logger.error(f"Runtime startup failed: {error}")

            return False

    def stop(self) -> None:
        """
        Stop runtime.
        """

        try:
            self.is_running = False

            self.websocket_manager.disconnect()

            self.session_manager.logout()

            self.logger.info("Runtime engine stopped")

        except Exception as error:
            self.logger.error(f"Runtime shutdown failed: {error}")

    def is_alive(self) -> bool:
        """
        Runtime health status.
        """

        if not self.is_running:
            return False

        return self.session_manager.is_session_alive()

    def get_tick_queue(self) -> TickQueue:
        """
        Return tick queue.
        """

        return self.tick_queue

    def get_websocket_manager(self) -> WebSocketManager:
        """
        Return websocket manager.
        """

        return self.websocket_manager

    def get_symbol_registry(self) -> SymbolRegistry:
        """
        Return symbol registry.
        """

        return self.symbol_registry

    def get_depth_queue(self) -> DepthQueue:
        """
        Return depth queue.
        """

        return self.depth_queue

    def get_orderflow_runtime(self) -> OrderFlowRuntime:
        """
        Return orderflow runtime.
        """

        return self.orderflow_runtime

    def get_tick_processor(self) -> TickProcessor:
        """
        Return tick processor.
        """

        return self.tick_processor

    def get_depth_processor(self) -> DepthProcessor:
        """
        Return self.depth processor.
        """

        return self.depth_processor

    def get_indicator_runtime(self) -> IndicatorRuntime:

        return self.indicator_runtime

    def get_signal_runtime(self) -> SignalRuntime:

        return self.signal_runtime
    
    
    def shutdown_positions(self) -> int:
        """
        Close all open positions using
        latest available market prices.
        """

        latest_ticks = self.tick_processor.get_all_latest_ticks()

        price_map: dict[str, float] = {}

        for symbol, tick in latest_ticks.items():

            ltp = tick.get("ltp")

            if ltp is None:
                continue

            price_map[symbol] = float(ltp)

        return self.trade_manager.force_exit_all_positions(
            price_map=price_map,
            reason="SYSTEM_SHUTDOWN",
        )
