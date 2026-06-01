from config.scoring_config_loader import (
    ScoringConfigLoader
)


def test_scoring_config_loader() -> None:

    print(
        "\n=== SCORING CONFIG LOADER TEST ===\n"
    )

    loader = (
        ScoringConfigLoader()
    )

    # ---------------------------------
    # Metadata
    # ---------------------------------

    print(
        f"Version: "
        f"{loader.get_version()}"
    )

    print(
        f"Last Updated: "
        f"{loader.get_last_updated()}"
    )

    assert (
        loader.get_version()
        > 0
    )

    # ---------------------------------
    # Weight Lookup
    # ---------------------------------

    ema_weight = (
        loader.get_weight(
            "trend",
            "ema_bullish"
        )
    )

    print(
        f"EMA Bullish Weight: "
        f"{ema_weight}"
    )

    assert (
        isinstance(
            ema_weight,
            float
        )
    )

    # ---------------------------------
    # Threshold Lookup
    # ---------------------------------

    long_threshold = (
        loader.get_threshold(
            "long"
        )
    )

    print(
        f"Long Threshold: "
        f"{long_threshold}"
    )

    assert (
        long_threshold
        > 0
    )

    # ---------------------------------
    # Position Sizing
    # ---------------------------------

    full_size = (
        loader.get_position_size_rule(
            "full_size_score"
        )
    )

    print(
        f"Full Size Score: "
        f"{full_size}"
    )

    assert (
        full_size
        > 0
    )

    # ---------------------------------
    # Minimum Conditions
    # ---------------------------------

    conditions = (
        loader.get_minimum_conditions()
    )

    print(
        f"Minimum Conditions: "
        f"{conditions}"
    )

    assert (
        isinstance(
            conditions,
            dict
        )
    )

    # ---------------------------------
    # Full Weight Tree
    # ---------------------------------

    weights = (
        loader.get_weights()
    )

    print(
        "\nWeight Categories:"
    )

    for category in (
        weights.keys()
    ):

        print(
            f"  {category}"
        )

    assert (
        len(weights)
        > 0
    )

    print(
        "\n=== TEST COMPLETE ==="
    )