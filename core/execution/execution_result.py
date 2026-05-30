# core/execution/execution_result.py

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class ExecutionResult:
    """
    Result of a paper execution.
    """

    success: bool

    symbol: str

    side: str

    quantity: int

    fill_price: float

    timestamp: datetime

    message: str
    
    position_opened: bool = False

    position_closed: bool = False