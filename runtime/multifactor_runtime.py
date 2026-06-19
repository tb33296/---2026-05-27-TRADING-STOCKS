# runtime/multifactor_runtime.py

from core.logging_manager import LoggingManager

from runtime.indicator_runtime import IndicatorRuntime

from core.strategy.multifactor_strategy import MultiFactorStrategy
from core.strategy.multifactor_decision import MultiFactorDecision

from core.strategy.trade_decision_engine import TradeDecisionEngine

from core.risk.position_sizing_engine import PositionSizingEngine

from runtime.trade_pipeline import TradePipeline

from core.strategy.trade_context import TradeContext

from core.instruments.instrument_manager import InstrumentManager

from runtime.orderflow_runtime import OrderFlowRuntime


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
        orderflow_runtime: OrderFlowRuntime,
        trade_decision_engine: TradeDecisionEngine,
        position_sizing_engine: PositionSizingEngine,
        trade_pipeline: TradePipeline,
        instrument_manager: InstrumentManager,
    ) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.indicator_runtime = indicator_runtime

        self.trade_decision_engine = trade_decision_engine

        self.position_sizing_engine = position_sizing_engine

        self.trade_pipeline = trade_pipeline

        self.instrument_manager = instrument_manager

        self.orderflow_runtime = orderflow_runtime

        self.strategies: dict[
            tuple[str, str],
            MultiFactorStrategy,
        ] = {}

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
            liquidity = self.orderflow_runtime.get_liquidity(symbol)

            cvd = self.orderflow_runtime.get_cvd(symbol)

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

            self.logger.error(f"Strategy evaluation failed {symbol}: {error}")

            self.logger.error(traceback.format_exc())

            return None

    def process_trade_opportunity(
        self,
        symbol: str,
        timeframe: str,
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

        strategy = self.strategies.get((symbol, timeframe))

        liquidity = self.orderflow_runtime.get_liquidity(symbol)

        cvd = self.orderflow_runtime.get_cvd(symbol)

        if strategy is None:
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

        # ----------------------------------
        # Instrument Metadata
        # ----------------------------------

        instrument = self.instrument_manager.get_primary_instrument(symbol)

        if instrument is None:
            self.logger.warning(f"No instrument found for {symbol}")

            return None

        exchange = instrument.get("exchange", "UNKNOWN")

        segment = instrument.get("segment", "UNKNOWN")

        trade_context = TradeContext(
            symbol=symbol,
            exchange=exchange,
            segment=segment,
            score=decision.score,
            direction=decision.direction,
            confidence=decision.confidence,
            reasons=decision.reasons,
            entry_price=current_price,
            stop_loss=decision.stop_loss,
            target=decision.target,
            # ==================================
            # Metrics Snapshot
            # ==================================
            atr=strategy.atr.get_value(),
            rvol=strategy.rvol.get_value(),
            vwap=strategy.vwap.get_value(),
            awvap=strategy.awvap.get_value(),
            vwma=strategy.vwma.get_value(),
            liquidity_ratio=(liquidity.get_ratio() if liquidity else 0.0),
            liquidity_delta=(liquidity.get_delta() if liquidity else 0.0),
            cvd=(cvd.get_cvd() if cvd else 0.0),
            # ==================================
            # Feature Snapshot
            # ==================================
            trend_state=(
                "BULLISH"
                if strategy.ema_fast.get_value() > strategy.ema_slow.get_value()
                else "BEARISH"
            ),
            vwap_state=(
                "ABOVE" if current_price > strategy.vwap.get_value() else "BELOW"
            ),
            awvap_state=(
                "ABOVE" if current_price > strategy.awvap.get_value() else "BELOW"
            ),
            vwma_state=(
                "ABOVE" if current_price > strategy.vwma.get_value() else "BELOW"
            ),
            rvol_state=(
                "HIGH"
                if strategy.rvol.get_value() >= 1.5
                else ("LOW" if strategy.rvol.get_value() < 1.0 else "NORMAL")
            ),
            atr_state=("ACTIVE" if strategy.atr.get_value() > 0 else "INACTIVE"),
            liquidity_state=(
                "BULLISH"
                if liquidity and liquidity.is_bullish()
                else ("BEARISH" if liquidity and liquidity.is_bearish() else "NEUTRAL")
            ),
            
            cvd_state=(
                "BULLISH"
                if cvd and cvd.is_bullish()
                else ("BEARISH" if cvd and cvd.is_bearish() else "NEUTRAL")
            ),
        )
        self.logger.info(
            f"[TRADE_CANDIDATE] {symbol} {decision.direction} score={decision.score}"
        )
        return self.trade_pipeline.execute_trade(
            trade_context=trade_context,
            account_size=account_size,
        )
