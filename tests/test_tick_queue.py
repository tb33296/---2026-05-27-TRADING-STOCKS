
# tests/test_tick_queue.py

from core.websocket.tick_queue import TickQueue


def test_enqueue() -> None:

    queue = TickQueue(max_size=3)

    result = queue.enqueue(
        {
            "symbol": "SBIN",
            "ltp": 100.0
        }
    )

    assert result is True

    assert queue.size() == 1


def test_dequeue() -> None:

    queue = TickQueue(max_size=3)

    queue.enqueue(
        {
            "symbol": "INFY",
            "ltp": 1500.0
        }
    )

    tick = queue.dequeue()

    assert tick is not None

    assert tick["symbol"] == "INFY"

    assert queue.size() == 0


def test_queue_overflow() -> None:

    queue = TickQueue(max_size=2)

    queue.enqueue(
        {
            "symbol": "RELIANCE",
            "ltp": 2500.0
        }
    )

    queue.enqueue(
        {
            "symbol": "TCS",
            "ltp": 3500.0
        }
    )

    result = queue.enqueue(
        {
            "symbol": "HDFCBANK",
            "ltp": 1600.0
        }
    )

    assert result is False

    assert queue.get_dropped_tick_count() == 1


def test_queue_clear() -> None:

    queue = TickQueue(max_size=5)

    queue.enqueue(
        {
            "symbol": "ITC",
            "ltp": 450.0
        }
    )

    queue.clear()

    assert queue.is_empty() is True


def test_queue_utilization() -> None:

    queue = TickQueue(max_size=4)

    queue.enqueue(
        {
            "symbol": "AXISBANK",
            "ltp": 1200.0
        }
    )

    utilization = (
        queue.get_utilization_percent()
    )

    assert utilization == 25.0
