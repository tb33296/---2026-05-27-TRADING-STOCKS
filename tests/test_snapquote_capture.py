# tests/test_snapquote_capture.py
import time

from runtime.runtime_engine import RuntimeEngine


def test_snapquote_capture() -> None:

    print(
        "\n=== SNAPQUOTE CAPTURE TEST ===\n"
    )

    engine = RuntimeEngine()

    assert engine.start()

    print(
        "\nWaiting for first packet..."
    )

    time.sleep(30)

    engine.stop()

    print(
        "\nCheck:"
    )

    print(
        "logs/raw_tick_capture.json"
    )

    print(
        "\n=== TEST COMPLETE ==="
    )