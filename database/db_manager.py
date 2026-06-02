# OPTIONAL FUTURE IMPROVEMENT (LATER)

# Eventually you MAY add helpers:

# fetchone()
# fetchall()
# executemany()
# transaction()

# But NOT required now.

# Your current implementation is sufficient.



import sqlite3
from pathlib import Path
from typing import Optional

from config.config import SQLITE_DB_PATH, SQLITE_TIMEOUT


class DatabaseManager:
    """
    SQLite database manager.
    """

    def __init__(self) -> None:
        self.connection: Optional[sqlite3.Connection] = None

    def connect(self) -> None:
        """
        Create SQLite connection.
        """

        Path(SQLITE_DB_PATH).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            SQLITE_DB_PATH,
            timeout=SQLITE_TIMEOUT,
            check_same_thread=False
        )

        self.connection.execute("PRAGMA journal_mode=WAL;")
        self.connection.execute("PRAGMA synchronous=NORMAL;")

    def initialize_schema(self) -> None:
        """
        Initialize database schema.
        """

        if self.connection is None:
            raise RuntimeError("Database not connected")

        cursor = self.connection.cursor()

        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            side TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            entry_price REAL NOT NULL,
            exit_price REAL NOT NULL,
            pnl REAL NOT NULL,
            entry_time TEXT NOT NULL,
            exit_time TEXT NOT NULL,
            duration_seconds REAL NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS trade_reasons (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            trade_id INTEGER NOT NULL,

            reason TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS trade_metrics_snapshot (

            trade_id INTEGER PRIMARY KEY,

            atr REAL,

            rvol REAL,

            vwap REAL,

            awvap REAL,

            vwma REAL,

            liquidity_ratio REAL,

            liquidity_delta REAL,

            cvd REAL
        );

        CREATE TABLE IF NOT EXISTS trade_feature_snapshot (

            trade_id INTEGER PRIMARY KEY,

            trend_state TEXT,

            vwap_state TEXT,

            awvap_state TEXT,

            vwma_state TEXT,

            rvol_state TEXT,

            atr_state TEXT,

            liquidity_state TEXT,

            cvd_state TEXT
        );
        """)

        self.connection.commit()

    def execute(
        self,
        query: str,
        params: tuple = ()
    ) -> sqlite3.Cursor:
        """
        Execute query.
        """

        if self.connection is None:
            raise RuntimeError("Database not connected")

        cursor = self.connection.cursor()

        cursor.execute(query, params)

        self.connection.commit()

        return cursor

    def close(self) -> None:
        """
        Close connection.
        """

        if self.connection:
            self.connection.close()