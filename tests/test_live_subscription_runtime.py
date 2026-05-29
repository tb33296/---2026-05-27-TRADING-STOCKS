# tests/test_live_subscription_runtime.py

import time

from config.config import (
    INSTRUMENT_MASTER_PATH,
    DEFAULT_WATCHLIST_FILE,
    MAX_TICK_QUEUE_SIZE
)

from core.auth.auth_manager import (
    AuthManager
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


def test_live_subscription_runtime() -> None:

    print(
        "\n=== LIVE SUBSCRIPTION TEST ===\n"
    )

    # ---------------------------------
    # Session Layer
    # ---------------------------------

    session_manager = SessionManager()
    
    assert (
        session_manager.start_session()
        is True
    )
    print(
        f"Session Alive: "
        f"{session_manager.is_session_alive()}"
        )
    # ---------------------------------
    # Tick Queue
    # ---------------------------------

    tick_queue = TickQueue(
        MAX_TICK_QUEUE_SIZE
    )

    # ---------------------------------
    # WebSocket
    # ---------------------------------

    websocket_manager = (
        WebSocketManager(
            session_manager,
            tick_queue
        )
    )

    assert (
        websocket_manager.connect()
        is True
    )

    print(
        "WebSocket Connected"
    )

    # ---------------------------------
    # Instrument Layer
    # ---------------------------------

    instrument_manager = (
        InstrumentManager(
            INSTRUMENT_MASTER_PATH
        )
    )

    assert (
        instrument_manager
        .load_instruments()
        is True
    )

    token_resolver = (
        TokenResolver(
            instrument_manager
        )
    )

    # ---------------------------------
    # Registry
    # ---------------------------------

    registry = (
        SymbolRegistry(
            token_resolver
        )
    )

    loader = WatchlistLoader()

    symbols = loader.load(
        DEFAULT_WATCHLIST_FILE
    )

    for symbol in symbols:

        registry.add_symbol(
            symbol
        )

    # ---------------------------------
    # Subscription Manager
    # ---------------------------------

    subscription_manager = (
        SubscriptionManager(
            registry
        )
    )

    payload = (
        subscription_manager
        .build_subscription_payload(
            exchange="NSE"
        )
    )

    assert payload is not None

    print(
        "\nPayload:"
    )

    print(payload)

    # ---------------------------------
    # Subscribe
    # ---------------------------------

    assert (
        websocket_manager.subscribe(
            correlation_id="runtime_test",
            mode=1,
            token_list=payload
        )
        is True
    )

    print(
        "\nSubscription Sent"
    )

    # ---------------------------------
    # Wait For Live Ticks
    # ---------------------------------

    print(
        "\nCollecting ticks..."
    )

    for _ in range(20):

        print(
            f"Queue Size: "
            f"{tick_queue.size()}"
        )

        time.sleep(1)

    print(
        f"\nTotal Ticks Received: "
        f"{websocket_manager.get_total_ticks_received()}"
    )

    print(
        f"Final Queue Size: "
        f"{tick_queue.size()}"
    )

    websocket_manager.disconnect()

    assert (
        websocket_manager
        .get_total_ticks_received()
        > 0
    )

    print(
        "\n=== TEST COMPLETE ==="
    )