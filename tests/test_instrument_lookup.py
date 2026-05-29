# tests/test_instrument_lookup.py
# tests/test_instrument_lookup.py

from config.config import (
    INSTRUMENT_MASTER_PATH
)

from core.instruments.instrument_manager import (
    InstrumentManager
)


def test_lookup() -> None:

    manager = InstrumentManager(
        INSTRUMENT_MASTER_PATH
    )

    manager.load_instruments()

    for symbol in [
        "RELIANCE",
        "TCS",
        "INFY",
        "HDFCBANK"
    ]:

        instruments = (
            manager.get_instruments_by_symbol(
                symbol
            )
        )

        print(
            f"\n{symbol}"
        )

        print(
            f"Count: {len(instruments)}"
        )

        for row in instruments[:10]:

            print(
                row["exchange"],
                row["token"]
            )