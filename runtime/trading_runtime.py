# runtime/trading_runtime.py

# runtime/trading_runtime.py

from core.trade_management.trade_manager import TradeManager

from runtime.tick_processor import TickProcessor

from core.logging_manager import LoggingManager


class TradingRuntime:
    """
    Live trade monitoring runtime.

    Responsibilities:
    - consume processed ticks
    - build price map
    - evaluate open positions
    """
    

    def __init__(
        self, tick_processor: TickProcessor, trade_manager: TradeManager
    ) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.tick_processor = tick_processor

        self.trade_manager = trade_manager

    def process_market(self) -> int:
        """
        Process current market snapshot.

        Returns:
            number of positions closed
        """
        self.logger.info("[TRADE_RUNTIME] process_market()")
        latest_ticks = self.tick_processor.get_all_latest_ticks()

        price_map: dict[str, float] = {}

        for symbol, tick in latest_ticks.items():
            ltp = tick.get("ltp")

            if ltp is None:
                continue

            price_map[symbol] = float(ltp)

        return self.trade_manager.process_all_positions(price_map)
