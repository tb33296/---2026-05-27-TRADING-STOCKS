# core/config/scoring_config_loader.py

import json
from pathlib import Path

from core.logging_manager import (
    LoggingManager
)


class ScoringConfigLoader:
    """
    Loads scoring weights and thresholds.

    Source:
        config/scoring_weights.json

    Responsibilities:
    - load JSON
    - cache configuration
    - provide typed accessors
    """

    CONFIG_FILE = (
        Path("config")
        / "scoring_weights.json"
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
        Load JSON configuration.
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
                "Scoring configuration loaded"
            )

        except Exception as error:

            self.logger.error(
                f"Failed to load scoring "
                f"configuration: {error}"
            )

            self.config = {}

    def reload(
        self
    ) -> None:
        """
        Reload configuration.
        """

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

    def get_weights(
        self
    ) -> dict:

        return self.config.get(
            "weights",
            {}
        )

    def get_thresholds(
        self
    ) -> dict:

        return self.config.get(
            "thresholds",
            {}
        )

    def get_position_sizing(
        self
    ) -> dict:

        return self.config.get(
            "position_sizing",
            {}
        )

    def get_minimum_conditions(
        self
    ) -> dict:

        return self.config.get(
            "minimum_conditions",
            {}
        )

    def get_weight(
        self,
        category: str,
        name: str,
        default: float = 0.0
    ) -> float:
        """
        Return single weight.

        Example:
            get_weight(
                "trend",
                "ema_bullish"
            )
        """

        try:

            return float(
                self.config
                .get(
                    "weights",
                    {}
                )
                .get(
                    category,
                    {}
                )
                .get(
                    name,
                    default
                )
            )

        except Exception:

            return default

    def get_threshold(
        self,
        name: str,
        default: float = 0.0
    ) -> float:
        """
        Return threshold.
        """

        try:

            return float(
                self.config
                .get(
                    "thresholds",
                    {}
                )
                .get(
                    name,
                    default
                )
            )

        except Exception:

            return default

    def get_position_size_rule(
        self,
        name: str,
        default: float = 0.0
    ) -> float:
        """
        Return position sizing rule.
        """

        try:

            return float(
                self.config
                .get(
                    "position_sizing",
                    {}
                )
                .get(
                    name,
                    default
                )
            )

        except Exception:

            return default