# core/websocket/subscription_manager.py

from typing import Optional

from core.instruments.symbol_registry import (
    SymbolRegistry
)

from core.logging_manager import LoggingManager


class SubscriptionManager:
    """
    Handles websocket subscription payload generation.

    Responsibilities:
    - registry integration
    - exchange mapping
    - token batching
    - SmartAPI payload generation
    """

    EXCHANGE_TYPE_MAP = {
        "NSE": 1,
        "NFO": 2,
        "BSE": 3,
        "MCX": 5
    }

    def __init__(
        self,
        symbol_registry: SymbolRegistry
    ) -> None:

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.symbol_registry = (
            symbol_registry
        )

    def build_subscription_payload(
        self,
        exchange: str = "NSE"
    ) -> Optional[list[dict]]:
        """
        Build SmartAPI subscription payload.

        Example output:
        [
            {
                "exchangeType": 1,
                "tokens": ["2885", "3045"]
            }
        ]
        """

        try:

            normalized_exchange = (
                exchange.upper().strip()
            )

            exchange_type = (
                self.EXCHANGE_TYPE_MAP.get(
                    normalized_exchange
                )
            )

            if exchange_type is None:

                self.logger.error(
                    f"Unsupported exchange: "
                    f"{normalized_exchange}"
                )

                return None

            tokens = (
                self.symbol_registry
                .get_subscription_tokens(
                    exchange=normalized_exchange
                )
            )

            if not tokens:

                self.logger.warning(
                    "No subscription tokens available"
                )

                return None

            unique_tokens = sorted(
                list(set(tokens))
            )

            payload = [
                {
                    "exchangeType": exchange_type,
                    "tokens": unique_tokens
                }
            ]

            self.logger.info(
                f"Built subscription payload "
                f"for "
                f"{len(unique_tokens)} tokens"
            )

            return payload

        except Exception as error:

            self.logger.error(
                f"Subscription payload build "
                f"failed: {error}"
            )

            return None

    def build_group_subscription_payload(
        self,
        group_name: str,
        exchange: str = "NSE"
    ) -> Optional[list[dict]]:
        """
        Build subscription payload for group.
        """

        try:

            normalized_exchange = (
                exchange.upper().strip()
            )

            exchange_type = (
                self.EXCHANGE_TYPE_MAP.get(
                    normalized_exchange
                )
            )

            if exchange_type is None:

                self.logger.error(
                    f"Unsupported exchange: "
                    f"{normalized_exchange}"
                )

                return None

            symbols = (
                self.symbol_registry
                .get_group_symbols(
                    group_name
                )
            )

            if not symbols:

                self.logger.warning(
                    f"No symbols found in group: "
                    f"{group_name}"
                )

                return None

            tokens: list[str] = []

            resolver = (
                self.symbol_registry
                .token_resolver
            )

            for symbol in symbols:

                token = resolver.get_token(
                    symbol=symbol,
                    exchange=normalized_exchange
                )

                if token is not None:

                    tokens.append(token)

            if not tokens:

                self.logger.warning(
                    "No valid group tokens found"
                )

                return None

            unique_tokens = sorted(
                list(set(tokens))
            )

            payload = [
                {
                    "exchangeType": exchange_type,
                    "tokens": unique_tokens
                }
            ]

            self.logger.info(
                f"Built group subscription "
                f"payload for "
                f"{group_name}"
            )

            return payload

        except Exception as error:

            self.logger.error(
                f"Group subscription payload "
                f"failed: {error}"
            )

            return None

    def get_exchange_type(
        self,
        exchange: str
    ) -> Optional[int]:
        """
        Return SmartAPI exchange type.
        """

        return self.EXCHANGE_TYPE_MAP.get(
            exchange.upper().strip()
        )

    def is_exchange_supported(
        self,
        exchange: str
    ) -> bool:
        """
        Check exchange support.
        """

        return (
            self.get_exchange_type(
                exchange
            ) is not None
        )
