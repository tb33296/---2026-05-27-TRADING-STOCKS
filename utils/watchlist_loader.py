# utils/watchlist_loader.py

from pathlib import Path

from core.logging_manager import LoggingManager


class WatchlistLoader:
    """
    Loads watchlist files.

    One symbol per line.
    """

    def __init__(self) -> None:

        self.logger = LoggingManager.get_logger(
            __name__
        )

    def load(
        self,
        file_path: str
    ) -> list[str]:
        """
        Load symbols from watchlist file.
        """

        try:

            path = Path(file_path)

            if not path.exists():

                self.logger.error(
                    f"Watchlist file not found: "
                    f"{file_path}"
                )

                return []

            symbols: list[str] = []

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as file:

                for line in file:

                    symbol = (
                        line.strip()
                        .upper()
                    )

                    if not symbol:
                        continue

                    symbols.append(symbol)

            self.logger.info(
                f"Loaded {len(symbols)} "
                f"symbols from watchlist"
            )

            return symbols

        except Exception as error:

            self.logger.error(
                f"Watchlist load failed: "
                f"{error}"
            )

            return []