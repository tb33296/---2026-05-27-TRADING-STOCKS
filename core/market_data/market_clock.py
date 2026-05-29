# core/market_data/market_clock.py

from datetime import (
    date,
    datetime,
    time,
    timedelta
)

from pathlib import Path
from typing import Optional

from core.logging_manager import LoggingManager
from config.config import ( MARKET_HOLIDAY_FILE )

class MarketClock:
    """
    Centralized NSE market timing authority.

    Responsibilities:
    - market open detection
    - market close detection
    - holiday detection
    - candle boundary calculations
    - session timing helpers
    """

    from config.config import ( MARKET_OPEN_TIME, MARKET_CLOSE_TIME )

    def __init__(
        self,
        holiday_file: str
    ) -> None:

        self.logger = LoggingManager.get_logger(
            __name__
        )

        self.holiday_file = Path(
            MARKET_HOLIDAY_FILE
            )                       

        self.holidays: set[date] = set()

        self.load_holidays()

    def load_holidays(self) -> None:
        """
        Load holiday dates from file.
        """

        try:

            if not self.holiday_file.exists():

                self.logger.warning(
                    f"Holiday file missing: "
                    f"{self.holiday_file}"
                )

                return

            with open(
                self.holiday_file,
                "r",
                encoding="utf-8"
            ) as file:

                for line in file:

                    stripped = line.strip()

                    if not stripped:
                        continue

                    holiday_date = (
                        datetime.strptime(
                            stripped,
                            "%d/%m/%Y"
                        ).date()
                    )

                    self.holidays.add(
                        holiday_date
                    )

            self.logger.info(
                f"Loaded "
                f"{len(self.holidays)} "
                f"market holidays"
            )

        except Exception as error:

            self.logger.error(
                f"Holiday load failed: "
                f"{error}"
            )

    def is_market_holiday(
        self,
        check_date: Optional[date] = None
    ) -> bool:
        """
        Check whether date is a market holiday.
        """

        if check_date is None:

            check_date = datetime.now().date()

        return check_date in self.holidays

    def is_weekend(
        self,
        check_date: Optional[date] = None
    ) -> bool:
        """
        Check whether date is weekend.
        """

        if check_date is None:

            check_date = datetime.now().date()

        return check_date.weekday() >= 5

    def is_market_open(
        self,
        current_time: Optional[
            datetime
        ] = None
    ) -> bool:
        """
        Check whether market session is open.
        """

        if current_time is None:

            current_time = datetime.now()

        current_date = current_time.date()

        if self.is_weekend(current_date):

            return False

        if self.is_market_holiday(
            current_date
        ):

            return False

        current_clock = current_time.time()

        return (
            self.MARKET_OPEN_TIME
            <= current_clock
            <= self.MARKET_CLOSE_TIME
        )

    def get_current_session(
        self
    ) -> str:
        """
        Return current market session state.
        """

        now = datetime.now()

        if self.is_market_holiday():

            return "HOLIDAY"

        if self.is_weekend():

            return "WEEKEND"

        if now.time() < self.MARKET_OPEN_TIME:

            return "PRE_MARKET"

        if now.time() > self.MARKET_CLOSE_TIME:

            return "POST_MARKET"

        return "LIVE_MARKET"

    def get_next_market_open(
        self
    ) -> datetime:
        """
        Return next market open datetime.
        """

        current_date = datetime.now().date()

        next_day = current_date

        while True:

            next_day += timedelta(days=1)

            if self.is_weekend(next_day):
                continue

            if self.is_market_holiday(
                next_day
            ):
                continue

            return datetime.combine(
                next_day,
                self.MARKET_OPEN_TIME
            )

    def get_candle_start_time(
        self,
        timestamp: datetime,
        timeframe_minutes: int
    ) -> datetime:
        """
        Return candle start time.
        """

        minute = (
            timestamp.minute //
            timeframe_minutes
        ) * timeframe_minutes

        return timestamp.replace(
            minute=minute,
            second=0,
            microsecond=0
        )

    def get_candle_end_time(
        self,
        candle_start: datetime,
        timeframe_minutes: int
    ) -> datetime:
        """
        Return candle end time.
        """

        return candle_start + timedelta(
            minutes=timeframe_minutes
        )

    def seconds_until_market_open(
        self
    ) -> int:
        """
        Return seconds until next market open.
        """

        next_open = (
            self.get_next_market_open()
        )

        delta = next_open - datetime.now()

        return int(delta.total_seconds())
