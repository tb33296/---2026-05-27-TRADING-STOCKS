# runtime/candidate_selection_engine.py

from config.config import MAX_NEW_TRADES_PER_CANDLE

from core.logging_manager import LoggingManager

from runtime.candidate_pool import CandidatePool

from runtime.trade_pipeline import TradePipeline


class CandidateSelectionEngine:
    def __init__(
        self,
        candidate_pool: CandidatePool,
        trade_pipeline: TradePipeline,
    ) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.candidate_pool = candidate_pool

        self.trade_pipeline = trade_pipeline

    def process_candidates(
        self,
    ) -> int:

        candidates = self.candidate_pool.get_all()

        if not candidates:
            return 0
        self.logger.info(f"[POOL_SIZE] {len(candidates)}")
        candidates.sort(
            key=lambda candidate: candidate.ranking_score,
            reverse=True,
        )

        top_candidates = candidates[:MAX_NEW_TRADES_PER_CANDLE]

        self.logger.info(
            f"[CANDIDATE_SELECTION] "
            f"pool={len(candidates)} "
            f"selected={len(top_candidates)}"
        )

        executed = 0

        for candidate in top_candidates:
            self.logger.info(
                f"[SELECTED] {candidate.trade_context.symbol} {candidate.ranking_score}"
            )
            self.trade_pipeline.execute_trade(
                trade_context=candidate.trade_context,
                account_size=candidate.account_size,
            )

            executed += 1

        self.candidate_pool.clear()

        return executed
