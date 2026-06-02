from database.db_manager import (
    DatabaseManager
)

from core.journal.trade_snapshot import (
    TradeSnapshot
)

from core.journal.trade_metrics_snapshot import (
    TradeMetricsSnapshot
)

from core.journal.trade_feature_snapshot import (
    TradeFeatureSnapshot
)


class TradeJournalManager:
    """
    Trade journal persistence layer.
    """

    def __init__(
        self,
        db_manager: DatabaseManager
    ) -> None:

        self.db = db_manager

    def create_trade(
        self,
        trade: TradeSnapshot
    ) -> int:
        """
        Create trade record.

        Returns:
            trade_id
        """

        cursor = self.db.execute(
            """
            INSERT INTO trades (

                symbol,
                segment,
                strategy_name,
                direction,

                entry_time,

                quantity,

                entry_price,

                stop_loss,
                target,

                score,
                confidence,

                risk_amount,
                risk_percent,

                status

            )

            VALUES (
                ?, ?, ?, ?,
                ?,
                ?,
                ?,
                ?, ?,
                ?, ?,
                ?, ?,
                ?
            )
            """,
            (
                trade.symbol,
                trade.segment,
                trade.strategy_name,
                trade.direction,

                trade.entry_time,

                trade.quantity,

                trade.entry_price,

                trade.stop_loss,
                trade.target,

                trade.score,
                trade.confidence,

                trade.risk_amount,
                trade.risk_percent,

                trade.status
            )
        )

        if cursor.lastrowid is None:

            raise RuntimeError(
                "Failed to create trade record"
            )

        return cursor.lastrowid

    def add_reason(
        self,
        trade_id: int,
        reason: str
    ) -> None:

        self.db.execute(
            """
            INSERT INTO trade_reasons (
                trade_id,
                reason
            )
            VALUES (?, ?)
            """,
            (
                trade_id,
                reason
            )
        )

    def add_metrics_snapshot(
        self,
        snapshot: TradeMetricsSnapshot
    ) -> None:

        self.db.execute(
            """
            INSERT INTO
            trade_metrics_snapshot (

                trade_id,

                atr,
                rvol,

                vwap,
                awvap,
                vwma,

                liquidity_ratio,
                liquidity_delta,

                cvd

            )

            VALUES (
                ?, ?, ?,
                ?, ?, ?,
                ?, ?,
                ?
            )
            """,
            (
                snapshot.trade_id,

                snapshot.atr,
                snapshot.rvol,

                snapshot.vwap,
                snapshot.awvap,
                snapshot.vwma,

                snapshot.liquidity_ratio,
                snapshot.liquidity_delta,

                snapshot.cvd
            )
        )

    def add_feature_snapshot(
        self,
        snapshot: TradeFeatureSnapshot
    ) -> None:

        self.db.execute(
            """
            INSERT INTO
            trade_feature_snapshot (

                trade_id,

                trend_state,

                vwap_state,
                awvap_state,
                vwma_state,

                rvol_state,
                atr_state,

                liquidity_state,

                cvd_state

            )

            VALUES (
                ?, ?, ?,
                ?, ?, ?,
                ?, ?,
                ?
            )
            """,
            (
                snapshot.trade_id,

                snapshot.trend_state,

                snapshot.vwap_state,
                snapshot.awvap_state,
                snapshot.vwma_state,

                snapshot.rvol_state,
                snapshot.atr_state,

                snapshot.liquidity_state,

                snapshot.cvd_state
            )
        )

    def close_trade(
        self,
        trade_id: int,
        exit_time: str,
        exit_price: float,
        gross_pnl: float,
        net_pnl: float,
        charges: float,
        exit_reason: str,
        duration_seconds: int
    ) -> None:

        self.db.execute(
            """
            UPDATE trades
            SET

                exit_time = ?,

                exit_price = ?,

                gross_pnl = ?,

                net_pnl = ?,

                charges = ?,

                exit_reason = ?,

                trade_duration_seconds = ?,

                status = 'CLOSED'

            WHERE trade_id = ?
            """,
            (
                exit_time,

                exit_price,

                gross_pnl,

                net_pnl,

                charges,

                exit_reason,

                duration_seconds,

                trade_id
            )
        )

    def get_trade(
        self,
        trade_id: int
    ):

        cursor = self.db.execute(
            """
            SELECT *
            FROM trades
            WHERE trade_id = ?
            """,
            (
                trade_id,
            )
        )

        return cursor.fetchone()