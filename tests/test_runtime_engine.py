# tests/test_runtime_engine.py

import time

from runtime.runtime_engine import (
    RuntimeEngine
)


def test_runtime_engine() -> None:
    """
    Runtime engine startup test.
    """

    print(
        "\n=== STARTING RUNTIME ENGINE TEST ===\n"
    )

    engine = RuntimeEngine()

    assert engine.start() is True

    print(
        "Runtime engine started successfully"
    )

    assert (
        engine.is_running
        is True
    )

    print(
        "\nCollecting ticks...\n"
    )

    for _ in range(10):

        queue_size = 0

        if engine.tick_queue is not None:

            queue_size = (
                engine.tick_queue.size()
            )

        print(
            f"Queue Size: {queue_size}"
        )

        time.sleep(1)

    engine.stop()

    assert (
        engine.is_running
        is False
    )

    print(
        "\n=== RUNTIME ENGINE TEST COMPLETE ==="
    )