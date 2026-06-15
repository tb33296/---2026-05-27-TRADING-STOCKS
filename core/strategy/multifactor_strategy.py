# core/strategy/multifactor_strategy.py
from config.scoring_config_loader import ScoringConfigLoader

from core.strategy.multifactor_decision import MultiFactorDecision

from config.config import ATR_STOP_MULTIPLIER, RISK_REWARD_RATIO

from core.logging_manager import LoggingManager


class MultiFactorStrategy:
    """
    Multi-factor scoring engine.

    Produces:

    LONG
    SHORT
    NO_TRADE

    based on weighted indicator scores.
    """

    def __init__(
        self, ema_fast, ema_slow, vwap, awvap, rvol, vwma, atr, liquidity, cvd
    ) -> None:

        self.loader = ScoringConfigLoader()

        self.logger = LoggingManager.get_logger(__name__)

        self.ema_fast = ema_fast

        self.ema_slow = ema_slow

        self.vwap = vwap

        self.awvap = awvap

        self.rvol = rvol

        self.vwma = vwma

        self.atr = atr

        self.liquidity = liquidity

        self.cvd = cvd

    def evaluate(self, current_price: float) -> MultiFactorDecision:

        score = 0.0

        reasons: list[str] = []

        # ===================================
        # TREND
        # ===================================

        if self.ema_fast.get_value() > self.ema_slow.get_value():
            score += self.loader.get_weight("trend", "ema_bullish")

            reasons.append("EMA Bullish")

        else:
            score += self.loader.get_weight("trend", "ema_bearish")

            reasons.append("EMA Bearish")

        # ===================================
        # VWAP
        # ===================================

        if current_price > self.vwap.get_value():
            score += self.loader.get_weight("fair_value", "vwap_bullish")

            reasons.append("Above VWAP")

        else:
            score += self.loader.get_weight("fair_value", "vwap_bearish")

            reasons.append("Below VWAP")

        # ===================================
        # AWVAP
        # ===================================

        if current_price > self.awvap.get_value():
            score += self.loader.get_weight("fair_value", "awvap_bullish")

            reasons.append("Above AWVAP")

        else:
            score += self.loader.get_weight("fair_value", "awvap_bearish")

            reasons.append("Below AWVAP")

        # ===================================
        # RVOL
        # ===================================

        rvol_value = self.rvol.get_value()

        if rvol_value >= 1.5:
            score += self.loader.get_weight("volume", "rvol_bullish")

            reasons.append(f"RVOL={rvol_value}")

        elif rvol_value < 1.0:
            score += self.loader.get_weight("volume", "rvol_bearish")

            reasons.append(f"Weak RVOL={rvol_value}")

        # ===================================
        # VWMA
        # ===================================

        if current_price > self.vwma.get_value():
            score += self.loader.get_weight("volume", "vwma_bullish")

            reasons.append("Above VWMA")

        else:
            score += self.loader.get_weight("volume", "vwma_bearish")

            reasons.append("Below VWMA")

        # ===================================
        # ATR
        # ===================================

        if self.atr.get_value() > 0:
            score += self.loader.get_weight("volatility", "atr_active")

            reasons.append("ATR Active")

        # ===================================
        # LIQUIDITY
        # ===================================
        #! Removing the CVD and Liquidity and replacing them with None Temporarily.
        # if self.liquidity.is_bullish():
        #     score += self.loader.get_weight("orderflow", "liquidity_bullish")

        #     reasons.append("Liquidity Bullish")

        # elif self.liquidity.is_bearish():
        #     score += self.loader.get_weight("orderflow", "liquidity_bearish")

        #     reasons.append("Liquidity Bearish")
        if self.liquidity is not None:
            if self.liquidity.is_bullish():
                score += self.loader.get_weight("orderflow", "liquidity_bullish")

                reasons.append("Liquidity Bullish")

            elif self.liquidity.is_bearish():
                score += self.loader.get_weight("orderflow", "liquidity_bearish")

                reasons.append("Liquidity Bearish")
        # ===================================
        # CVD
        # ===================================

        # if self.cvd.is_bullish():
        #     score += self.loader.get_weight("orderflow", "cvd_bullish")

        #     reasons.append("CVD Bullish")

        # elif self.cvd.is_bearish():
        #     score += self.loader.get_weight("orderflow", "cvd_bearish")

        #     reasons.append("CVD Bearish")
        if self.cvd is not None:
            if self.cvd.is_bullish():
                score += self.loader.get_weight("orderflow", "cvd_bullish")

                reasons.append("cvd Bullish")

            elif self.cvd.is_bearish():
                score += self.loader.get_weight("orderflow", "cvd_bearish")

                reasons.append("cvd Bearish")
        # ===================================
        # DECISION
        # ===================================
        self.logger.info(
            f"[SCORE_BREAKDOWN] "
            f"score={score} "
            f"reasons={reasons} "
            f"EMA_FAST={self.ema_fast.get_value()} "
            f"EMA_SLOW={self.ema_slow.get_value()} "
            f"VWAP={self.vwap.get_value()} "
            f"AWVAP={self.awvap.get_value()} "
            f"RVOL={self.rvol.get_value()} "
            f"VWMA={self.vwma.get_value()} "
            f"ATR={self.atr.get_value()}"
        )
        if score >= (self.loader.get_threshold("strong_long")):
            direction = "STRONG_LONG"

            confidence = "HIGH"

        elif score >= (self.loader.get_threshold("long")):
            direction = "LONG"

            confidence = "MEDIUM"

        elif score <= (self.loader.get_threshold("strong_short")):
            direction = "STRONG_SHORT"

            confidence = "HIGH"

        elif score <= (self.loader.get_threshold("short")):
            direction = "SHORT"

            confidence = "MEDIUM"

        else:
            direction = "NO_TRADE"

            confidence = "LOW"

        # ===================================
        # TRADE SETUP
        # ===================================

        atr_value = self.atr.get_value()
        self.logger.info(
            f"[ATR_DEBUG] direction={direction} price={current_price} atr={atr_value}"
        )
        if atr_value <= 0:
            self.logger.info(
                f"[ATR_STATE] "
                f"{self.atr.symbol} "
                f"{self.atr.timeframe} "
                f"value={atr_value} "
                f"ready={self.atr.is_ready()}"
            )
            return MultiFactorDecision(
                score=round(score, 2),
                direction="NO_TRADE",
                confidence="LOW",
                reasons=reasons + ["ATR_NOT_READY"],
                stop_loss=0.0,
                target=0.0,
            )

        risk_distance = atr_value * ATR_STOP_MULTIPLIER

        stop_loss = 0.0

        target = 0.0

        # -----------------------------------
        # LONG SETUP
        # -----------------------------------

        if direction in {"LONG", "STRONG_LONG"}:
            stop_loss = round(current_price - risk_distance, 2)

            target = round(current_price + (risk_distance * RISK_REWARD_RATIO), 2)

        # -----------------------------------
        # SHORT SETUP
        # -----------------------------------

        elif direction in {"SHORT", "STRONG_SHORT"}:
            stop_loss = round(current_price + risk_distance, 2)

            target = round(current_price - (risk_distance * RISK_REWARD_RATIO), 2)

        return MultiFactorDecision(
            score=round(score, 2),
            direction=direction,
            confidence=confidence,
            reasons=reasons,
            stop_loss=stop_loss,
            target=target,
        )
