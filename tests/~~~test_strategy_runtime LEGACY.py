# tests/test_strategy_runtime.py
from runtime.strategy_runtime import StrategyRuntime

from core.strategy.multifactor_strategy import MultiFactorStrategy


class MockIndicator:
    def __init__(self, value: float) -> None:

        self.value = value

    def get_value(self) -> float:

        return self.value


class MockLiquidity:
    def is_bullish(self) -> bool:

        return True

    def is_bearish(self) -> bool:

        return False


class MockCVD:
    def is_bullish(self) -> bool:

        return True

    def is_bearish(self) -> bool:

        return False


def test_strategy_runtime() -> None:

    print("\n=== STRATEGY RUNTIME TEST ===\n")

    strategy = MultiFactorStrategy(
        ema_fast=MockIndicator(110),
        ema_slow=MockIndicator(100),
        vwap=MockIndicator(100),
        awvap=MockIndicator(100),
        rvol=MockIndicator(2.0),
        vwma=MockIndicator(100),
        atr=MockIndicator(5.0),
        liquidity=MockLiquidity(),
        cvd=MockCVD(),
    )

    runtime = StrategyRuntime(strategy)

    decision = runtime.evaluate(current_price=110)

    assert decision is not None

    assert decision.score > 0

    assert decision.direction in ["LONG", "STRONG_LONG"]

    print(f"Score: {decision.score}")

    print(f"Direction: {decision.direction}")

    print(f"Confidence: {decision.confidence}")

    print(f"Reasons: {len(decision.reasons)}")

    print("\n=== TEST COMPLETE ===")
