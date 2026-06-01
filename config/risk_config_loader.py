# config/risk_config_loader.py

import json
from pathlib import Path

from core.logging_manager import (
    LoggingManager
)


class RiskConfigLoader:
    """
    Loads risk management configuration.

    Source:
        config/risk_parameters.json
    """

    CONFIG_FILE = (
        Path("config")
        / "risk_parameters.json"
    )

    def __init__(
        self
    ) -> None:

        self.logger = (
            LoggingManager.get_logger(
                __name__
            )
        )

        self.config: dict = {}

        self.load()

    def load(
        self
    ) -> None:
        """
        Load configuration file.
        """

        try:

            with open(
                self.CONFIG_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                self.config = (
                    json.load(file)
                )

            self.logger.info(
                "Risk configuration loaded"
            )

        except Exception as error:

            self.logger.error(
                f"Failed to load risk "
                f"configuration: {error}"
            )

            self.config = {}

    def reload(
        self
    ) -> None:

        self.load()

    def get_version(
        self
    ) -> int:

        return int(
            self.config.get(
                "version",
                0
            )
        )

    def get_last_updated(
        self
    ) -> str:

        return str(
            self.config.get(
                "last_updated",
                ""
            )
        )

    def get_account_settings(
        self
    ) -> dict:

        return self.config.get(
            "account",
            {}
        )

    def get_daily_settings(
        self
    ) -> dict:

        return self.config.get(
            "daily",
            {}
        )

    def get_trade_settings(
        self
    ) -> dict:

        return self.config.get(
            "trade",
            {}
        )

    def get_position_sizing(
        self
    ) -> dict:

        return self.config.get(
            "position_sizing",
            {}
        )

    def get_partial_exit_settings(
        self
    ) -> dict:

        return self.config.get(
            "partial_exit",
            {}
        )

    def get_max_drawdown_percent(
        self
    ) -> float:

        return float(
            self.config
            .get(
                "account",
                {}
            )
            .get(
                "max_drawdown_percent",
                0.0
            )
        )

    def get_daily_loss_percent(
        self
    ) -> float:

        return float(
            self.config
            .get(
                "daily",
                {}
            )
            .get(
                "max_loss_percent",
                0.0
            )
        )

    def get_base_risk_percent(
        self
    ) -> float:

        return float(
            self.config
            .get(
                "trade",
                {}
            )
            .get(
                "base_risk_percent",
                0.0
            )
        )

    def get_max_risk_percent(
        self
    ) -> float:

        return float(
            self.config
            .get(
                "trade",
                {}
            )
            .get(
                "max_risk_percent",
                0.0
            )
        )

    def get_score_multiplier(
        self,
        key: str,
        default: float = 1.0
    ) -> float:

        return float(
            self.config
            .get(
                "position_sizing",
                {}
            )
            .get(
                key,
                default
            )
        )

    def is_partial_exit_enabled(
        self
    ) -> bool:

        return bool(
            self.config
            .get(
                "partial_exit",
                {}
            )
            .get(
                "enabled",
                False
            )
        )

    def get_partial_exit_percent(
        self
    ) -> float:

        return float(
            self.config
            .get(
                "partial_exit",
                {}
            )
            .get(
                "first_target_percent",
                0.0
            )
        )

    def get_runner_percent(
        self
    ) -> float:

        return float(
            self.config
            .get(
                "partial_exit",
                {}
            )
            .get(
                "runner_percent",
                0.0
            )
        )