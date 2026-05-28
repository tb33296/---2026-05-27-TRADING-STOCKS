# tests/test_websocket_runtime.py

from core.logging_manager import LoggingManager

from core.session.session_manager import (
    SessionManager
)

from core.websocket.tick_queue import TickQueue

from core.websocket.websocket_manager import (
    WebSocketManager
)


def test_websocket_initialization() -> None:

    LoggingManager.initialize()

    session_manager = SessionManager()

    tick_queue = TickQueue(max_size=100)

    websocket_manager = WebSocketManager(
        session_manager=session_manager,
        tick_queue=tick_queue
    )

    assert websocket_manager is not None

    assert (
        websocket_manager
        .get_connection_status()
        is False
    )

    assert (
        websocket_manager
        .get_total_ticks_received()
        == 0
    )
