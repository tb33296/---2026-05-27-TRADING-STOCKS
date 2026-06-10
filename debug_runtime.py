import time

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
        print(
            f"is_alive={runtime.is_alive()}"
        )
        time.sleep(5)

except KeyboardInterrupt:

    print("Stopping runtime")

    runtime.stop()