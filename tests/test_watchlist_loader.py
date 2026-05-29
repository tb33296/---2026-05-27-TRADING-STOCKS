from config.config import (
    DEFAULT_WATCHLIST_FILE
)

from utils.watchlist_loader import WatchlistLoader


def test_watchlist_loader() -> None:

    loader = WatchlistLoader()

    symbols = loader.load(
        DEFAULT_WATCHLIST_FILE
    )

    print(
        f"Loaded Symbols: "
        f"{len(symbols)}"
    )

    print(
        symbols[:10]
    )

    assert len(symbols) > 0