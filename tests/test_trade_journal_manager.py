from datetime import datetime

from database.db_manager import (
    DatabaseManager
)

from core.journal.trade_journal_manager import (
    TradeJournalManager
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
# test_trade_database_schema.py

def test_trade_journal_manager() -> None:

    print(
        "\n=== TRADE JOURNAL TEST ===\n"
    )

    db = DatabaseManager()

    db.connect()

    db.initialize_schema()

    manager = (
        TradeJournalManager(
            db
        )
    )

    trade_id = (
        manager.create_trade(
            TradeSnapshot(
                trade_id=None,

                symbol="RELIANCE",

                segment="EQUITY",

                strategy_name=(
                    "MultiFactor"
                ),

                direction="LONG",

                entry_time=(
                    datetime.now()
                    .isoformat()
                ),

                quantity=100,

                entry_price=100,

                stop_loss=95,

                target=110,

                score=85,

                confidence="HIGH",

                risk_amount=625,

                risk_percent=0.625,

                status="OPEN"
            )
        )
    )

    print(
        f"Trade ID: "
        f"{trade_id}"
    )

    manager.add_reason(
        trade_id,
        "EMA Bullish"
    )

    manager.add_reason(
        trade_id,
        "Above VWAP"
    )

    manager.add_metrics_snapshot(
        TradeMetricsSnapshot(
            trade_id=trade_id,

            atr=10,

            rvol=2,

            vwap=100,

            awvap=99,

            vwma=98,

            liquidity_ratio=0.75,

            liquidity_delta=500,

            cvd=1500
        )
    )

    manager.add_feature_snapshot(
        TradeFeatureSnapshot(
            trade_id=trade_id,

            trend_state="BULLISH",

            vwap_state="ABOVE",

            awvap_state="ABOVE",

            vwma_state="ABOVE",

            rvol_state="HIGH",

            atr_state="NORMAL",

            liquidity_state=(
                "BULLISH"
            ),

            cvd_state="BULLISH"
        )
    )

    trade = (
        manager.get_trade(
            trade_id
        )
    )

    assert trade is not None

    print(
        "Trade Record Created"
    )

    manager.close_trade(
        trade_id=trade_id,

        exit_time=(
            datetime.now()
            .isoformat()
        ),

        exit_price=110,

        gross_pnl=1000,

        net_pnl=980,

        charges=20,

        exit_reason="TARGET",

        duration_seconds=300
    )

    print(
        "Trade Closed"
    )

    db.close()

    print(
        "\n=== TEST COMPLETE ==="
    )