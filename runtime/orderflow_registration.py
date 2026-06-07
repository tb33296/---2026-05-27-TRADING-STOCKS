# runtime/orderflow_registration.py

from core.indicators.cvd import CVD
from core.indicators.liquidity_delta import LiquidityDelta

from runtime.orderflow_runtime import OrderFlowRuntime

from core.instruments.symbol_registry import SymbolRegistry


class OrderFlowRegistration:
    """
    Creates and registers orderflow indicators.

    Responsibilities:
    - CVD registration
    - Liquidity Delta registration
    """

    def __init__(
        self,
        symbol_registry: SymbolRegistry,
        orderflow_runtime: OrderFlowRuntime,
    ) -> None:

        self.symbol_registry = symbol_registry

        self.orderflow_runtime = orderflow_runtime

    def register_all(self) -> int:
        """
        Register all orderflow indicators.

        Returns:
            Total indicators registered.
        """

        count = 0

        symbols = self.symbol_registry.get_all_symbols()

        for symbol in symbols:

            cvd = CVD(
                name="CVD",
                symbol=symbol,
                timeframe="TICK",
            )

            self.orderflow_runtime.register_cvd(cvd)

            count += 1

            liquidity = LiquidityDelta(
                name="LIQUIDITY_DELTA",
                symbol=symbol,
                timeframe="DEPTH",
            )

            self.orderflow_runtime.register_liquidity(
                liquidity
            )

            count += 1

        return count