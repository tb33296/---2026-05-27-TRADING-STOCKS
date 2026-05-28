
# core/websocket/websocket_manager.py

from datetime import datetime
from threading import Lock
from typing import Any, Optional

from SmartApi.smartWebSocketV2 import SmartWebSocketV2

from config.config import (
    ENABLE_TICK_LOGGING,
    WEBSOCKET_SUBSCRIBE_DELAY
)

from core.logging_manager import LoggingManager
from core.session.session_manager import SessionManager
from core.websocket.tick_queue import TickQueue

import time


class WebSocketManager:
    """
    Handles SmartAPI websocket connection and tick ingestion.
    """

    def __init__(
        self,
        session_manager: SessionManager,
        tick_queue: TickQueue
    ) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.session_manager = session_manager

        self.tick_queue = tick_queue

        self.websocket: Optional[
            SmartWebSocketV2
        ] = None

        self.is_connected = False

        self.is_running = False

        self.connection_lock = Lock()

        self.subscribed_tokens: list[dict[str, Any]] = []

        self.total_ticks_received = 0

        self.last_tick_time: Optional[
            datetime
        ] = None

    def connect(self) -> bool:
        """
        Establish websocket connection.
        """

        try:

            auth_manager = (
                self.session_manager.get_auth_manager()
            )

            if not auth_manager.is_session_valid():

                self.logger.error(
                    "Cannot connect websocket. "
                    "Session invalid."
                )

                return False

            feed_token = (
                auth_manager.get_feed_token()
            )

            if feed_token is None:

                self.logger.error(
                    "Feed token unavailable"
                )

                return False

            profile = auth_manager.user_profile 
            if profile is None: 
                self.logger.error( "User profile unavailable" ) 
                return False 
            client_code = ( profile.get("data", {}) .get("clientcode") )

            if not client_code:

                self.logger.error(
                    "Client code unavailable"
                )

                return False

            jwt_token = auth_manager.jwt_token

            if jwt_token is None:

                self.logger.error(
                    "JWT token unavailable"
                )

                return False

            smart_api = auth_manager.smart_api

            if smart_api is None:

                self.logger.error(
                    "SmartAPI instance unavailable"
                )

                return False

            self.websocket = SmartWebSocketV2(
                auth_token=jwt_token,
                api_key=smart_api.api_key,
                client_code=client_code,
                feed_token=feed_token
            )

            self.websocket.on_open = self.on_open

            self.websocket.on_data = self.on_data

            self.websocket.on_error = self.on_error

            self.websocket.on_close = self.on_close

            self.is_running = True

            self.logger.info(
                "Connecting websocket"
            )

            self.websocket.connect()

            return True

        except Exception as error:

            self.logger.error(
                f"Websocket connection failed: {error}"
            )

            return False

    def subscribe(
        self,
        correlation_id: str,
        mode: int,
        token_list: list[dict[str, Any]]
    ) -> bool:
        """
        Subscribe to market data tokens.
        """

        try:

            if self.websocket is None:

                self.logger.error(
                    "Websocket not initialized"
                )

                return False

            self.websocket.subscribe(
                correlation_id,
                mode,
                token_list
            )

            self.subscribed_tokens.extend(
                token_list
            )

            time.sleep(
                WEBSOCKET_SUBSCRIBE_DELAY
            )

            self.logger.info(
                f"Subscribed to "
                f"{len(token_list)} token groups"
            )

            return True

        except Exception as error:

            self.logger.error(
                f"Subscription failed: {error}"
            )

            return False

    def on_open(self, wsapp: Any) -> None:
        """
        Websocket open callback.
        """

        with self.connection_lock:

            self.is_connected = True

        self.logger.info(
            "Websocket connected"
        )

    def on_data( self, 
                wsapp: Any, 
                data: dict[str, Any] ) -> None:
        """
        Tick data callback.
        """

        try:

            normalized_tick = (
                self.normalize_tick(data)
            )

            if normalized_tick is None:
                return

            success = self.tick_queue.enqueue(
                normalized_tick
            )

            if not success:

                self.logger.warning(
                    "Tick queue overflow"
                )

                return

            self.total_ticks_received += 1

            self.last_tick_time = datetime.now()

            if ENABLE_TICK_LOGGING:

                self.logger.info(
                    f"Tick: {normalized_tick}"
                )

        except Exception as error:

            self.logger.error(
                f"Tick processing failed: {error}"
            )

    def on_error( self, *args: Any ) -> None:
        """
        Websocket error callback.
        """

        self.logger.error(
            f"Websocket error: {args}"
        )

    def on_close(self, wsapp: Any) -> None:
        """
        Websocket close callback.
        """

        with self.connection_lock:

            self.is_connected = False

        self.logger.warning(
            "Websocket disconnected"
        )

    def normalize_tick(
        self,
        raw_tick: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        """
        Normalize SmartAPI tick structure.
        """

        try:

            token = str(
                raw_tick.get("token", "")
            )

            ltp = float(
                raw_tick.get("last_traded_price", 0)
            ) / 100

            volume = int(
                raw_tick.get("volume_trade_for_the_day", 0)
            )

            exchange_time = raw_tick.get(
                "exchange_timestamp"
            )

            normalized_tick = {
                "symbol": token,
                "token": token,
                "ltp": ltp,
                "volume": volume,
                "timestamp": datetime.now(),
                "exchange_timestamp": exchange_time
            }

            return normalized_tick

        except Exception as error:

            self.logger.error(
                f"Tick normalization failed: {error}"
            )

            return None

    def disconnect(self) -> None:
        """
        Disconnect websocket safely.
        """

        try:

            self.is_running = False

            if self.websocket is not None:

                self.websocket.close_connection()

            with self.connection_lock:

                self.is_connected = False

            self.logger.info(
                "Websocket disconnected safely"
            )

        except Exception as error:

            self.logger.error(
                f"Websocket disconnect failed: {error}"
            )

    def get_connection_status(self) -> bool:
        """
        Return websocket connection state.
        """

        return self.is_connected

    def get_total_ticks_received(self) -> int:
        """
        Return total tick count.
        """

        return self.total_ticks_received

    def get_last_tick_time(
        self
    ) -> Optional[datetime]:
        """
        Return last received tick time.
        """

        return self.last_tick_time
