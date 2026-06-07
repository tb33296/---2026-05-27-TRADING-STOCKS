# tests/test_runtime_startup.py

import time

from runtime.runtime_engine import RuntimeEngine


def test_runtime_startup():

    runtime = RuntimeEngine()

    assert runtime.start()

    time.sleep(5)

    assert runtime.is_alive()

    assert runtime.get_tick_processor() is not None

    assert runtime.get_depth_processor() is not None

    runtime.stop()