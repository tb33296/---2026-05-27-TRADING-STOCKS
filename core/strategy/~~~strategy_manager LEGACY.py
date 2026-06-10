# core/strategy/strategy_manager.py

from threading import Lock
from typing import Optional

from core.logging_manager import LoggingManager

from core.signals.signal import Signal

from core.strategy.strategy_base import (
    StrategyBase
)


class StrategyManager:
    """
    Handles strategy orchestration.

    Responsibilities:
    - strategy registration
    - signal routing
    - strategy execution
    - action collection
    """

    def __init__(self) -> None:

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.lock = Lock()

        self.strategies: dict[
            tuple[str, str],
            dict[str, StrategyBase]
        ] = {}

    def register_strategy(
        self,
        strategy: StrategyBase
    ) -> bool:
        """
        Register strategy instance.
        """

        try:

            key = (
                strategy.get_symbol(),
                strategy.get_timeframe()
            )

            strategy_name = (
                strategy.get_name()
            )

            with self.lock:

                if key not in self.strategies:

                    self.strategies[key] = {}

                if (
                    strategy_name
                    in self.strategies[key]
                ):

                    self.logger.warning(
                        f"Strategy already "
                        f"registered: "
                        f"{strategy_name}"
                    )

                    return False

                self.strategies[key][
                    strategy_name
                ] = strategy

            self.logger.info(
                f"Registered strategy: "
                f"{strategy_name}"
            )

            return True

        except Exception as error:

            self.logger.error(
                f"Strategy registration "
                f"failed: {error}"
            )

            return False

    def process_signal(
        self,
        signal: Signal
    ) -> list[Signal]:
        """
        Route signal to strategies.

        Returns:
            Strategy action signals.
        """

        actions: list[Signal] = []

        try:

            key = (
                signal.symbol,
                signal.timeframe
            )

            with self.lock:

                strategy_group = (
                    self.strategies.get(
                        key,
                        {}
                    )
                )

                strategies = list(
                    strategy_group.values()
                )

            for strategy in strategies:

                action = strategy.on_signal(
                    signal
                )

                if action is not None:

                    actions.append(action)

            return actions

        except Exception as error:

            self.logger.error(
                f"Strategy processing "
                f"failed: {error}"
            )

            return []

    def get_strategy(
        self,
        symbol: str,
        timeframe: str,
        strategy_name: str
    ) -> Optional[StrategyBase]:
        """
        Return strategy instance.
        """

        key = (
            symbol,
            timeframe
        )

        with self.lock:

            group = self.strategies.get(
                key
            )

            if group is None:

                return None

            return group.get(
                strategy_name
            )

    def get_registered_strategies(
        self,
        symbol: str,
        timeframe: str
    ) -> list[str]:
        """
        Return registered strategies.
        """

        key = (
            symbol,
            timeframe
        )

        with self.lock:

            group = self.strategies.get(
                key,
                {}
            )

            return sorted(
                list(group.keys())
            )

    def clear(self) -> None:
        """
        Clear all strategies.
        """

        with self.lock:

            self.strategies.clear()

        self.logger.info(
            "Strategy manager cleared"
        )

    def total_strategy_count(
        self
    ) -> int:
        """
        Return total registered strategies.
        """

        total = 0

        with self.lock:

            for group in (
                self.strategies.values()
            ):

                total += len(group)

        return total

    def strategy_exists(
        self,
        symbol: str,
        timeframe: str,
        strategy_name: str
    ) -> bool:
        """
        Check whether strategy exists.
        """

        key = (
            symbol,
            timeframe
        )

        with self.lock:

            group = self.strategies.get(
                key,
                {}
            )

            return (
                strategy_name
                in group
            )

