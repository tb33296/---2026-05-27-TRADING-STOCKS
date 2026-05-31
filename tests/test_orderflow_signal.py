from core.indicators.cvd import (
    CVD
)

from core.indicators.liquidity_delta import (
    LiquidityDelta
)

from core.signals.orderflow_signal import (
    OrderFlowSignal
)


def test_orderflow_signal() -> None:

    print(
        "\n=== ORDER FLOW SIGNAL TEST ===\n"
    )

    liquidity = LiquidityDelta(
        name="LIQUIDITY",
        symbol="RELIANCE",
        timeframe="1m"
    )

    cvd = CVD(
        name="CVD",
        symbol="RELIANCE",
        timeframe="1m"
    )

    signal_engine = OrderFlowSignal(
        name="ORDERFLOW",
        liquidity_indicator=liquidity,
        cvd_indicator=cvd
    )

    # ----------------------------------
    # Strong Bullish Order Book
    # ----------------------------------

    liquidity.update(
        {
            "buy": [
                {"quantity": 1000},
                {"quantity": 800}
            ],
            "sell": [
                {"quantity": 200},
                {"quantity": 100}
            ]
        }
    )

    print(
        f"Liquidity Ratio = "
        f"{liquidity.get_ratio()}"
    )

    # ----------------------------------
    # Tick #1
    # Initializes CVD
    # ----------------------------------

    cvd.update(
        102,
        100
    )

    signal = (
        signal_engine.evaluate()
    )

    assert signal is None

    print(
        f"CVD={cvd.get_cvd()} "
        f"(Initialization)"
    )

    # ----------------------------------
    # Tick #2
    # Initializes previous_cvd
    # ----------------------------------

    cvd.update(
        103,
        200
    )

    signal = (
        signal_engine.evaluate()
    )

    assert signal is None

    print(
        f"CVD={cvd.get_cvd()} "
        f"(Baseline Established)"
    )

    # ----------------------------------
    # Tick #3
    # Actual BUY signal
    # ----------------------------------

    cvd.update(
        104,
        100
    )

    signal = (
        signal_engine.evaluate()
    )

    assert signal is not None

    print(
        f"Signal: "
        f"{signal.signal_type}"
    )

    assert (
        signal.signal_type
        == "BUY"
    )

    print(
        f"CVD={cvd.get_cvd()}"
    )

    print(
        "\n=== TEST COMPLETE ==="
    )