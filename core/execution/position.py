# core/execution/position.py

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Position:
    """
    Runtime trading position.
    """

    symbol: str

    side: str

    quantity: int

    entry_price: float

    entry_time: datetime

    current_price: float

    realized_pnl: float = 0.0

    unrealized_pnl: float = 0.0

    is_open: bool = True

    exit_price: float | None = None

    exit_time: datetime | None = None

    def update_price(
        self,
        price: float
    ) -> None:
        """
        Update current market price.
        """

        self.current_price = price

        self.unrealized_pnl = (
            self.calculate_unrealized_pnl()
        )

    def calculate_unrealized_pnl(
        self
    ) -> float:
        """
        Calculate unrealized PnL.
        """

        if self.is_long():

            return (
                (
                    self.current_price
                    - self.entry_price
                )
                * self.quantity
            )

        if self.is_short():

            return (
                (
                    self.entry_price
                    - self.current_price
                )
                * self.quantity
            )

        return 0.0

    def close(
        self,
        exit_price: float,
        exit_time: datetime
    ) -> None:
        """
        Close position.
        """

        self.exit_price = exit_price

        self.exit_time = exit_time

        self.current_price = exit_price

        self.realized_pnl = (
            self.calculate_realized_pnl()
        )

        self.unrealized_pnl = 0.0

        self.is_open = False

    def calculate_realized_pnl(
        self
    ) -> float:
        """
        Calculate realized PnL.
        """

        if self.exit_price is None:

            return 0.0

        if self.is_long():

            return (
                (
                    self.exit_price
                    - self.entry_price
                )
                * self.quantity
            )

        if self.is_short():

            return (
                (
                    self.entry_price
                    - self.exit_price
                )
                * self.quantity
            )

        return 0.0

    def is_long(self) -> bool:
        """
        Check LONG position.
        """

        return (
            self.side.upper()
            == "BUY"
        )

    def is_short(self) -> bool:
        """
        Check SHORT position.
        """

        return (
            self.side.upper()
            == "SELL"
        )

    def duration_seconds(
        self
    ) -> float:
        """
        Return trade duration in seconds.
        """

        if self.exit_time is None:

            return 0.0

        return (
            self.exit_time
            - self.entry_time
        ).total_seconds()

    def to_dict(self) -> dict:
        """
        Convert position to dictionary.
        """

        return {
            "symbol": self.symbol,

            "side": self.side,

            "quantity": self.quantity,

            "entry_price": self.entry_price,

            "entry_time": self.entry_time,

            "current_price": (
                self.current_price
            ),

            "realized_pnl": (
                self.realized_pnl
            ),

            "unrealized_pnl": (
                self.unrealized_pnl
            ),

            "is_open": self.is_open,

            "exit_price": self.exit_price,

            "exit_time": self.exit_time
        }
