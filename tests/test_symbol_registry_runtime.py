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

from utils.watchlist_loader import (
    WatchlistLoader
)


def test_symbol_registry_runtime() -> None:

    print(
        "\n=== SYMBOL REGISTRY TEST ===\n"
    )

    # -------------------------
    # Load Instrument Master
    # -------------------------

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

    # -------------------------
    # Build Resolver
    # -------------------------

    token_resolver = (
        TokenResolver(
            instrument_manager
        )
    )

    # -------------------------
    # Build Registry
    # -------------------------

    registry = (
        SymbolRegistry(
            token_resolver
        )
    )

    # -------------------------
    # Load Watchlist
    # -------------------------

    loader = WatchlistLoader()

    symbols = loader.load(
        DEFAULT_WATCHLIST_FILE
    )

    print(
        f"Watchlist Symbols: "
        f"{len(symbols)}"
    )

    # -------------------------
    # Add Symbols
    # -------------------------

    added = 0

    for symbol in symbols:

        if registry.add_symbol(symbol):

            added += 1

    print(
        f"Added Symbols: {added}"
    )

    # -------------------------
    # Generate Tokens
    # -------------------------

    tokens = (
        registry.get_subscription_tokens(
            exchange="NSE"
        )
    )

    print(
        f"Subscription Tokens: "
        f"{len(tokens)}"
    )

    print(
        tokens[:10]
    )

    assert len(tokens) > 0

    print(
        "\n=== TEST COMPLETE ==="
    )