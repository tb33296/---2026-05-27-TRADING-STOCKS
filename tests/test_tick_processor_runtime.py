# tests/test_tick_processor_runtime.py

import time

from runtime.runtime_engine import (
    RuntimeEngine
)

from runtime.tick_processor import (
    TickProcessor
)


def test_tick_processor_runtime() -> None:

    print(
        "\n=== TICK PROCESSOR TEST ===\n"
    )

    # -------------------------
    # Start Runtime
    # -------------------------

    engine = RuntimeEngine()

    assert (
        engine.start()
        is True
    )

    print(
        "Runtime Started"
    )

    # -------------------------
    # Build Processor
    # -------------------------

    processor = TickProcessor(
        engine.get_tick_queue()
    )

    # -------------------------
    # Allow Tick Collection
    # -------------------------

    print(
        "\nCollecting ticks..."
    )

    time.sleep(5)

    print(
        f"Queue Size Before Processing: "
        f"{engine.get_tick_queue().size()}"
    )

    # -------------------------
    # Process Queue
    # -------------------------

    processed = (
        processor.process_all_available()
    )

    print(
        f"Processed Ticks: "
        f"{processed}"
    )

    print(
        f"Total Processed: "
        f"{processor.get_total_processed()}"
    )

    print(
        f"Tracked Tokens: "
        f"{processor.get_tracked_symbol_count()}"
    )

    print(
        f"Invalid Ticks: "
        f"{processor.get_invalid_tick_count()}"
    )

    print(
        f"Queue Size After Processing: "
        f"{engine.get_tick_queue().size()}"
    )

    # -------------------------
    # Dump Latest Ticks
    # -------------------------

    print(
        "\nLatest Tick Snapshot:\n"
    )

    latest_ticks = (
        processor.get_all_latest_ticks()
    )

    for token, tick in (
        latest_ticks.items()
    ):

        print(
            f"{token} -> {tick}"
        )

    # -------------------------
    # Validation
    # -------------------------

    assert (
        processor.get_total_processed()
        > 0
    )

    assert (
        processor.get_tracked_symbol_count()
        > 0
    )

    # -------------------------
    # Shutdown
    # -------------------------

    engine.stop()

    print(
        "\n=== TEST COMPLETE ==="
    )