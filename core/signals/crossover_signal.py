# core/signals/crossover_signal.py

from datetime import datetime
from typing import Optional

from core.indicators.indicator_base import IndicatorBase

from core.logging_manager import LoggingManager

from core.signals.signal import Signal


class CrossoverSignal:
    """
    Detects indicator crossover events.

    Example:
    - EMA9 crossing above EMA20
    - SMA20 crossing below SMA50
    """

    VALID_STATES = {"ABOVE", "BELOW", "NEUTRAL"}

    def __init__(
        self,
        name: str,
        fast_indicator: IndicatorBase,
        slow_indicator: IndicatorBase,
        signal_strength: float = 1.0,
        rvol_indicator: Optional[IndicatorBase] = None,
        min_rvol: float = 0.0,
    ) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.name = name

        self.fast_indicator = fast_indicator

        self.slow_indicator = slow_indicator

        self.signal_strength = signal_strength
        self.rvol_indicator = rvol_indicator

        self.min_rvol = min_rvol
        self.previous_state = "NEUTRAL"

    def evaluate(self) -> Optional[Signal]:
        """
        Evaluate crossover state.

        Returns:
            Signal on crossover event.
        """

        try:
            # ================================
            # READINESS CHECK
            # ================================

            if not (self.fast_indicator.is_ready()):
                return None

            if not (self.slow_indicator.is_ready()):
                return None

            fast_value = self.fast_indicator.get_value()
            # ================================
            # RVOL FILTER
            # ================================

            if self.rvol_indicator is not None:
                if not (self.rvol_indicator.is_ready()):
                    return None

                rvol_value = self.rvol_indicator.get_value()

                if rvol_value < self.min_rvol:
                    return None

            slow_value = self.slow_indicator.get_value()

            # ================================
            # DETERMINE CURRENT STATE
            # ================================

            current_state = self._determine_state(fast_value, slow_value)

            # ================================
            # NO STATE CHANGE
            # ================================

            if current_state == self.previous_state:
                return None

            # ================================
            # GENERATE SIGNAL
            # ================================

            signal = None

            if self.previous_state == "BELOW" and current_state == "ABOVE":
                signal = self._create_signal(
                    signal_type="BUY",
                    fast_value=fast_value,
                    slow_value=slow_value,
                    current_state=current_state,
                )

            elif self.previous_state == "ABOVE" and current_state == "BELOW":
                signal = self._create_signal(
                    signal_type="SELL",
                    fast_value=fast_value,
                    slow_value=slow_value,
                    current_state=current_state,
                )

            # ================================
            # UPDATE STATE
            # ================================

            self.previous_state = current_state

            return signal

        except Exception as error:
            self.logger.error(f"Crossover evaluation failed: {error}")

            return None

    def _determine_state(self, fast_value: float, slow_value: float) -> str:
        """
        Determine crossover state.
        """

        if fast_value > slow_value:
            return "ABOVE"

        if fast_value < slow_value:
            return "BELOW"

        return "NEUTRAL"

    def _create_signal(
        self,
        signal_type: str,
        fast_value: float,
        slow_value: float,
        current_state: str,
    ) -> Signal:
        """
        Create crossover signal.
        """

        signal = Signal(
            symbol=(self.fast_indicator.get_symbol()),
            timeframe=(self.fast_indicator.get_timeframe()),
            signal_type=signal_type,
            strength=self.signal_strength,
            timestamp=datetime.now(),
            metadata={
                "signal_name": self.name,
                "fast_indicator": (self.fast_indicator.get_name()),
                "slow_indicator": (self.slow_indicator.get_name()),
                "fast_value": fast_value,
                "slow_value": slow_value,
                "previous_state": (self.previous_state),
                "current_state": current_state,
                "rvol": (
                    self.rvol_indicator.get_value() if self.rvol_indicator else None
                ),
            },
        )

        self.logger.info(f"{self.name} generated {signal_type} signal")

        return signal

    def reset(self) -> None:
        """
        Reset crossover state.
        """

        self.previous_state = "NEUTRAL"

        self.logger.info(f"{self.name} reset")

    def get_current_state(self) -> str:
        """
        Return current crossover state.
        """

        return self.previous_state
