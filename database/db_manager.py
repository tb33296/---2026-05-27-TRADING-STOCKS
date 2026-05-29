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
        CREATE TABLE IF NOT EXISTS candles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            timeframe TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume INTEGER NOT NULL
        );

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
            duration_seconds REAL NOT NULL );

        CREATE TABLE IF NOT EXISTS system_health (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            cpu_usage REAL,
            memory_usage REAL,
            websocket_latency REAL
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