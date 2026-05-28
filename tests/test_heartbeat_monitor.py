
# tests/test_heartbeat_monitor.py

from datetime import datetime, timedelta
from typing import Protocol
from typing import Optional

from core.watchdog.heartbeat_monitor import (
    HeartbeatMonitor
)

class WebSocketProtocol(Protocol):
    def get_connection_status(self) -> bool: ... 
    
    def get_last_tick_time( 
                           self ) -> Optional[datetime]: ...
    
    
class MockWebSocketManager:

    def __init__(self) -> None:

        self.connected = True

        self.last_tick_time = datetime.now()

    def get_connection_status(self) -> bool:

        return self.connected

    def get_last_tick_time(self):

        return self.last_tick_time


def test_healthy_connection() -> None:

    websocket = MockWebSocketManager()

    heartbeat = HeartbeatMonitor(websocket)

    result = heartbeat.check_connection_health()

    assert result == "HEALTHY"


def test_stale_connection() -> None:

    websocket = MockWebSocketManager()

    websocket.last_tick_time = (
        datetime.now() - timedelta(seconds=60)
    )

    heartbeat = HeartbeatMonitor(websocket)

    result = heartbeat.check_connection_health()

    assert result == "STALE"


def test_dead_connection() -> None:

    websocket = MockWebSocketManager()

    websocket.connected = False

    heartbeat = HeartbeatMonitor(websocket)

    result = heartbeat.check_connection_health()

    assert result == "DEAD"
