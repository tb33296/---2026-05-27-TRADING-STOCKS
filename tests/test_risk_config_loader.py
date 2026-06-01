from config.risk_config_loader import (
    RiskConfigLoader
)


def test_risk_config_loader() -> None:

    print(
        "\n=== RISK CONFIG LOADER TEST ===\n"
    )

    loader = (
        RiskConfigLoader()
    )

    print(
        f"Version: "
        f"{loader.get_version()}"
    )

    print(
        f"Last Updated: "
        f"{loader.get_last_updated()}"
    )

    print(
        f"Max Drawdown: "
        f"{loader.get_max_drawdown_percent()}%"
    )

    print(
        f"Daily Loss Limit: "
        f"{loader.get_daily_loss_percent()}%"
    )

    print(
        f"Base Risk: "
        f"{loader.get_base_risk_percent()}%"
    )

    print(
        f"Max Risk: "
        f"{loader.get_max_risk_percent()}%"
    )

    print(
        f"Partial Exit Enabled: "
        f"{loader.is_partial_exit_enabled()}"
    )

    print(
        f"Partial Exit %: "
        f"{loader.get_partial_exit_percent()}"
    )

    print(
        f"Runner %: "
        f"{loader.get_runner_percent()}"
    )

    assert (
        loader.get_version()
        > 0
    )

    assert (
        loader.get_max_drawdown_percent()
        > 0
    )

    assert (
        loader.get_daily_loss_percent()
        > 0
    )

    assert (
        loader.get_base_risk_percent()
        > 0
    )

    assert (
        loader.get_max_risk_percent()
        > 0
    )

    print(
        "\n=== TEST COMPLETE ==="
    )