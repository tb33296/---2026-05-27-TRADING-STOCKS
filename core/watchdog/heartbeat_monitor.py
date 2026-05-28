# core/watchdog/heartbeat_monitor.py

from datetime import datetime, timedelta
from threading import Lock
from typing import Optional

from config.config import (
    WEBSOCKET_HEARTBEAT_TIMEOUT
)

from core.logging_manager import LoggingManager
from core.websocket.websocket_manager import (
    WebSocketManager
)


class HeartbeatMonitor:
    """
    Monitors websocket heartbeat health.
    """

    def __init__(
        self,
        websocket_manager: WebSocketManager
    ) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.websocket_manager = websocket_manager

        self.lock = Lock()

        self.last_heartbeat_check: Optional[
            datetime
        ] = None

        self.connection_health = "UNKNOWN"

    def check_connection_health(self) -> str:
        """
        Evaluate websocket heartbeat state.

        Returns:
            str:
                HEALTHY
                STALE
                DEAD
        """

        try:

            with self.lock:

                self.last_heartbeat_check = (
                    datetime.now()
                )

                if not (
                    self.websocket_manager
                    .get_connection_status()
                ):

                    self.connection_health = "DEAD"

                    self.logger.error(
                        "Websocket connection dead"
                    )

                    return self.connection_health

                last_tick_time = (
                    self.websocket_manager
                    .get_last_tick_time()
                )

                if last_tick_time is None:

                    self.connection_health = "STALE"

                    self.logger.warning(
                        "No ticks received yet"
                    )

                    return self.connection_health

                time_since_last_tick = (
                    datetime.now() - last_tick_time
                )

                timeout_threshold = timedelta(
                    seconds=(
                        WEBSOCKET_HEARTBEAT_TIMEOUT
                    )
                )

                if (
                    time_since_last_tick >
                    timeout_threshold
                ):

                    self.connection_health = "STALE"

                    self.logger.warning(
                        "Heartbeat timeout detected"
                    )

                    return self.connection_health

                self.connection_health = "HEALTHY"

                return self.connection_health

        except Exception as error:

            self.connection_health = "DEAD"

            self.logger.error(
                f"Heartbeat check failed: {error}"
            )

            return self.connection_health

    def get_connection_health(self) -> str:
        """
        Return latest connection health state.
        """

        with self.lock:

            return self.connection_health

    def get_last_heartbeat_check(
        self
    ) -> Optional[datetime]:
        """
        Return timestamp of last heartbeat check.
        """

        with self.lock:

            return self.last_heartbeat_check

    def is_connection_healthy(self) -> bool:
        """
        Return True if connection is healthy.
        """

        with self.lock:

            return (
                self.connection_health ==
                "HEALTHY"
            )

    def reset(self) -> None:
        """
        Reset heartbeat monitor state.
        """

        with self.lock:

            self.last_heartbeat_check = None

            self.connection_health = "UNKNOWN"

            self.logger.info(
                "Heartbeat monitor reset"
            )
