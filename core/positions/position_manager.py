# core/positions/position_manager.py

from datetime import datetime

from core.logging_manager import LoggingManager

from core.positions.position import Position
from core.execution.charges_engine import ChargesEngine


class PositionManager:
    """
    Tracks all positions and PnL.
    """

    def __init__(self) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.charges_engine = ChargesEngine()

        self.open_positions: dict[str, Position] = {}

        self.closed_positions: list[Position] = []

    def open_position(self, position: Position) -> bool:
        """
        Open new position.
        """

        try:
            if position.symbol in self.open_positions:
                self.logger.warning(f"Position already open: {position.symbol}")

                return False

            self.open_positions[position.symbol] = position

            return True

        except Exception as error:
            self.logger.error(f"Open position failed: {error}")

            return False

    def close_position(self, symbol: str, exit_price: float) -> Position | None:
        """
        Close existing position.
        """

        try:
            position = self.open_positions.get(symbol)

            if position is None:
                return None

            position.exit_price = exit_price

            position.exit_time = datetime.now()
            position.duration_seconds = int(
                (position.exit_time - position.entry_time).total_seconds()
            )
            position.status = "CLOSED"

            if position.side == "LONG":
                gross_pnl = (exit_price - position.entry_price) * position.quantity

            elif position.side == "SHORT":
                gross_pnl = (position.entry_price - exit_price) * position.quantity

            else:
                raise ValueError(f"Unknown side: {position.side}")

            position.gross_pnl = gross_pnl

            turnover = (position.entry_price * position.quantity) + (
                exit_price * position.quantity
            )

            charges = self.charges_engine.calculate(
                segment=position.segment, turnover=turnover
            )
            self.logger.debug(f"Turnover={turnover} Charges={charges}")
            position.charges = charges

            position.net_pnl = gross_pnl - charges

            self.closed_positions.append(position)

            del self.open_positions[symbol]

            return position

        except Exception as error:
            self.logger.error(f"Close position failed: {error}")

            return None

    def get_open_positions(self) -> dict[str, Position]:

        return self.open_positions

    def get_closed_positions(self) -> list[Position]:

        return self.closed_positions

    def get_open_position_count(self) -> int:

        return len(self.open_positions)

    def get_total_gross_pnl(self) -> float:

        return round(sum(p.gross_pnl for p in self.closed_positions), 2)

    def get_total_charges(self) -> float:

        return round(sum(p.charges for p in self.closed_positions), 2)

    def get_total_net_pnl(self) -> float:

        return round(sum(p.net_pnl for p in self.closed_positions), 2)

    def get_consecutive_losses(self) -> int:
        """
        Count consecutive losing trades.
        """

        count = 0

        for position in reversed(self.closed_positions):
            if position.net_pnl < 0:
                count += 1

            else:
                break

        return count
