# database/cvd_state_manager.py

from datetime import date
from datetime import datetime

from database.db_manager import DatabaseManager

from core.logging_manager import LoggingManager


class CVDStateManager:

    def __init__(
        self,
        database_manager: DatabaseManager,
    ) -> None:

        self.database_manager = database_manager

        self.logger = LoggingManager.get_logger(__name__)

    def load_symbol_cvd(
        self,
        symbol: str,
    ) -> float | None:

        try:

            today = date.today().isoformat()

            query = """
                SELECT
                    cvd
                FROM cvd_state
                WHERE symbol = ?
                AND trade_date = ?
            """

            row = self.database_manager.fetch_one(
                query,
                (
                    symbol,
                    today,
                ),
            )

            if row is None:
                return None

            return float(row["cvd"])

        except Exception as error:

            self.logger.error(
                f"Failed loading CVD for {symbol}: {error}"
            )

            return None

    def save_symbol_cvd(
        self,
        symbol: str,
        cvd: float,
        last_price: float = 0.0,
    ) -> None:

        try:

            today = date.today().isoformat()

            query = """
                INSERT INTO cvd_state (
                    symbol,
                    trade_date,
                    cvd,
                    last_price,
                    updated_at
                )
                VALUES (
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                )
                ON CONFLICT(
                    symbol,
                    trade_date
                )
                DO UPDATE SET
                    cvd = excluded.cvd,
                    last_price = excluded.last_price,
                    updated_at = excluded.updated_at
            """

            self.database_manager.execute(
                query,
                (
                    symbol,
                    today,
                    cvd,
                    last_price,
                    datetime.now().isoformat(),
                ),
            )

        except Exception as error:

            self.logger.error(
                f"Failed saving CVD for {symbol}: {error}"
            )

    def cleanup_old_rows(self) -> None:

        try:

            today = date.today().isoformat()

            self.database_manager.execute(
                """
                DELETE
                FROM cvd_state
                WHERE trade_date < ?
                """,
                (today,),
            )

        except Exception as error:

            self.logger.error(
                f"CVD cleanup failed: {error}"
            )