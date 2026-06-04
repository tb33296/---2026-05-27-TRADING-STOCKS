# runtime/trade_pipeline.py

from core.execution.paper_execution_engine import PaperExecutionEngine

from core.logging_manager import LoggingManager

from core.risk.position_sizing_engine import PositionSizingEngine

from core.risk.risk_engine import RiskEngine

from core.strategy.trade_context import TradeContext

from core.strategy.trade_decision_engine import TradeDecisionEngine

from core.journal.trade_journal_manager import TradeJournalManager

from core.journal.trade_snapshot import TradeSnapshot


class TradePipeline:
    """
    Trading orchestration layer.

    Responsibilities:

    - trade approval
    - risk validation
    - position sizing
    - execution
    """

    def __init__(
        self,
        risk_engine: RiskEngine,
        execution_engine: PaperExecutionEngine,
        journal_manager: TradeJournalManager,
    ) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.risk_engine = risk_engine

        self.execution_engine = execution_engine
        self.journal_manager = journal_manager

        self.trade_decision_engine = TradeDecisionEngine()

        self.position_sizing_engine = PositionSizingEngine()

    # -------------------------------------------------------------------------------------
    def _create_journal_entry(
        self, trade_context: TradeContext, execution, sizing
    ) -> int:
        """
        Persist newly opened trade.
        """

        trade_id = self.journal_manager.create_trade(
            TradeSnapshot(
                trade_id=None,
                symbol=(trade_context.symbol),
                segment=(trade_context.segment),
                strategy_name=("MultiFactor"),
                direction=(trade_context.direction),
                entry_time=(execution.timestamp.isoformat()),
                quantity=(execution.quantity),
                entry_price=(execution.fill_price),
                stop_loss=(trade_context.stop_loss),
                target=(trade_context.target),
                score=(trade_context.score),
                confidence=(trade_context.confidence),
                risk_amount=(sizing.risk_amount),
                risk_percent=(sizing.risk_percent),
                status="OPEN",
            )
        )

        for reason in trade_context.reasons:
            self.journal_manager.add_reason(trade_id, reason)

        return trade_id

    # `````````````````````````````````````````````````````~~~~~~~~~~~~~~~~~~~~~~~~~```````

    def execute_trade(self, trade_context: TradeContext, account_size: float):
        """
        Execute full trade workflow.
        """

        try:
            sizing = self.position_sizing_engine.calculate(
                account_size=account_size,
                score=(trade_context.score),
                entry_price=(trade_context.entry_price),
                stop_loss=(trade_context.stop_loss),
            )

            decision = self.trade_decision_engine.evaluate(
                score=(trade_context.score),
                direction=(trade_context.direction),
                confidence=(trade_context.confidence),
                quantity=(sizing.quantity),
            )

            if not decision.approved:
                return (decision, None, None, sizing)

            risk = self.risk_engine.evaluate(decision)

            if not risk.approved:
                return (decision, risk, None, sizing)

            if decision.is_long():
                execution = self.execution_engine.execute_buy(
                    symbol=(trade_context.symbol),
                    segment=(trade_context.segment),
                    quantity=(sizing.quantity),
                    ltp=(trade_context.entry_price),
                    stop_loss=(trade_context.stop_loss),
                    target=(trade_context.target),
                )
                if execution.success and execution.position_opened:
                    trade_id = self._create_journal_entry(
                        trade_context, execution, sizing
                    )

                    position = (
                        self.execution_engine.position_manager.open_positions.get(
                            trade_context.symbol
                        )
                    )

                    if position is not None:
                        position.trade_id = trade_id
                        self.logger.info(
                            f"Trade ID {trade_id} linked to {trade_context.symbol}"
                        )

                return (decision, risk, execution, sizing)

            return (decision, risk, None, sizing)

        except Exception as error:
            self.logger.error(f"Trade pipeline failed: {error}")

            return (None, None, None, None)

    def close_trade(self, symbol: str, exit_price: float, exit_reason: str) -> bool:
        """
        Close trade and update journal.
        """

        try:
            closed_position = self.execution_engine.execute_sell(
                symbol=symbol, exit_price=exit_price
            )

            if closed_position is None:
                return False

            if closed_position.trade_id is None:
                self.logger.error(f"No trade_id found for {symbol}")

                return False

            if closed_position.exit_time is None:
                self.logger.error(f"Missing exit_time for {symbol}")

                return False

            if closed_position.exit_price is None:
                self.logger.error(f"Missing exit_price for {symbol}")

                return False
            self.journal_manager.close_trade(
                trade_id=(closed_position.trade_id),
                exit_time=(closed_position.exit_time.isoformat()),
                exit_price=(closed_position.exit_price),
                gross_pnl=(closed_position.gross_pnl),
                net_pnl=(closed_position.net_pnl),
                charges=(closed_position.charges),
                exit_reason=(exit_reason),
                duration_seconds=(closed_position.duration_seconds),
            )

            self.logger.info(
                f"Trade closed: {symbol} (trade_id={closed_position.trade_id})"
            )
            return True

        except Exception as error:
            self.logger.error(f"Trade close failed: {error}")

            return False
