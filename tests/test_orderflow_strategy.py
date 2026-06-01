# tests/test_orderflow_strategy.py

from datetime import datetime

from core.signals.signal import (
    Signal
)

from core.strategy.orderflow_strategy import (
    OrderFlowStrategy
)


def test_orderflow_strategy() -> None:

    print(
        "\n=== ORDERFLOW STRATEGY TEST ===\n"
    )

    strategy = (
        OrderFlowStrategy(
            name="ORDERFLOW_STRATEGY",
            symbol="RELIANCE",
            timeframe="1m"
        )
    )

    # ----------------------------------
    # BUY
    # ----------------------------------

    buy_signal = Signal(
        symbol="RELIANCE",
        timeframe="1m",
        signal_type="BUY",
        strength=1.0,
        timestamp=datetime.now()
    )

    action = (
        strategy.on_signal(
            buy_signal
        )
    )

    assert action is not None

    assert (
        action.signal_type
        == "BUY"
    )

    print(
        f"BUY Action: "
        f"{action.signal_type}"
    )

    assert (
        strategy.is_long()
    )

    # ----------------------------------
    # SELL
    # ----------------------------------

    sell_signal = Signal(
        symbol="RELIANCE",
        timeframe="1m",
        signal_type="SELL",
        strength=1.0,
        timestamp=datetime.now()
    )

    action = (
        strategy.on_signal(
            sell_signal
        )
    )

    assert action is not None

    assert (
        action.signal_type
        == "EXIT"
    )

    print(
        f"EXIT Action: "
        f"{action.signal_type}"
    )

    assert (
        strategy.is_exited()
    )

    print(
        "\n=== TEST COMPLETE ==="
    )