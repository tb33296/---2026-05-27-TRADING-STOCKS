import time

from runtime.runtime_engine import (
    RuntimeEngine
)


def test_runtime_engine_v11() -> None:

    print(
        "\n=== RUNTIME ENGINE V1.1 TEST ===\n"
    )

    engine = RuntimeEngine()

    assert engine.start() is True

    print(
        "Runtime started"
    )

    queue = engine.get_tick_queue()

    for _ in range(20):

        print(
            f"Queue Size: "
            f"{queue.size()}"
        )

        time.sleep(1)

    print(
        f"\nTotal Ticks: "
        f"{engine.get_websocket_manager().get_total_ticks_received()}"
    )

    engine.stop()

    print(
        "\n=== TEST COMPLETE ==="
    )