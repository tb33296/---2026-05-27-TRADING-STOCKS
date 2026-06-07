# runtime/orderflow_runtime.py
from core.logging_manager import LoggingManager

from core.indicators.cvd import CVD

from core.indicators.liquidity_delta import LiquidityDelta


class OrderFlowRuntime:
    """
    Maintains tick-based orderflow indicators.

    Responsibilities:
    - update CVD
    - update Liquidity Delta
    - provide indicator lookup

    Does NOT:
    - build candles
    - execute strategies
    - execute trades
    """

    def __init__(self) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.cvd_indicators: dict[str, CVD] = {}

        self.liquidity_indicators: dict[str, LiquidityDelta] = {}

    def register_cvd(self, indicator: CVD) -> None:

        self.cvd_indicators[indicator.symbol] = indicator

    def register_liquidity(self, indicator: LiquidityDelta) -> None:

        self.liquidity_indicators[indicator.symbol] = indicator

    def process_tick(self, tick: dict) -> None:
        """
        Update tick-based indicators.
        """

        try:
            symbol = str(tick.get("symbol", ""))

            if not symbol:
                return

            price = float(tick.get("ltp", 0))

            volume = int(tick.get("volume", 0))

            cvd = self.cvd_indicators.get(symbol)

            if cvd is not None:
                cvd.update(price, volume)

            liquidity = self.liquidity_indicators.get(symbol)

            if liquidity is not None:
                depth_data = tick.get("depth", {})

                liquidity.update(depth_data)

        except Exception as error:
            self.logger.error(f"OrderFlowRuntime failed: {error}")

    def get_cvd(self, symbol: str) -> CVD | None:

        return self.cvd_indicators.get(symbol)

    def get_liquidity(self, symbol: str) -> LiquidityDelta | None:

        return self.liquidity_indicators.get(symbol)

    def clear(self) -> None:

        self.cvd_indicators.clear()

        self.liquidity_indicators.clear()

    def process_depth(self, depth_packet: dict) -> None:
        """
        Update depth-based indicators.
        """

        try:
            symbol = str(depth_packet.get("symbol", ""))

            if not symbol:
                return

            liquidity = self.liquidity_indicators.get(symbol)

            if liquidity is None:
                return

            liquidity.update(depth_packet)

        except Exception as error:
            self.logger.error(f"Depth processing failed: {error}")
