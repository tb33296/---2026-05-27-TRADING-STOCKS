# tests/test_risk_engine.py

from core.risk.risk_engine import RiskEngine


class MockPositionManager:
    def __init__(
        self, open_positions: int, realized_pnl: float, consecutive_losses: int
    ) -> None:

        self.open_positions = open_positions

        self.realized_pnl = realized_pnl

        self.consecutive_losses = consecutive_losses

    def get_open_position_count(self) -> int:

        return self.open_positions

    def get_realized_pnl(self) -> float:

        return self.realized_pnl

    def get_total_net_pnl(self) -> float:

        return self.realized_pnl

    def get_consecutive_losses(self) -> int:

        return self.consecutive_losses


def test_risk_engine() -> None:

    print("\n=== RISK ENGINE TEST ===\n")

    # -------------------------
    # Approved
    # -------------------------

    manager = MockPositionManager(
        open_positions=1, realized_pnl=500, consecutive_losses=0
    )

    risk_engine = RiskEngine(manager)

    decision = risk_engine.evaluate(signal=None)

    print(f"Approved: {decision}")

    assert decision.approved

    # -------------------------
    # Max Positions
    # -------------------------

    manager = MockPositionManager(
        open_positions=999, realized_pnl=500, consecutive_losses=0
    )

    risk_engine = RiskEngine(manager)

    decision = risk_engine.evaluate(signal=None)

    print(f"Max Positions: {decision}")

    assert not decision.approved

    # -------------------------
    # Drawdown
    # -------------------------

    manager = MockPositionManager(
        open_positions=1, realized_pnl=-100000, consecutive_losses=0
    )

    risk_engine = RiskEngine(manager)

    decision = risk_engine.evaluate(signal=None)

    print(f"Drawdown: {decision}")

    assert not decision.approved

    # -------------------------
    # Consecutive Losses
    # -------------------------

    manager = MockPositionManager(
        open_positions=1, realized_pnl=0, consecutive_losses=999
    )

    risk_engine = RiskEngine(manager)

    decision = risk_engine.evaluate(signal=None)

    print(f"Losses: {decision}")

    assert not decision.approved

    print("\n=== TEST COMPLETE ===")
