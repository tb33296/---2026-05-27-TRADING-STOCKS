# core/instruments/token_resolver.py

from typing import Any, Optional

from core.instruments.instrument_manager import (
    InstrumentManager
)

from core.logging_manager import LoggingManager


class TokenResolver:
    """
    Handles instrument token resolution.

    Responsibilities:
    - symbol -> token
    - token -> symbol
    - exchange filtering
    - instrument filtering
    """

    def __init__(
        self,
        instrument_manager: InstrumentManager
    ) -> None:

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.instrument_manager = (
            instrument_manager
        )

    def get_token(
        self,
        symbol: str,
        exchange: Optional[str] = None
    ) -> Optional[str]:
        """
        Resolve token from symbol.
        """

        try:

            instruments = (
                self.instrument_manager
                .get_instruments_by_name(
                    symbol
                )
            )

            if not instruments:

                self.logger.warning(
                    f"Symbol not found: "
                    f"{symbol}"
                )

                return None

            if exchange is not None:

                exchange = (
                    exchange.upper()
                )

                for instrument in instruments:

                    if (
                        instrument["exchange"]
                        == exchange
                    ):

                        return instrument["token"]

                self.logger.warning(
                    f"Symbol {symbol} not found "
                    f"for exchange {exchange}"
                )

                return None

            return instruments[0]["token"]

        except Exception as error:

            self.logger.error(
                f"Token lookup failed: {error}"
            )

            return None

    def get_symbol(
        self,
        token: str
    ) -> Optional[str]:
        """
        Resolve symbol from token.
        """

        try:

            instrument = (
                self.instrument_manager
                .get_instrument_by_token(
                    token
                )
            )

            if instrument is None:

                self.logger.warning(
                    f"Token not found: {token}"
                )

                return None

            return instrument["symbol"]

        except Exception as error:

            self.logger.error(
                f"Symbol lookup failed: {error}"
            )

            return None

    def get_instrument(
        self,
        token: str
    ) -> Optional[dict[str, Any]]:
        """
        Return full instrument data.
        """

        try:

            return (
                self.instrument_manager
                .get_instrument_by_token(
                    token
                )
            )

        except Exception as error:

            self.logger.error(
                f"Instrument lookup failed: "
                f"{error}"
            )

            return None

    def get_equity_token(
        self,
        symbol: str
    ) -> Optional[str]:
        """
        Resolve NSE cash token.
        """

        return self.get_token(
            symbol=symbol,
            exchange="NSE"
        )

    def get_fno_token(
        self,
        symbol: str
    ) -> Optional[str]:
        """
        Resolve NSE F&O token.
        """

        return self.get_token(
            symbol=symbol,
            exchange="NFO"
        )

    def get_exchange(
        self,
        token: str
    ) -> Optional[str]:
        """
        Return exchange from token.
        """

        try:

            instrument = (
                self.instrument_manager
                .get_instrument_by_token(
                    token
                )
            )

            if instrument is None:
                return None

            return instrument["exchange"]

        except Exception as error:

            self.logger.error(
                f"Exchange lookup failed: "
                f"{error}"
            )

            return None

    def token_exists(
        self,
        token: str
    ) -> bool:
        """
        Check whether token exists.
        """

        instrument = self.get_instrument(
            token
        )

        return instrument is not None

    def symbol_exists(
        self,
        symbol: str
    ) -> bool:
        """
        Check whether symbol exists.
        """

        instruments = (
            self.instrument_manager
            .get_instruments_by_name(
                symbol
            )
        )

        return len(instruments) > 0
