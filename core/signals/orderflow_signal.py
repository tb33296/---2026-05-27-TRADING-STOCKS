# core/signals/orderflow_signal.py

from datetime import datetime
from typing import Optional

from core.indicators.cvd import (
    CVD
)

from core.indicators.liquidity_delta import (
    LiquidityDelta
)

from core.logging_manager import (
    LoggingManager
)

from core.signals.signal import (
    Signal
)


class OrderFlowSignal:
    """
    Order Flow Signal.

    Combines:

    - Liquidity Delta
    - CVD
    """

    def __init__(
        self,
        name: str,
        liquidity_indicator: LiquidityDelta,
        cvd_indicator: CVD,
        signal_strength: float = 1.0,
        bullish_ratio: float = 0.55,
        bearish_ratio: float = 0.45
    ) -> None:

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.name = name

        self.liquidity_indicator = (
            liquidity_indicator
        )

        self.cvd_indicator = (
            cvd_indicator
        )

        self.signal_strength = (
            signal_strength
        )

        self.bullish_ratio = (
            bullish_ratio
        )

        self.bearish_ratio = (
            bearish_ratio
        )

        self.previous_cvd = None

    def evaluate(
        self
    ) -> Optional[Signal]:

        try:

            if not (
                self.liquidity_indicator
                .is_ready()
            ):
                return None

            if not (
                self.cvd_indicator
                .is_ready()
            ):
                return None

            ratio = (
                self.liquidity_indicator
                .get_ratio()
            )

            current_cvd = (
                self.cvd_indicator
                .get_cvd()
            )

            if (
                self.previous_cvd
                is None
            ):

                self.previous_cvd = (
                    current_cvd
                )

                return None

            # ----------------------
            # BUY
            # ----------------------

            if (
                ratio
                >=
                self.bullish_ratio
                and
                current_cvd
                >
                self.previous_cvd
            ):

                self.previous_cvd = (
                    current_cvd
                )

                return Signal(
                    symbol=(
                        self.cvd_indicator
                        .get_symbol()
                    ),

                    timeframe=(
                        self.cvd_indicator
                        .get_timeframe()
                    ),

                    signal_type="BUY",

                    strength=(
                        self.signal_strength
                    ),

                    timestamp=datetime.now(),

                    metadata={
                        "ratio": ratio,
                        "cvd": current_cvd,
                        "signal_name": self.name
                    }
                )

            # ----------------------
            # SELL
            # ----------------------

            if (
                ratio
                <=
                self.bearish_ratio
                and
                current_cvd
                <
                self.previous_cvd
            ):

                self.previous_cvd = (
                    current_cvd
                )

                return Signal(
                    symbol=(
                        self.cvd_indicator
                        .get_symbol()
                    ),

                    timeframe=(
                        self.cvd_indicator
                        .get_timeframe()
                    ),

                    signal_type="SELL",

                    strength=(
                        self.signal_strength
                    ),

                    timestamp=datetime.now(),

                    metadata={
                        "ratio": ratio,
                        "cvd": current_cvd,
                        "signal_name": self.name
                    }
                )

            self.previous_cvd = (
                current_cvd
            )

            return None

        except Exception as error:

            self.logger.error(
                f"OrderFlowSignal failed: "
                f"{error}"
            )

            return None