# tests/test_instrument_updater.py
from core.instruments.instrument_updater import (
    InstrumentUpdater
)


def test_instrument_updater() -> None:

    print(
        "\n=== INSTRUMENT UPDATER TEST ===\n"
    )

    updater = InstrumentUpdater()

    assert updater.update() is True

    print(
        "Instrument master downloaded"
    )

    assert updater.validate() is True

    print(
        "Instrument master validated"
    )

    print(
        "\n=== TEST COMPLETE ==="
    )