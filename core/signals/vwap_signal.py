# core/signals/vwap_signal.py

from datetime import datetime
from typing import Optional

from core.indicators.vwap import VWAP

from core.logging_manager import (
    LoggingManager
)

from core.market_data.candle import (
    Candle
)

from core.signals.signal import Signal


class VWAPSignal:
    """
    VWAP crossover signal.

    BUY:
        Price crosses above VWAP

    SELL:
        Price crosses below VWAP
    """

    VALID_STATES = {
        "ABOVE",
        "BELOW",
        "NEUTRAL"
    }

    def __init__(
        self,
        name: str,
        vwap_indicator: VWAP,
        signal_strength: float = 1.0
    ) -> None:

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.name = name

        self.vwap_indicator = (
            vwap_indicator
        )

        self.signal_strength = (
            signal_strength
        )

        self.previous_state = (
            "NEUTRAL"
        )

    def evaluate(
        self,
        candle: Candle
    ) -> Optional[Signal]:
        """
        Evaluate VWAP relationship.
        """

        try:

            if not (
                self.vwap_indicator
                .is_ready()
            ):

                return None

            price = candle.close

            vwap_value = (
                self.vwap_indicator
                .get_value()
            )

            current_state = (
                self._determine_state(
                    price=price,
                    vwap=vwap_value
                )
            )

            # Initialize state

            if (self.previous_state == "NEUTRAL" ):
                self.previous_state = ( current_state)

                return None
            # No state change
            if (current_state == self.previous_state):
                return None

            signal = None

            # ------------------------
            # BUY
            # ------------------------

            if (
                self.previous_state
                == "BELOW"
                and
                current_state
                == "ABOVE"
            ):

                signal = self._create_signal(
                    signal_type="BUY",
                    price=price,
                    vwap=vwap_value
                )

            # ------------------------
            # SELL
            # ------------------------

            elif (
                self.previous_state
                == "ABOVE"
                and
                current_state
                == "BELOW"
            ):

                signal = self._create_signal(
                    signal_type="SELL",
                    price=price,
                    vwap=vwap_value
                )

            self.previous_state = (
                current_state
            )

            return signal

        except Exception as error:

            self.logger.error(
                f"VWAP evaluation failed: "
                f"{error}"
            )

            return None

    def _determine_state(
        self,
        price: float,
        vwap: float
    ) -> str:
        """
        Determine price vs VWAP state.
        """

        if price > vwap:

            return "ABOVE"

        if price < vwap:

            return "BELOW"

        return "NEUTRAL"

    def _create_signal(
        self,
        signal_type: str,
        price: float,
        vwap: float
    ) -> Signal:
        """
        Create VWAP signal.
        """

        signal = Signal(
            symbol=(
                self.vwap_indicator
                .get_symbol()
            ),

            timeframe=(
                self.vwap_indicator
                .get_timeframe()
            ),

            signal_type=signal_type,

            strength=self.signal_strength,

            timestamp=datetime.now(),

            metadata={
                "signal_name": self.name,

                "price": price,

                "vwap": vwap,

                "state": (
                    self.previous_state
                )
            }
        )

        self.logger.info(
            f"{self.name} generated "
            f"{signal_type} signal"
        )

        return signal

    def reset(
        self
    ) -> None:

        self.previous_state = (
            "NEUTRAL"
        )

    def get_current_state(
        self
    ) -> str:

        return self.previous_state