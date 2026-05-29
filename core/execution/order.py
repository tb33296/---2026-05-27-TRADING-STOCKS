# core/execution/order.py

from dataclasses import dataclass, field

from datetime import datetime

from typing import Any


@dataclass(slots=True)
class Order:
    """
    Standardized execution order.
    """

    symbol: str

    side: str

    quantity: int

    price: float

    order_type: str

    strategy_name: str

    timestamp: datetime

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def is_buy(self) -> bool:
        """
        Check BUY order.
        """

        return (
            self.side.upper()
            == "BUY"
        )

    def is_sell(self) -> bool:
        """
        Check SELL order.
        """

        return (
            self.side.upper()
            == "SELL"
        )

    def is_market_order(
        self
    ) -> bool:
        """
        Check MARKET order.
        """

        return (
            self.order_type.upper()
            == "MARKET"
        )

    def to_dict(self) -> dict:
        """
        Convert order to dictionary.
        """

        return {
            "symbol": self.symbol,

            "side": self.side,

            "quantity": self.quantity,

            "price": self.price,

            "order_type": self.order_type,

            "strategy_name": (
                self.strategy_name
            ),

            "timestamp": self.timestamp,

            "metadata": self.metadata
        }
