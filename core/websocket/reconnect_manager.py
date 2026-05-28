
# core/websocket/reconnect_manager.py

from datetime import datetime
from threading import Lock
from typing import Optional

from config.config import (
    MAX_WEBSOCKET_RETRIES,
    WEBSOCKET_RECONNECT_DELAY
)

from core.logging_manager import LoggingManager

import time


class ReconnectManager:
    """
    Handles websocket reconnect state and retry control.
    """

    def __init__(self) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.lock = Lock()

        self.reconnect_attempts = 0

        self.last_reconnect_time: Optional[
            datetime
        ] = None

        self.is_reconnecting = False

        self.connection_state = "DISCONNECTED"

    def can_reconnect(self) -> bool:
        """
        Check whether reconnect is allowed.
        """

        with self.lock:

            return (
                self.reconnect_attempts <
                MAX_WEBSOCKET_RETRIES
            )

    def start_reconnect(self) -> bool:
        """
        Begin reconnect process.
        """

        with self.lock:

            if self.is_reconnecting:

                self.logger.warning(
                    "Reconnect already in progress"
                )

                return False

            if not self.can_reconnect():

                self.connection_state = "FAILED"

                self.logger.error(
                    "Maximum reconnect attempts reached"
                )

                return False

            self.is_reconnecting = True

            self.reconnect_attempts += 1

            self.last_reconnect_time = datetime.now()

            self.connection_state = "RECONNECTING"

            self.logger.warning(
                f"Reconnect attempt "
                f"{self.reconnect_attempts}"
            )

            return True

    def wait_before_retry(self) -> None:
        """
        Wait before reconnect retry.
        """

        self.logger.info(
            f"Waiting "
            f"{WEBSOCKET_RECONNECT_DELAY} "
            f"seconds before retry"
        )

        time.sleep(
            WEBSOCKET_RECONNECT_DELAY
        )

    def reconnect_successful(self) -> None:
        """
        Mark reconnect as successful.
        """

        with self.lock:

            self.is_reconnecting = False

            self.reconnect_attempts = 0

            self.connection_state = "CONNECTED"

            self.logger.info(
                "Reconnect successful"
            )

    def reconnect_failed(self) -> None:
        """
        Mark reconnect attempt as failed.
        """

        with self.lock:

            self.is_reconnecting = False

            self.connection_state = "DISCONNECTED"

            self.logger.warning(
                "Reconnect failed"
            )

    def reset(self) -> None:
        """
        Reset reconnect manager state.
        """

        with self.lock:

            self.reconnect_attempts = 0

            self.last_reconnect_time = None

            self.is_reconnecting = False

            self.connection_state = "DISCONNECTED"

            self.logger.info(
                "Reconnect manager reset"
            )

    def get_reconnect_attempts(self) -> int:
        """
        Return reconnect attempt count.
        """

        with self.lock:

            return self.reconnect_attempts

    def get_connection_state(self) -> str:
        """
        Return current connection state.
        """

        with self.lock:

            return self.connection_state

    def get_last_reconnect_time(
        self
    ) -> Optional[datetime]:
        """
        Return last reconnect timestamp.
        """

        with self.lock:

            return self.last_reconnect_time

    def is_reconnect_active(self) -> bool:
        """
        Return reconnect activity status.
        """

        with self.lock:

            return self.is_reconnecting

