
# tests/test_live_market_feed.py

import time

from core.logging_manager import LoggingManager

from core.session.session_manager import (
    SessionManager
)

from core.websocket.tick_queue import (
    TickQueue
)

from core.websocket.websocket_manager import (
    WebSocketManager
)

from core.websocket.subscription_manager import (
    SubscriptionManager
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

from core.watchdog.heartbeat_monitor import (
    HeartbeatMonitor
)


def test_live_market_feed() -> None:

    LoggingManager.initialize()

    print("\n=== STARTING LIVE FEED TEST ===\n")

    # ============================================
    # Session
    # ============================================

    session_manager = SessionManager()

    assert (
        session_manager.start_session()
        is True
    )

    print("Session started successfully")

    # ============================================
    # Queue
    # ============================================

    tick_queue = TickQueue(max_size=1000)

    # ============================================
    # Websocket
    # ============================================

    websocket_manager = WebSocketManager(
        session_manager=session_manager,
        tick_queue=tick_queue
    )

    connected = websocket_manager.connect()

    assert connected is True

    print("Websocket connection initiated")

    # ============================================
    # Heartbeat
    # ============================================

    heartbeat = HeartbeatMonitor(
        websocket_manager
    )

    # ============================================
    # Temporary Registry Setup
    # ============================================

    instrument_manager = InstrumentManager(
        instrument_file=(
            "data/instruments/"
            "OpenAPIScripMaster.json"
        )
    )

    token_resolver = TokenResolver(
        instrument_manager
    )

    symbol_registry = SymbolRegistry(
        token_resolver
    )

    subscription_manager = (
        SubscriptionManager(
            symbol_registry
        )
    )

    # ============================================
    # TEMPORARY DIRECT SUBSCRIPTION
    # ============================================

    subscription_payload = [
        {
            "exchangeType": 1,
            "tokens": ["3045"]
        }
    ]

    time.sleep(5)

    subscribed = websocket_manager.subscribe(
        correlation_id="live_test",
        mode=1,
        token_list=subscription_payload
    )

    assert subscribed is True

    print("Subscription successful")

    # ============================================
    # Tick Collection Window
    # ============================================

    print("\nCollecting ticks...\n")

    start_time = time.time()

    while (
        time.time() - start_time
    ) < 30:

        queue_size = tick_queue.size()

        heartbeat_status = (
            heartbeat.check_connection_health()
        )

        print(
            f"Queue Size: {queue_size} | "
            f"Heartbeat: {heartbeat_status}"
        )

        tick = tick_queue.dequeue()

        if tick is not None:

            print(f"Tick: {tick}")

        time.sleep(1)

    # ============================================
    # Final Validation
    # ============================================

    assert (
        websocket_manager
        .get_total_ticks_received()
        > 0
    )

    print(
        "\nTotal Ticks Received:",
        websocket_manager
        .get_total_ticks_received()
    )

    print(
        "Final Queue Size:",
        tick_queue.size()
    )

    print(
        "Heartbeat Status:",
        heartbeat.get_connection_health()
    )

    # ============================================
    # Cleanup
    # ============================================

    websocket_manager.disconnect()

    session_manager.logout()

    print("\n=== LIVE FEED TEST COMPLETE ===\n")

