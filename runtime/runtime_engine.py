# runtime/runtime_engine.py

from config.config import (
    INSTRUMENT_MASTER_PATH,
    DEFAULT_WATCHLIST_FILE,
    MAX_TICK_QUEUE_SIZE
)

from core.logging_manager import (
    LoggingManager
)

from core.session.session_manager import (
    SessionManager
)

from core.websocket.tick_queue import (
    TickQueue
)

from core.websocket.websocket_manager import (
    WebSocketManager
)

from core.instruments.instrument_manager import (
    InstrumentManager
)

from core.instruments.token_resolver import (
    TokenResolver
)

from core.instruments.symbol_registry import (
    SymbolRegistry
)

from core.websocket.subscription_manager import (
    SubscriptionManager
)

from utils.watchlist_loader import (
    WatchlistLoader
)


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

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.session_manager = (
            SessionManager()
        )

        self.tick_queue = TickQueue(
            MAX_TICK_QUEUE_SIZE
        )

        self.websocket_manager = (
            WebSocketManager(
                self.session_manager,
                self.tick_queue
            )
        )

        self.instrument_manager = (
            InstrumentManager(
                INSTRUMENT_MASTER_PATH
            )
        )

        self.token_resolver = (
            TokenResolver(
                self.instrument_manager
            )
        )

        self.symbol_registry = (
            SymbolRegistry(
                self.token_resolver
            )
        )

        self.subscription_manager = (
            SubscriptionManager(
                self.symbol_registry
            )
        )

        self.watchlist_loader = (
            WatchlistLoader()
        )

        self.is_running = False

    def start(self) -> bool:
        """
        Start trading runtime.
        """

        try:

            self.logger.info(
                "Starting runtime engine"
            )

            # -------------------------
            # Session
            # -------------------------

            if not (
                self.session_manager
                .start_session()
            ):

                self.logger.error(
                    "Session startup failed"
                )

                return False

            # -------------------------
            # Instruments
            # -------------------------

            if not (
                self.instrument_manager
                .load_instruments()
            ):

                self.logger.error(
                    "Instrument loading failed"
                )

                return False

            # -------------------------
            # Watchlist
            # -------------------------

            symbols = (
                self.watchlist_loader.load(
                    DEFAULT_WATCHLIST_FILE
                )
            )

            if not symbols:

                self.logger.error(
                    "Watchlist empty"
                )

                return False

            added = 0

            for symbol in symbols:

                if (
                    self.symbol_registry
                    .add_symbol(symbol)
                ):

                    added += 1

            self.logger.info(
                f"Registered "
                f"{added} symbols"
            )

            # -------------------------
            # Subscription Payload
            # -------------------------

            payload = (
                self.subscription_manager
                .build_subscription_payload(
                    exchange="NSE"
                )
            )

            if payload is None:

                self.logger.error(
                    "Subscription payload failed"
                )

                return False

            # -------------------------
            # WebSocket
            # -------------------------

            if not (
                self.websocket_manager
                .connect()
            ):

                self.logger.error(
                    "WebSocket connection failed"
                )

                return False

            # -------------------------
            # Subscribe
            # -------------------------

            if not (
                self.websocket_manager
                .subscribe(
                    correlation_id="runtime_engine",
                    mode=1,
                    token_list=payload
                )
            ):

                self.logger.error(
                    "Subscription failed"
                )

                return False

            self.is_running = True

            self.logger.info(
                "Runtime engine started successfully"
            )

            return True

        except Exception as error:

            self.logger.error(
                f"Runtime startup failed: "
                f"{error}"
            )

            return False

    def stop(self) -> None:
        """
        Stop runtime.
        """

        try:

            self.is_running = False

            self.websocket_manager.disconnect()

            self.session_manager.logout()

            self.logger.info(
                "Runtime engine stopped"
            )

        except Exception as error:

            self.logger.error(
                f"Runtime shutdown failed: "
                f"{error}"
            )

    def is_alive(self) -> bool:
        """
        Runtime health status.
        """

        if not self.is_running:
            return False

        return (
            self.session_manager
            .is_session_alive()
        )

    def get_tick_queue(self) -> TickQueue:
        """
        Return tick queue.
        """

        return self.tick_queue

    def get_websocket_manager(
        self
    ) -> WebSocketManager:
        """
        Return websocket manager.
        """

        return self.websocket_manager

    def get_symbol_registry(
        self
    ) -> SymbolRegistry:
        """
        Return symbol registry.
        """

        return self.symbol_registry