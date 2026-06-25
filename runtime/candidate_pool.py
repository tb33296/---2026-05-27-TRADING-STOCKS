# runtime/candidate_pool.py

from core.strategy.trade_candidate import TradeCandidate
from core.logging_manager import LoggingManager


class CandidatePool:
    """
    Holds candidates waiting for ranking.

    One candidate per:
        symbol + direction

    Highest ranking score wins.
    """

    def __init__(self) -> None:
        self.logger = LoggingManager.get_logger(__name__)
        self.candidates: dict[
            tuple[str, str],
            TradeCandidate,
        ] = {}

    def add(
        self,
        candidate: TradeCandidate,
    ) -> None:

        key = (
            candidate.trade_context.symbol,
            candidate.trade_context.direction,
        )

        existing = self.candidates.get(key)

        if existing is None:
            self.candidates[key] = candidate
            self.logger.info(
                f"[POOL_ADD] "
                f"{candidate.trade_context.symbol} "
                f"{candidate.trade_context.direction} "
                f"{candidate.ranking_score}"
            )

            return

        if candidate.ranking_score > existing.ranking_score:
            self.candidates[key] = candidate
            self.logger.info(
                f"[POOL_REPLACE] "
                f"{candidate.trade_context.symbol} "
                f"{candidate.trade_context.direction} "
                f"{candidate.ranking_score}"
            )
        self.logger.info(
            f"[POOL_ADD] "
            f"{candidate.trade_context.symbol} "
            f"size_before={len(self.candidates)}"
        )

    def get_all(
        self,
    ) -> list[TradeCandidate]:

        return list(self.candidates.values())

    def size(
        self,
    ) -> int:

        return len(self.candidates)

    def clear(
        self,
    ) -> None:
        self.logger.info(f"[POOL_CLEAR] size={len(self.candidates)}")

        self.candidates.clear()
