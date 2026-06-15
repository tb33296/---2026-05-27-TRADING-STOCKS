# runtime/multifactor_runtime.py

from core.logging_manager import LoggingManager

from runtime.indicator_runtime import IndicatorRuntime

from core.strategy.multifactor_strategy import MultiFactorStrategy
from core.strategy.multifactor_decision import MultiFactorDecision

from core.strategy.trade_decision_engine import TradeDecisionEngine

from core.risk.position_sizing_engine import PositionSizingEngine

from runtime.trade_pipeline import TradePipeline

from core.strategy.trade_context import TradeContext


class MultiFactorRuntime:
    """
    Runtime bridge between:

        IndicatorRuntime
            ↓
        MultiFactorStrategy
            ↓
        TradingEngine / Trade Pipeline

    Responsibilities:
    - own strategy instances
    - evaluate strategies
    - submit trade candidates
    """

    def __init__(
        self,
        indicator_runtime: IndicatorRuntime,
        trade_decision_engine: TradeDecisionEngine,
        position_sizing_engine: PositionSizingEngine,
        trade_pipeline: TradePipeline,
    ) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.indicator_runtime = indicator_runtime

        self.trade_decision_engine = trade_decision_engine

        self.position_sizing_engine = position_sizing_engine

        self.trade_pipeline = trade_pipeline

        self.strategies: dict[tuple[str, str], MultiFactorStrategy] = {}

    # --------------------------------------------------
    # Strategy Registration
    # --------------------------------------------------

    def register_strategy(
        self,
        symbol: str,
        timeframe: str,
    ) -> bool:
        """
        Build MultiFactorStrategy from
        registered indicators.
        """

        try:
            ema_fast = self.indicator_runtime.get_indicator(
                symbol, timeframe, "EMA_FAST"
            )

            ema_slow = self.indicator_runtime.get_indicator(
                symbol, timeframe, "EMA_SLOW"
            )

            vwap = self.indicator_runtime.get_indicator(symbol, timeframe, "VWAP")

            awvap = self.indicator_runtime.get_indicator(symbol, timeframe, "AWVAP")

            rvol = self.indicator_runtime.get_indicator(symbol, timeframe, "RVOL")

            vwma = self.indicator_runtime.get_indicator(symbol, timeframe, "VWMA")

            atr = self.indicator_runtime.get_indicator(symbol, timeframe, "ATR")

            # ! Removing the next line and replacing them with None Temporarily.
            # liquidity = self.indicator_runtime.get_indicator(
            #     symbol, timeframe, "LIQUIDITY"
            # )

            # cvd = self.indicator_runtime.get_indicator(symbol, timeframe, "CVD")
            liquidity = None
            cvd = None
            strategy = MultiFactorStrategy(
                ema_fast=ema_fast,
                ema_slow=ema_slow,
                vwap=vwap,
                awvap=awvap,
                rvol=rvol,
                vwma=vwma,
                atr=atr,
                liquidity=liquidity,
                cvd=cvd,
            )

            self.strategies[(symbol, timeframe)] = strategy

            self.logger.info(f"Strategy registered {symbol} {timeframe}")

            return True

        except Exception as error:
            self.logger.error(
                f"Strategy registration failed {symbol} {timeframe}: {error}"
            )

            return False

    # --------------------------------------------------
    # Evaluation
    # --------------------------------------------------

    def evaluate(
        self,
        symbol: str,
        timeframe: str,
        current_price: float,
    ) -> MultiFactorDecision | None:
        """
        Evaluate strategy for a symbol.
        """

        strategy = self.strategies.get((symbol, timeframe))

        if strategy is None:
            self.logger.warning(f"No strategy registered {symbol} {timeframe}")

            return None

        try:
            decision = strategy.evaluate(current_price)

            return decision

        except Exception as error:
            import traceback

            self.logger.error(
                f"Strategy evaluation failed {symbol}: {error}"
            )

            self.logger.error(
                traceback.format_exc()
            )

            return None

    def process_trade_opportunity(
        self,
        symbol: str,
        timeframe: str,
        segment: str,
        current_price: float,
        account_size: float,
    ):
        """
        Evaluate strategy and submit
        trade candidate to pipeline.
        """

        decision = self.evaluate(
            symbol=symbol,
            timeframe=timeframe,
            current_price=current_price,
        )

        if decision is None:
            return None

        self.logger.info(
            f"[STRATEGY] "
            f"{symbol} "
            f"{timeframe} "
            f"{decision.direction} "
            f"score={decision.score}"
        )

        if decision.direction == "NO_TRADE":
            return None

        trade_context = TradeContext(
            symbol=symbol,
            segment=segment,
            score=decision.score,
            direction=decision.direction,
            confidence=decision.confidence,
            reasons=decision.reasons,
            entry_price=current_price,
            stop_loss=decision.stop_loss,
            target=decision.target,
        )
        self.logger.info(
            f"[TRADE_CANDIDATE] {symbol} {decision.direction} score={decision.score}"
        )
        return self.trade_pipeline.execute_trade(
            trade_context=trade_context,
            account_size=account_size,
        )
