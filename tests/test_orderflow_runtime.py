from runtime.orderflow_runtime import OrderFlowRuntime

from core.indicators.cvd import CVD

from core.indicators.liquidity_delta import LiquidityDelta


def test_orderflow_runtime() -> None:

    print("\n=== ORDERFLOW RUNTIME TEST ===\n")

    runtime = OrderFlowRuntime()

    # ----------------------------------
    # Register indicators
    # ----------------------------------

    cvd = CVD(
        name="CVD",
        symbol="RELIANCE",
        timeframe="1m"
    )

    liquidity = LiquidityDelta(
        name="LIQUIDITY",
        symbol="RELIANCE",
        timeframe="1m"
    )

    runtime.register_cvd(cvd)

    runtime.register_liquidity(liquidity)

    # ----------------------------------
    # Simulated Tick Stream
    # ----------------------------------

    ticks = [

        {
            "symbol": "RELIANCE",
            "ltp": 100,
            "volume": 100
        },

        {
            "symbol": "RELIANCE",
            "ltp": 101,
            "volume": 50
        },

        {
            "symbol": "RELIANCE",
            "ltp": 102,
            "volume": 50
        },

        {
            "symbol": "RELIANCE",
            "ltp": 101,
            "volume": 20
        }

    ]

    for tick in ticks:

        runtime.process_tick(tick)

    # ----------------------------------
    # Simulated Market Depth
    # ----------------------------------

    depth_tick = {

        "symbol": "RELIANCE",

        "best_5_buy_data": [

            {"quantity": 1000},
            {"quantity": 900},
        ],

        "best_5_sell_data": [

            {"quantity": 500},
            {"quantity": 400},
        ]
    }
    liquidity.update(
    {
        "buy": [
            {"quantity": 1000},
            {"quantity": 900},
        ],
        "sell": [
            {"quantity": 500},
            {"quantity": 400},
        ],
    }
)

    print(liquidity.get_delta())
    
    
    runtime.process_tick(depth_tick)

    # ----------------------------------
    # Validation
    # ----------------------------------

    cvd_result = runtime.get_cvd("RELIANCE")

    liquidity_result = runtime.get_liquidity("RELIANCE")

    assert cvd_result is not None

    assert liquidity_result is not None

    print(f"CVD: {cvd_result.get_cvd()}")

    print(
        f"Buy Volume: "
        f"{cvd_result.get_buy_volume()}"
    )

    print(
        f"Sell Volume: "
        f"{cvd_result.get_sell_volume()}"
    )

    print(
        f"Liquidity Delta: "
        f"{liquidity_result.get_delta()}"
    )

    print(
        f"Liquidity Ratio: "
        f"{liquidity_result.get_ratio()}"
    )

    assert cvd_result.get_cvd() == 80

    assert liquidity_result.get_delta() == 1000

    assert liquidity_result.is_bullish()

    print("\n=== TEST COMPLETE ===")