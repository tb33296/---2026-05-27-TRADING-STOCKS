from runtime.indicator_runtime import IndicatorRuntime

from runtime.strategy_factory import StrategyFactory

from runtime.strategy_runtime import StrategyRuntime


def test_strategy_factory() -> None:

    print("\n=== STRATEGY FACTORY TEST ===\n")

    indicator_runtime = IndicatorRuntime()

    strategy_runtime = StrategyFactory.create(
        symbol="RELIANCE", timeframe="1m", indicator_runtime=indicator_runtime
    )

    assert isinstance(strategy_runtime, StrategyRuntime)

    total = strategy_runtime.strategy

    assert total is not None

    print("Strategy Runtime Created")

    print("\n=== TEST COMPLETE ===")
