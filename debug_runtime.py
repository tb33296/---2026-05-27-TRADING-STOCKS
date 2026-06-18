# python debug_runtime.py
import time

import os

from core.debug.trade_monitor import trade_monitor

from runtime.runtime_engine import RuntimeEngine
from core.logging_manager import LoggingManager

print("Starting logging manager")
LoggingManager.initialize()

print("Creating RuntimeEngine")

runtime = RuntimeEngine()
print("ENTERED_RUNTIME_START")
print("Calling start()")

result = runtime.start()

print(f"start() returned: {result}")

if not result:
    print("Runtime startup failed")
    raise SystemExit(1)

print("Runtime running")

try:
    while True:
        os.system("cls")

        print("=" * 80)
        print("INTRADAY TRADING PLATFORM")
        print("=" * 80)

        print(f"Runtime Alive : {runtime.is_alive()}")

        print()

        print("=" * 80)
        print("TRADE PIPELINE MONITOR")
        print("=" * 80)

        events = trade_monitor.get_events()

        if not events:
            print("No events yet")

        else:
            for event in events[:30]:
                print(f"[{event['category']:<18}] {event['message']}")

        print()
        print("=" * 80)

        time.sleep(2)

except KeyboardInterrupt:
    print("Closing open positions...")

    closed = runtime.shutdown_positions()

    print(f"Closed {closed} open positions")

    print("Stopping runtime")

    runtime.stop()
