# core/execution/tradebook.py

from threading import Lock

from database.db_manager import ( DatabaseManager )




from core.execution.position import Position

from core.logging_manager import LoggingManager


class Tradebook:
    """
    Handles closed trade persistence
    and trade analytics.
    """

    TABLE_NAME = "legacy_trades"

    def __init__(
        self,
        database_manager: DatabaseManager
    ) -> None:

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.database_manager = (
            database_manager
        )

        self.lock = Lock()

        self.closed_trades: list[
            Position
        ] = []

        self._initialize_table()

    def _initialize_table(
        self
    ) -> None:
        """
        Create trades table if needed.
        """

        try:

            query = f"""
            CREATE TABLE IF NOT EXISTS
            {self.TABLE_NAME}
            (
                id INTEGER PRIMARY KEY
                AUTOINCREMENT,

                symbol TEXT NOT NULL,

                side TEXT NOT NULL,

                quantity INTEGER NOT NULL,

                entry_price REAL NOT NULL,

                exit_price REAL NOT NULL,

                pnl REAL NOT NULL,

                entry_time TEXT NOT NULL,

                exit_time TEXT NOT NULL,

                duration_seconds REAL NOT NULL
            )
            """

            self.database_manager.execute(
                query
            )

            self.logger.info(
                "Tradebook table initialized"
            )

        except Exception as error:

            self.logger.error(
                f"Tradebook table init "
                f"failed: {error}"
            )

    def add_trade(
        self,
        position: Position
    ) -> bool:
        """
        Store closed trade.
        """

        try:

            if position.is_open:

                self.logger.warning(
                    "Cannot persist open "
                    "position"
                )

                return False

            with self.lock:

                self.closed_trades.append(
                    position
                )

            query = f"""
            INSERT INTO
            {self.TABLE_NAME}
            (
                symbol,
                side,
                quantity,
                entry_price,
                exit_price,
                pnl,
                entry_time,
                exit_time,
                duration_seconds
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """

            values = (
                position.symbol,

                position.side,

                position.quantity,

                position.entry_price,

                position.exit_price,

                position.realized_pnl,

                position.entry_time.isoformat(),

                (
                    position.exit_time
                    .isoformat()
                    if position.exit_time
                    else ""
                ),

                position.duration_seconds()
            )

            self.database_manager.execute(
                query,
                values
            )

            self.logger.info(
                f"Trade stored: "
                f"{position.symbol} "
                f"PnL="
                f"{position.realized_pnl:.2f}"
            )

            return True

        except Exception as error:

            self.logger.error(
                f"Trade persistence failed: "
                f"{error}"
            )

            return False

    def get_all_trades(
        self
    ) -> list[Position]:
        """
        Return closed trades.
        """

        with self.lock:

            return list(
                self.closed_trades
            )

    def total_pnl(
        self
    ) -> float:
        """
        Return total realized PnL.
        """

        with self.lock:

            return sum(
                trade.realized_pnl
                for trade in (
                    self.closed_trades
                )
            )

    def total_trades(
        self
    ) -> int:
        """
        Return total trade count.
        """

        with self.lock:

            return len(
                self.closed_trades
            )

    def winning_trades(
        self
    ) -> int:
        """
        Return winning trade count.
        """

        with self.lock:

            return sum(
                1
                for trade in (
                    self.closed_trades
                )
                if (
                    trade.realized_pnl > 0
                )
            )

    def losing_trades(
        self
    ) -> int:
        """
        Return losing trade count.
        """

        with self.lock:

            return sum(
                1
                for trade in (
                    self.closed_trades
                )
                if (
                    trade.realized_pnl < 0
                )
            )

    def win_rate(
        self
    ) -> float:
        """
        Return trade win rate.
        """

        total = self.total_trades()

        if total == 0:

            return 0.0

        return (
            self.winning_trades()
            / total
        ) * 100

    def average_win(
        self
    ) -> float:
        """
        Return average winning PnL.
        """

        wins = []

        with self.lock:

            for trade in (
                self.closed_trades
            ):

                if (
                    trade.realized_pnl > 0
                ):

                    wins.append(
                        trade.realized_pnl
                    )

        if not wins:

            return 0.0

        return sum(wins) / len(wins)

    def average_loss(
        self
    ) -> float:
        """
        Return average losing PnL.
        """

        losses = []

        with self.lock:

            for trade in (
                self.closed_trades
            ):

                if (
                    trade.realized_pnl < 0
                ):

                    losses.append(
                        trade.realized_pnl
                    )

        if not losses:

            return 0.0

        return sum(losses) / len(losses)

    def clear(self) -> None:
        """
        Clear in-memory tradebook.
        """

        with self.lock:

            self.closed_trades.clear()

        self.logger.info(
            "Tradebook cleared"
        )
