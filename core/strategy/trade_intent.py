from dataclasses import dataclass, field

from datetime import datetime

from uuid import uuid4


@dataclass(slots=True)
class TradeIntent:
    """
    Strategy decision object.

    Represents an action a strategy wishes
    to perform.

    TradeIntent is NOT an order.

    It is later validated by:

    Strategy Runtime
            ↓
    Risk Runtime
            ↓
    Execution Runtime
    """

    symbol: str

    timeframe: str

    action: str

    quantity: int

    timestamp: datetime

    strategy_name: str

    signal_name: str | None = None

    confidence: float = 1.0

    price: float | None = None

    metadata: dict = field(default_factory=dict)

    reason: str = ""

    intent_id: str = field(default_factory=lambda: str(uuid4()))

    VALID_ACTIONS = {
        "BUY",
        "SELL",
        "EXIT_LONG",
        "EXIT_SHORT",
        "HOLD",
        "REVERSE_LONG",
        "REVERSE_SHORT",
    }

    def __post_init__(self) -> None:

        self.action = self.action.upper().strip()

        if self.action not in self.VALID_ACTIONS:
            raise ValueError(f"Invalid action: {self.action}")

    def is_entry(self) -> bool:

        return self.action in {
            "BUY",
            "SELL",
        }

    def is_exit(self) -> bool:

        return self.action in {
            "EXIT_LONG",
            "EXIT_SHORT",
        }

    def is_buy(self) -> bool:

        return self.action == "BUY"

    def is_sell(self) -> bool:

        return self.action == "SELL"

    def is_exit_long(self) -> bool:

        return self.action == "EXIT_LONG"

    def is_exit_short(self) -> bool:

        return self.action == "EXIT_SHORT"

    def is_hold(self) -> bool:

        return self.action == "HOLD"

    def to_dict(self) -> dict:

        return {
            "intent_id": self.intent_id,
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "action": self.action,
            "quantity": self.quantity,
            "timestamp": self.timestamp,
            "strategy_name": self.strategy_name,
            "signal_name": self.signal_name,
            "confidence": self.confidence,
            "price": self.price,
            "reason": self.reason,
            "metadata": self.metadata,
        }
