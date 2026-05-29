# runtime/runtime_engine.py

from __future__ import annotations

from typing import Optional

from config.config import MAX_TICK_QUEUE_SIZE

from core.session.session_manager import (
    SessionManager
)

from core.websocket.tick_queue import (
    TickQueue
)

from core.websocket.websocket_manager import (
    WebSocketManager
)

from core.watchdog.heartbeat_monitor import (
    HeartbeatMonitor
)

from core.logging_manager import (
    LoggingManager
)


class RuntimeEngine:
    """
    Runtime Engine v1

    Responsibilities:

    Session
    → Auth
    → WebSocket
    → Tick Queue
    → Heartbeat Monitor

    Future Versions:

    Tick Queue
    → Candle Builder
    → Indicators
    → Signals
    → Strategy
    → Paper Broker
    """

    def __init__(self) -> None:

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.session_manager: Optional[
            SessionManager
        ] = None

        self.tick_queue: Optional[
            TickQueue
        ] = None

        self.websocket_manager: Optional[
            WebSocketManager
        ] = None

        self.heartbeat_monitor: Optional[
            HeartbeatMonitor
        ] = None

        self.running = False

    def start(self) -> bool:
        """
        Start runtime engine.
        """

        try:

            self.logger.info(
                "Starting Runtime Engine"
            )

            # -------------------------
            # Session + Authentication
            # -------------------------

            self.session_manager = (
                SessionManager()
            )

            auth_manager = (
                self.session_manager.get_auth_manager()
            )

            if not auth_manager.login():

                self.logger.error(
                    "Authentication failed"
                )

                return False

            # -------------------------
            # Tick Queue
            # -------------------------

            self.tick_queue = TickQueue(
                max_size=MAX_TICK_QUEUE_SIZE
            )

            # -------------------------
            # WebSocket
            # -------------------------

            self.websocket_manager = (
                WebSocketManager(
                    session_manager=
                    self.session_manager,
                    tick_queue=
                    self.tick_queue
                )
            )

            # -------------------------
            # Heartbeat Monitor
            # -------------------------

            self.heartbeat_monitor = (
                HeartbeatMonitor(
                    self.websocket_manager
                )
            )

            # -------------------------
            # Connect WebSocket
            # -------------------------

            if not (
                self.websocket_manager.connect()
            ):

                self.logger.error(
                    "WebSocket connection failed"
                )

                return False

            self.running = True

            self.logger.info(
                "Runtime Engine started"
            )

            return True

        except Exception as error:

            self.logger.exception(
                f"Runtime startup failed: "
                f"{error}"
            )

            return False

    def stop(self) -> None:
        """
        Stop runtime engine.
        """

        try:

            self.logger.info(
                "Stopping Runtime Engine"
            )

            self.running = False

            if (
                self.websocket_manager
                is not None
            ):

                self.websocket_manager.disconnect()

            self.logger.info(
                "Runtime Engine stopped"
            )

        except Exception as error:

            self.logger.exception(
                f"Runtime shutdown failed: "
                f"{error}"
            )

    def is_running(self) -> bool:
        """
        Runtime status.
        """

        return self.running