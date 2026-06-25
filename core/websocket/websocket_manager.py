# core/websocket/websocket_manager.py

from datetime import datetime
from threading import Lock
from typing import Any, Optional
from threading import Thread

from SmartApi.smartWebSocketV2 import SmartWebSocketV2

from config.config import ENABLE_TICK_LOGGING, WEBSOCKET_SUBSCRIBE_DELAY

from core.logging_manager import LoggingManager
from core.session.session_manager import SessionManager
from core.websocket.tick_queue import TickQueue
from core.websocket.depth_queue import DepthQueue

import time

import json
from pathlib import Path


class WebSocketManager:
    """
    Handles SmartAPI websocket connection and tick ingestion.
    """

    def __init__(
        self,
        session_manager: SessionManager,
        tick_queue: TickQueue,
        depth_queue: DepthQueue,
    ) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.session_manager = session_manager

        self.tick_queue = tick_queue
        
        self.depth_queue = depth_queue

        self.websocket: Optional[SmartWebSocketV2] = None

        self.connection_thread: Optional[Thread] = None

        self.is_connected = False

        self.is_running = False

        self.connection_lock = Lock()

        self.subscribed_tokens: list[dict[str, Any]] = []

        self.total_ticks_received = 0

        self.quote_ticks_received = 0

        self.depth_ticks_received = 0

        self.last_depth_packet: Optional[dict[str, Any]] = None

        self.last_tick_time: Optional[datetime] = None
        self.token_symbol_map: dict[str, str] = {}
        
        # ----------------------------------
        # Volume Tracking
        # ----------------------------------

        self.previous_day_volume: dict[str, int] = {}


        self.raw_tick_captured = False

    def connect(self) -> bool:
        """
        Establish websocket connection.
        """

        try:
            auth_manager = self.session_manager.get_auth_manager()

            if not auth_manager.is_session_valid():
                self.logger.error("Cannot connect websocket. Session invalid.")

                return False

            feed_token = auth_manager.get_feed_token()

            if feed_token is None:
                self.logger.error("Feed token unavailable")

                return False

            profile = auth_manager.user_profile
            if profile is None:
                self.logger.error("User profile unavailable")
                return False
            client_code = profile.get("data", {}).get("clientcode")

            if not client_code:
                self.logger.error("Client code unavailable")

                return False

            jwt_token = auth_manager.jwt_token

            if jwt_token is None:
                self.logger.error("JWT token unavailable")

                return False

            smart_api = auth_manager.smart_api

            if smart_api is None:
                self.logger.error("SmartAPI instance unavailable")

                return False

            self.websocket = SmartWebSocketV2(
                auth_token=jwt_token,
                api_key=smart_api.api_key,
                client_code=client_code,
                feed_token=feed_token,
            )

            self.websocket.on_open = self.on_open

            self.websocket.on_data = self.on_data

            self.websocket.on_error = self.on_error

            self.websocket.on_close = self.on_close  # type: ignore

            self.is_running = True

            self.logger.info("Connecting websocket")

            self.connection_thread = Thread(
                target=self.websocket.connect,
                daemon=True,
                name="SmartAPI-WebSocket-Thread",
            )

            self.connection_thread.start()

            timeout = 10

            start_time = time.time()

            while not self.is_connected and (time.time() - start_time) < timeout:
                time.sleep(0.1)

            if not self.is_connected:
                self.logger.error("Websocket connection timeout")

                return False

            return True

        except Exception as error:
            self.logger.error(f"Websocket connection failed: {error}")

            return False

    def subscribe(
        self, correlation_id: str, mode: int, token_list: list[dict[str, Any]]
    ) -> bool:
        """
        Subscribe to market data tokens.
        """

        try:
            if self.websocket is None:
                self.logger.error("Websocket not initialized")

                return False

            self.websocket.subscribe(correlation_id, mode, token_list)

            self.subscribed_tokens.extend(token_list)

            time.sleep(WEBSOCKET_SUBSCRIBE_DELAY)

            self.logger.info(f"Subscribed to {len(token_list)} token groups")

            return True

        except Exception as error:
            self.logger.error(f"Subscription failed: {error}")

            return False

    def on_open(self, wsapp: Any) -> None:
        """
        Websocket open callback.
        """

        with self.connection_lock:
            self.is_connected = True

        self.logger.info("Websocket connected")

    def on_data(self, wsapp: Any, data: dict[str, Any]) -> None:
        """
        SmartAPI packet router.

        Mode 2 -> Quote Handler

        Mode 4 -> Depth Handler
        """

        try:
            self.capture_raw_tick(data)

            subscription_mode = data.get("subscription_mode")

            if subscription_mode == 2:
                self.handle_quote_tick(data)

            elif subscription_mode == 3:
                self.handle_snapquote_tick(data)

            elif subscription_mode == 4:
                self.handle_depth_tick(data)

            else:
                return

        except Exception as error:
            self.logger.error(f"Packet routing failed: {error}")

    def handle_depth_tick(self, raw_tick: dict[str, Any]) -> None:
        """
        Mode 4 Depth packet.
        """

        try:
            normalized_depth = self.normalize_depth_tick(
                raw_tick
            )

            if normalized_depth is None:
                return

            # ----------------------------------
            # Push into Depth Queue
            # ----------------------------------

            success = self.depth_queue.enqueue(
                normalized_depth
            )

            if not success:

                self.logger.warning(
                    "Depth queue overflow"
                )

                return

            self.last_depth_packet = (
                normalized_depth
            )

            self.total_ticks_received += 1

            self.depth_ticks_received += 1

            if ENABLE_TICK_LOGGING:
                self.logger.info(f"DEPTH: {normalized_depth['symbol']}")

        except Exception as error:
            self.logger.error(f"Depth processing failed: {error}")

    def handle_quote_tick(self, raw_tick: dict[str, Any]) -> None:
        """
        Mode 2 Quote packet.
        """

        try:
            normalized_tick = self.normalize_quote_tick(raw_tick)

            if normalized_tick is None:
                return

            success = self.tick_queue.enqueue(normalized_tick)

            if not success:
                self.logger.warning("Tick queue overflow")

                return

            self.total_ticks_received += 1

            self.quote_ticks_received += 1

            self.last_tick_time = datetime.now()

            if ENABLE_TICK_LOGGING:
                self.logger.info(f"QUOTE: {normalized_tick}")

        except Exception as error:
            self.logger.error(f"Quote processing failed: {error}")

    def handle_snapquote_tick(self, raw_tick: dict[str, Any]) -> None:
        """
        Mode 3 Snapshot Quote.

        Build synthetic depth packet
        from best 5 bid/ask levels.
        """

        try:
            normalized_depth = self.normalize_snapquote_depth(raw_tick)

            if normalized_depth is None:
                return

            success = self.depth_queue.enqueue(normalized_depth)

            if not success:
                self.logger.warning("Depth queue overflow")

                return

            self.depth_ticks_received += 1

        except Exception as error:
            self.logger.error(f"Snapquote processing failed: {error}")
    
    
    
    def on_error(self, *args: Any) -> None:
        """
        Websocket error callback.
        """

        self.logger.error(f"Websocket error: {args}")

    def on_close(self, *args: Any) -> None:
        """
        Websocket close callback.
        """

        with self.connection_lock:
            self.is_connected = False

        self.logger.warning("Websocket disconnected")

    def register_token_mapping(self, token: str, symbol: str) -> None:
        """
        Register token → symbol mapping.
        """
        self.token_symbol_map[str(token)] = symbol.upper()

    def register_token_mappings(self, mappings: dict[str, str]) -> None:
        """
        Register token -> symbol mappings.
        """

        self.token_symbol_map.update(mappings)

        self.logger.info(f"Registered {len(mappings)} token mappings")

    def normalize_quote_tick(
        self, raw_tick: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        """
        Normalize SmartAPI tick structure.
        this is being used for mode 2
        """

        try:
            token = str(raw_tick.get("token", ""))

            ltp = float(raw_tick.get("last_traded_price", 0)) / 100

            day_volume = int(raw_tick.get("volume_trade_for_the_day", 0))

            exchange_time = raw_tick.get("exchange_timestamp")

            symbol = self.token_symbol_map.get(token, token)

            # ----------------------------------
            # Convert cumulative day volume
            # into incremental tick volume
            # ----------------------------------

            previous_volume = self.previous_day_volume.get(symbol, day_volume)

            volume = max(0, day_volume - previous_volume)

            self.previous_day_volume[symbol] = day_volume
            
            self.logger.info(f"[VOLUME] {symbol} day={day_volume} tick={volume}")

            normalized_tick = {
                "symbol": symbol,
                "token": token,
                "ltp": ltp,
                "volume": volume,
                "timestamp": datetime.now(),
                "exchange_timestamp": exchange_time,
            }

            return normalized_tick

        except Exception as error:
            self.logger.error(f"Tick normalization failed: {error}")

            return None

    def normalize_depth_tick(
        self, raw_tick: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        """
        Normalize Mode 4 depth packet.
        """

        try:
            token = str(raw_tick.get("token", ""))

            symbol = self.token_symbol_map.get(token, token)

            normalized_depth = {
                "symbol": symbol,
                "token": token,
                "buy": raw_tick.get("depth_20_buy_data", []),
                "sell": raw_tick.get("depth_20_sell_data", []),
                "timestamp": datetime.now(),
            }

            return normalized_depth

        except Exception as error:
            self.logger.error(f"Depth normalization failed: {error}")

            return None

    def capture_raw_tick(self, raw_tick: dict[str, Any]) -> None:
        """
        Save first raw websocket packet
        for structure analysis.
        """

        try:
            if self.raw_tick_captured:
                return

            from config.config import CAPTURE_FIRST_RAW_TICK, RAW_TICK_CAPTURE_FILE

            if not CAPTURE_FIRST_RAW_TICK:
                return

            Path("logs").mkdir(parents=True, exist_ok=True)

            with open(RAW_TICK_CAPTURE_FILE, "w", encoding="utf-8") as file:
                json.dump(raw_tick, file, indent=4, default=str)

            self.raw_tick_captured = True

            self.logger.info(f"Raw tick captured -> {RAW_TICK_CAPTURE_FILE}")

        except Exception as error:
            self.logger.error(f"Raw tick capture failed: {error}")

    def normalize_snapquote_depth(
        self,
        raw_tick: dict[str, Any]
    ) -> Optional[dict[str, Any]]:

        try:

            token = str(
                raw_tick.get(
                    "token",
                    ""
                )
            )

            symbol = (
                self.token_symbol_map.get(
                    token,
                    token
                )
            )

            buy_levels = raw_tick.get(
                "best_5_buy_data",
                []
            )

            sell_levels = raw_tick.get(
                "best_5_sell_data",
                []
            )
            self.logger.info(
                f"[SNAPQUOTE_RAW] "
                f"{symbol} "
                f"buy={len(buy_levels)} "
                f"sell={len(sell_levels)} "
                f"first_buy={buy_levels[0] if buy_levels else None} "
                f"first_sell={sell_levels[0] if sell_levels else None}"
            )

            normalized_depth = {
                "symbol": symbol,
                "token": token,
                "buy": buy_levels,
                "sell": sell_levels,
                "timestamp": datetime.now(),
            }

            return normalized_depth

        except Exception as error:

            self.logger.error(
                f"Snapquote normalization failed: {error}"
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

            self.logger.info("Websocket disconnected safely")

        except Exception as error:
            self.logger.error(f"Websocket disconnect failed: {error}")

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

    def get_last_tick_time(self) -> Optional[datetime]:
        """
        Return last received tick time.
        """

        return self.last_tick_time
