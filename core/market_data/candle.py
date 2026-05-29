# core/market_data/candle.py

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Candle:
    """
    Represents a market OHLCV candle.
    """

    symbol: str

    timeframe: str

    open: float

    high: float

    low: float

    close: float

    volume: int

    start_time: datetime

    end_time: datetime

    is_closed: bool = False

    def update(
        self,
        price: float,
        volume: int
    ) -> None:
        """
        Update candle with incoming tick data.
        """

        if price > self.high:

            self.high = price

        if price < self.low:

            self.low = price

        self.close = price

        self.volume += volume

    def close_candle(self) -> None:
        """
        Mark candle as closed.
        """

        self.is_closed = True

    def to_dict(self) -> dict:
        """
        Convert candle to dictionary.
        """

        return {
            "symbol": self.symbol,

            "timeframe": self.timeframe,

            "open": self.open,

            "high": self.high,

            "low": self.low,

            "close": self.close,

            "volume": self.volume,

            "start_time": self.start_time,

            "end_time": self.end_time,

            "is_closed": self.is_closed
        }

    @classmethod
    def from_tick(
        cls,
        symbol: str,
        timeframe: str,
        price: float,
        volume: int,
        start_time: datetime,
        end_time: datetime
    ) -> "Candle":
        """
        Create candle from first tick.
        """

        return cls(
            symbol=symbol,

            timeframe=timeframe,

            open=price,

            high=price,

            low=price,

            close=price,

            volume=volume,

            start_time=start_time,

            end_time=end_time,

            is_closed=False
        )

