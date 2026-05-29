# core/instruments/instrument_manager.py

import json

from pathlib import Path
from threading import Lock
from typing import Any, Optional

from core.logging_manager import LoggingManager

class InstrumentManager:
    """
    Handles instrument master loading and indexing.

    ```
    Responsibilities:
    - load instrument master
    - normalize records
    - build indexes
    - provide fast lookup access
    """

    def __init__(
        self,
        instrument_file: str
    ) -> None:

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.instrument_file = Path(
            instrument_file
        )

        self.lock = Lock()

        self.instruments: list[
            dict[str, Any]
        ] = []

        self.token_index: dict[
            str,
            dict[str, Any]
        ] = {}

        self.symbol_index: dict[
            str,
            list[dict[str, Any]]
        ] = {}

        self.name_index: dict[
            str,
            list[dict[str, Any]]
        ] = {}

        self.exchange_index: dict[
            str,
            list[dict[str, Any]]
        ] = {}

        self.is_loaded = False

    def load_instruments(self) -> bool:
        """
        Load and index instrument master.
        """

        try:

            if not self.instrument_file.exists():

                self.logger.error(
                    f"Instrument file missing: "
                    f"{self.instrument_file}"
                )

                return False

            self.logger.info(
                "Loading instrument master"
            )

            with open(
                self.instrument_file,
                "r",
                encoding="utf-8"
            ) as file:

                raw_data = json.load(file)

            if not isinstance(raw_data, list):

                self.logger.error(
                    "Invalid instrument file format"
                )

                return False

            with self.lock:

                self.instruments.clear()

                self.token_index.clear()

                self.symbol_index.clear()

                self.name_index.clear()

                self.exchange_index.clear()

                for record in raw_data:

                    normalized = (
                        self.normalize_instrument(
                            record
                        )
                    )

                    if normalized is None:
                        continue

                    self.instruments.append(
                        normalized
                    )

                    token = normalized["token"]

                    symbol = normalized["symbol"]

                    name = normalized[
                        "name"
                    ].upper()

                    exchange = normalized[
                        "exchange"
                    ]

                    self.token_index[token] = (
                        normalized
                    )

                    if (
                        symbol
                        not in self.symbol_index
                    ):

                        self.symbol_index[
                            symbol
                        ] = []

                    self.symbol_index[
                        symbol
                    ].append(normalized)

                    if (
                        name
                        not in self.name_index
                    ):

                        self.name_index[
                            name
                        ] = []

                    self.name_index[
                        name
                    ].append(normalized)

                    if (
                        exchange
                        not in self.exchange_index
                    ):

                        self.exchange_index[
                            exchange
                        ] = []

                    self.exchange_index[
                        exchange
                    ].append(normalized)

                self.is_loaded = True

            self.logger.info(
                f"Loaded "
                f"{len(self.instruments)} "
                f"instruments"
            )

            return True

        except Exception as error:

            self.logger.error(
                f"Instrument loading failed: "
                f"{error}"
            )

            return False

    def normalize_instrument(
        self,
        record: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        """
        Normalize raw instrument record.
        """

        try:

            token = str(
                record.get("token", "")
            ).strip()

            symbol = str(
                record.get("symbol", "")
            ).strip().upper()

            exchange = str(
                record.get("exch_seg", "")
            ).strip().upper()

            instrument = {
                "token": token,

                "symbol": symbol,

                "name": str(
                    record.get("name", "")
                ).strip(),

                "exchange": exchange,

                "instrument_type": str(
                    record.get(
                        "instrumenttype",
                        ""
                    )
                ).strip(),

                "expiry": str(
                    record.get(
                        "expiry",
                        ""
                    )
                ).strip(),

                "strike": float(
                    record.get(
                        "strike",
                        0
                    )
                ),

                "lot_size": int(
                    record.get(
                        "lotsize",
                        0
                    )
                )
            }

            if not token:
                return None

            if not symbol:
                return None

            return instrument

        except Exception as error:

            self.logger.warning(
                f"Instrument normalization failed: "
                f"{error}"
            )

            return None

    def get_instrument_by_token(
        self,
        token: str
    ) -> Optional[dict[str, Any]]:
        """
        Return instrument by token.
        """

        with self.lock:

            return self.token_index.get(
                token
            )

    def get_instruments_by_symbol(
        self,
        symbol: str
    ) -> list[dict[str, Any]]:
        """
        Return instruments for trading symbol.
        """

        with self.lock:

            return self.symbol_index.get(
                symbol.upper(),
                []
            )

    def get_instruments_by_name(
        self,
        name: str
    ) -> list[dict[str, Any]]:
        """
        Return instruments for company name.
        """

        with self.lock:

            return self.name_index.get(
                name.upper(),
                []
            )

    def get_instruments_by_exchange(
        self,
        exchange: str
    ) -> list[dict[str, Any]]:
        """
        Return instruments for exchange.
        """

        with self.lock:

            return self.exchange_index.get(
                exchange.upper(),
                []
            )

    def get_total_instruments(self) -> int:
        """
        Return total loaded instruments.
        """

        with self.lock:

            return len(
                self.instruments
            )

    def is_instrument_loaded(self) -> bool:
        """
        Return instrument load status.
        """

        return self.is_loaded

    def clear(self) -> None:
        """
        Clear all cached instruments.
        """

        with self.lock:

            self.instruments.clear()

            self.token_index.clear()

            self.symbol_index.clear()

            self.name_index.clear()

            self.exchange_index.clear()

            self.is_loaded = False

            self.logger.info(
                "Instrument cache cleared"
            )
