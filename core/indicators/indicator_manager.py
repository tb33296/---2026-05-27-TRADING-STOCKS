# core/indicators/indicator_manager.py

from threading import Lock
from typing import Optional

from core.indicators.indicator_base import (
    IndicatorBase
)

from core.logging_manager import LoggingManager

from core.market_data.candle import Candle


class IndicatorManager:
    """
    Handles indicator orchestration.

    Responsibilities:
    - indicator registration
    - candle routing
    - indicator updates
    - indicator lookup
    """

    def __init__(self) -> None:

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.lock = Lock()

        self.indicators: dict[
            tuple[str, str],
            dict[str, IndicatorBase]
        ] = {}

    def register_indicator(
        self,
        indicator: IndicatorBase
    ) -> bool:
        """
        Register indicator instance.
        """

        try:

            key = (
                indicator.get_symbol(),
                indicator.get_timeframe()
            )

            indicator_name = (
                indicator.get_name()
            )

            with self.lock:

                if key not in self.indicators:

                    self.indicators[key] = {}

                if (
                    indicator_name
                    in self.indicators[key]
                ):

                    self.logger.warning(
                        f"Indicator already "
                        f"registered: "
                        f"{indicator_name}"
                    )

                    return False

                self.indicators[key][
                    indicator_name
                ] = indicator

            self.logger.info(
                f"Registered indicator: "
                f"{indicator_name}"
            )

            return True

        except Exception as error:

            self.logger.error(
                f"Indicator registration "
                f"failed: {error}"
            )

            return False

    def update_indicators(
        self,
        candle: Candle
    ) -> None:
        """
        Update indicators using closed candle.
        """

        try:

            key = (
                candle.symbol,
                candle.timeframe
            )

            with self.lock:

                indicator_group = (
                    self.indicators.get(
                        key,
                        {}
                    )
                )

                indicators = list(
                    indicator_group.values()
                )

            for indicator in indicators:

                indicator.update(candle)

        except Exception as error:

            self.logger.error(
                f"Indicator update failed: "
                f"{error}"
            )

    def get_indicator(
        self,
        symbol: str,
        timeframe: str,
        indicator_name: str
    ) -> Optional[IndicatorBase]:
        """
        Return indicator instance.
        """

        key = (
            symbol,
            timeframe
        )

        with self.lock:

            group = self.indicators.get(
                key
            )

            if group is None:

                return None

            return group.get(
                indicator_name
            )

    def get_indicator_value(
        self,
        symbol: str,
        timeframe: str,
        indicator_name: str
    ) -> Optional[float]:
        """
        Return indicator value.
        """

        indicator = self.get_indicator(
            symbol=symbol,
            timeframe=timeframe,
            indicator_name=indicator_name
        )

        if indicator is None:

            return None

        return indicator.get_value()

    def get_registered_indicators(
        self,
        symbol: str,
        timeframe: str
    ) -> list[str]:
        """
        Return registered indicator names.
        """

        key = (
            symbol,
            timeframe
        )

        with self.lock:

            group = self.indicators.get(
                key,
                {}
            )

            return sorted(
                list(group.keys())
            )

    def clear(self) -> None:
        """
        Clear all indicators.
        """

        with self.lock:

            self.indicators.clear()

            self.logger.info(
                "Indicator manager cleared"
            )

    def total_indicator_count(
        self
    ) -> int:
        """
        Return total registered indicators.
        """

        total = 0

        with self.lock:

            for group in (
                self.indicators.values()
            ):

                total += len(group)

        return total
