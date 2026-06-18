from datetime import datetime

import pytz

from config.config import (
    TIMEZONE,
    MARKET_OPEN_TIME,
    MARKET_CLOSE_TIME
)


class MarketTime:
    """
    Market timing utilities.
    """

    @staticmethod
    def now() -> datetime:
        timezone = pytz.timezone(TIMEZONE)
        return datetime.now(timezone)

    @staticmethod
    def is_market_open() -> bool:

        current_time = MarketTime.now().time()

        return (
            MARKET_OPEN_TIME
            <= current_time
            <= MARKET_CLOSE_TIME
        )