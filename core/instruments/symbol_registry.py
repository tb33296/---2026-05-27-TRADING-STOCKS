# core/instruments/symbol_registry.py

from threading import Lock
from typing import Optional

from core.instruments.token_resolver import (
    TokenResolver
)

from core.logging_manager import LoggingManager


class SymbolRegistry:
    """
    Runtime symbol registry.

    Responsibilities:
    - active symbol tracking
    - subscription token generation
    - symbol group management
    - runtime watchlists
    """

    def __init__(
        self,
        token_resolver: TokenResolver
    ) -> None:

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.token_resolver = token_resolver

        self.lock = Lock()

        self.active_symbols: set[str] = set()

        self.symbol_groups: dict[
            str,
            set[str]
        ] = {}

    def add_symbol(
        self,
        symbol: str
    ) -> bool:
        """
        Add symbol to active registry.
        """

        try:

            normalized_symbol = (
                symbol.upper().strip()
            )

            if not (
                self.token_resolver
                .symbol_exists(
                    normalized_symbol
                )
            ):

                self.logger.warning(
                    f"Symbol does not exist: "
                    f"{normalized_symbol}"
                )

                return False

            with self.lock:

                if (
                    normalized_symbol
                    in self.active_symbols
                ):

                    self.logger.warning(
                        f"Duplicate symbol ignored: "
                        f"{normalized_symbol}"
                    )

                    return False

                self.active_symbols.add(
                    normalized_symbol
                )

            self.logger.info(
                f"Added symbol: "
                f"{normalized_symbol}"
            )

            return True

        except Exception as error:

            self.logger.error(
                f"Failed to add symbol: "
                f"{error}"
            )

            return False

    def remove_symbol(
        self,
        symbol: str
    ) -> bool:
        """
        Remove symbol from registry.
        """

        try:

            normalized_symbol = (
                symbol.upper().strip()
            )

            with self.lock:

                if (
                    normalized_symbol
                    not in self.active_symbols
                ):

                    return False

                self.active_symbols.remove(
                    normalized_symbol
                )

                for group_symbols in (
                    self.symbol_groups.values()
                ):

                    group_symbols.discard(
                        normalized_symbol
                    )

            self.logger.info(
                f"Removed symbol: "
                f"{normalized_symbol}"
            )

            return True

        except Exception as error:

            self.logger.error(
                f"Failed to remove symbol: "
                f"{error}"
            )

            return False

    def get_all_symbols(
        self
    ) -> list[str]:
        """
        Return all active symbols.
        """

        with self.lock:

            return sorted(
                self.active_symbols
            )

    def create_group(
        self,
        group_name: str
    ) -> bool:
        """
        Create symbol group.
        """

        try:

            normalized_group = (
                group_name.upper().strip()
            )

            with self.lock:

                if (
                    normalized_group
                    in self.symbol_groups
                ):

                    self.logger.warning(
                        f"Group already exists: "
                        f"{normalized_group}"
                    )

                    return False

                self.symbol_groups[
                    normalized_group
                ] = set()

            self.logger.info(
                f"Created group: "
                f"{normalized_group}"
            )

            return True

        except Exception as error:

            self.logger.error(
                f"Failed to create group: "
                f"{error}"
            )

            return False

    def add_symbol_to_group(
        self,
        group_name: str,
        symbol: str
    ) -> bool:
        """
        Add symbol to group.
        """

        try:

            normalized_group = (
                group_name.upper().strip()
            )

            normalized_symbol = (
                symbol.upper().strip()
            )

            with self.lock:

                if (
                    normalized_group
                    not in self.symbol_groups
                ):

                    self.logger.warning(
                        f"Group not found: "
                        f"{normalized_group}"
                    )

                    return False

                if (
                    normalized_symbol
                    not in self.active_symbols
                ):

                    self.logger.warning(
                        f"Symbol not active: "
                        f"{normalized_symbol}"
                    )

                    return False

                self.symbol_groups[
                    normalized_group
                ].add(
                    normalized_symbol
                )

            self.logger.info(
                f"Added {normalized_symbol} "
                f"to group "
                f"{normalized_group}"
            )

            return True

        except Exception as error:

            self.logger.error(
                f"Failed to add symbol to group: "
                f"{error}"
            )

            return False

    def get_group_symbols(
        self,
        group_name: str
    ) -> list[str]:
        """
        Return symbols for group.
        """

        normalized_group = (
            group_name.upper().strip()
        )

        with self.lock:

            symbols = (
                self.symbol_groups.get(
                    normalized_group,
                    set()
                )
            )

            return sorted(symbols)

    def get_subscription_tokens(
        self,
        exchange: str = "NSE"
    ) -> list[str]:
        """
        Return subscription-ready tokens.
        """

        tokens: list[str] = []

        try:

            with self.lock:

                symbols = list(
                    self.active_symbols
                )

            for symbol in symbols:

                token = (
                    self.token_resolver
                    .get_token(
                        symbol=symbol,
                        exchange=exchange
                    )
                )

                if token is not None:

                    tokens.append(token)

            return tokens

        except Exception as error:

            self.logger.error(
                f"Subscription token generation "
                f"failed: {error}"
            )

            return []

    def clear(self) -> None:
        """
        Clear registry state.
        """

        with self.lock:

            self.active_symbols.clear()

            self.symbol_groups.clear()

            self.logger.info(
                "Symbol registry cleared"
            )

    def get_total_symbols(self) -> int:
        """
        Return active symbol count.
        """

        with self.lock:

            return len(
                self.active_symbols
            )

    def group_exists(
        self,
        group_name: str
    ) -> bool:
        """
        Check whether group exists.
        """

        normalized_group = (
            group_name.upper().strip()
        )

        with self.lock:

            return (
                normalized_group
                in self.symbol_groups
            )

