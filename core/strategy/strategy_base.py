# core/strategy/strategy_base.py

from abc import ABC, abstractmethod

from core.logging_manager import LoggingManager

from core.signals.signal import Signal

from core.strategy.trade_intent import TradeIntent


class StrategyBase(ABC):
    """
    Base class for all trading strategies.

    Responsibilities:
    - signal handling contract
    - strategy state management
    - entry/exit lifecycle
    - runtime state tracking
    """

    VALID_STATES = {"IDLE", "LONG", "SHORT", "EXITED"}

    def __init__(self, name: str, symbol: str, timeframe: str) -> None:

        self.logger = LoggingManager.get_logger(__name__)

        self.name = name

        self.symbol = symbol

        self.timeframe = timeframe

        self.state = "IDLE"

        self.ready = False

        self.total_signals_processed = 0

        self.last_signal: Signal | None = None

    @abstractmethod
    def on_signal(self, signal: Signal) -> TradeIntent | None:
        """
        Process incoming signal.

        Returns:
            Strategy action signal.
        """

        pass

    @abstractmethod
    def should_enter(self, signal: Signal) -> bool:
        """
        Determine entry condition.
        """

        pass

    @abstractmethod
    def should_exit(self, signal: Signal) -> bool:
        """
        Determine exit condition.
        """

        pass

    @abstractmethod
    def reset(self) -> None:
        """
        Reset strategy state.
        """

        pass

    def set_state(self, state: str) -> None:
        """
        Update strategy state.
        """

        normalized = state.upper().strip()

        if normalized not in self.VALID_STATES:
            raise ValueError(f"Invalid strategy state: {normalized}")

        self.state = normalized

    def get_state(self) -> str:
        """
        Return strategy state.
        """

        return self.state

    def is_idle(self) -> bool:
        """
        Check idle state.
        """

        return self.state == "IDLE"

    def is_long(self) -> bool:
        """
        Check long state.
        """

        return self.state == "LONG"

    def is_short(self) -> bool:
        """
        Check short state.
        """

        return self.state == "SHORT"

    def is_exited(self) -> bool:
        """
        Check exited state.
        """

        return self.state == "EXITED"

    def get_name(self) -> str:
        """
        Return strategy name.
        """

        return self.name

    def get_full_name(self) -> str:
        """
        Return unique strategy identifier.
        """

        return f"{self.symbol}_{self.timeframe}_{self.name}"

    def get_symbol(self) -> str:
        """
        Return strategy symbol.
        """

        return self.symbol

    def get_timeframe(self) -> str:
        """
        Return strategy timeframe.
        """

        return self.timeframe

    def get_last_signal(self) -> Signal | None:
        """
        Return last processed signal.
        """

        return self.last_signal

    def set_last_signal(self, signal: Signal) -> None:
        """
        Store last processed signal.
        """

        self.last_signal = signal

    def increment_signal_count(self) -> None:
        """
        Increment processed signal count.
        """

        self.total_signals_processed += 1

    def get_total_signals_processed(self) -> int:
        """
        Return processed signal count.
        """

        return self.total_signals_processed

    def mark_ready(self) -> None:
        """
        Mark strategy ready.
        """

        self.ready = True

    def is_ready(self) -> bool:
        """
        Return readiness state.
        """

        return self.ready
