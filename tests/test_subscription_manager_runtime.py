# tests/test_subscription_manager_runtime.py

from config.config import (
    INSTRUMENT_MASTER_PATH,
    DEFAULT_WATCHLIST_FILE
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


def test_subscription_manager_runtime() -> None:

    print(
        "\n=== SUBSCRIPTION MANAGER TEST ===\n"
    )

    # ---------------------------------
    # Instrument Manager
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

    print(
        f"Instruments Loaded: "
        f"{instrument_manager.get_total_instruments()}"
    )

    # ---------------------------------
    # Token Resolver
    # ---------------------------------

    token_resolver = (
        TokenResolver(
            instrument_manager
        )
    )

    # ---------------------------------
    # Symbol Registry
    # ---------------------------------

    registry = (
        SymbolRegistry(
            token_resolver
        )
    )

    # ---------------------------------
    # Watchlist
    # ---------------------------------

    loader = WatchlistLoader()

    symbols = loader.load(
        DEFAULT_WATCHLIST_FILE
    )

    print(
        f"Watchlist Symbols: "
        f"{len(symbols)}"
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

    first_payload = payload[0]

    assert (
        first_payload["exchangeType"]
        == 1
    )

    assert (
        len(
            first_payload["tokens"]
        )
        > 0
    )

    print(
        "\n=== TEST COMPLETE ==="
    )