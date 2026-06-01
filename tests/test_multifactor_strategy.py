from core.strategy.multifactor_strategy import (
    MultiFactorStrategy
)


class MockIndicator:

    def __init__(
        self,
        value: float,
        ready: bool = True
    ) -> None:

        self.value = value

        self.ready = ready

    def get_value(
        self
    ) -> float:

        return self.value

    def is_ready(
        self
    ) -> bool:

        return self.ready


class MockLiquidity:

    def __init__(
        self,
        bullish: bool
    ) -> None:

        self.bullish = bullish

    def is_bullish(
        self
    ) -> bool:

        return self.bullish

    def is_bearish(
        self
    ) -> bool:

        return not self.bullish


class MockCVD:

    def __init__(
        self,
        bullish: bool
    ) -> None:

        self.bullish = bullish

    def is_bullish(
        self
    ) -> bool:

        return self.bullish

    def is_bearish(
        self
    ) -> bool:

        return not self.bullish


def test_multifactor_strategy() -> None:

    print(
        "\n=== MULTIFACTOR STRATEGY TEST ===\n"
    )

    strategy = (
        MultiFactorStrategy(

            ema_fast=MockIndicator(
                110
            ),

            ema_slow=MockIndicator(
                100
            ),

            vwap=MockIndicator(
                100
            ),

            awvap=MockIndicator(
                100
            ),

            rvol=MockIndicator(
                2.0
            ),

            vwma=MockIndicator(
                100
            ),

            atr=MockIndicator(
                5.0
            ),

            liquidity=MockLiquidity(
                bullish=True
            ),

            cvd=MockCVD(
                bullish=True
            )
        )
    )

    decision = (
        strategy.evaluate(
            current_price=110
        )
    )

    print(
        f"Score: "
        f"{decision.score}"
    )

    print(
        f"Direction: "
        f"{decision.direction}"
    )

    print(
        f"Confidence: "
        f"{decision.confidence}"
    )

    print(
        "\nReasons:"
    )

    for reason in (
        decision.reasons
    ):

        print(
            f"  - {reason}"
        )

    assert (
        decision.score > 0
    )

    assert (
        decision.direction
        in
        [
            "LONG",
            "STRONG_LONG"
        ]
    )

    print(
        "\n=== TEST COMPLETE ==="
    )