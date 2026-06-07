# tests/test_live_candle_builder.py
import time

from runtime.runtime_engine import (
    RuntimeEngine
)

from runtime.tick_processor import (
    TickProcessor
)

from runtime.candle_runtime import (
    CandleRuntime
)


def test_live_candle_builder() -> None:

    print(
        "\n=== LIVE CANDLE TEST ===\n"
    )

    engine = RuntimeEngine()

    assert engine.start()

    time.sleep(5)

    processor = TickProcessor(
        engine.get_tick_queue()
    )

    processor.process_all_available()

    candle_runtime = CandleRuntime(
        processor
    )

    candle_runtime.process_ticks()

    symbols = [
        "RELIANCE",
        "TCS",
        "INFY",
        "HDFCBANK"
    ]

    for symbol in symbols:

        candle = (
            candle_runtime
            .get_current_candle(
                symbol
            )
        )

        print()

        print(symbol)

        print(candle)

    engine.stop()

    print(
        "\n=== TEST COMPLETE ==="
    )