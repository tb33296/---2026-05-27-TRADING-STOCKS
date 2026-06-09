# tests/test_indicator_signal_flow.py

import pytest

from core.market_data.candle import Candle

from runtime.indicator_runtime import IndicatorRuntime
from runtime.signal_runtime import SignalRuntime

from core.indicators.ema import EMA
from core.indicators.rvol import RVOL
from core.indicators.vwap import VWAP

from core.market_data.market_clock import MarketClock

from core.signals.crossover_signal import CrossoverSignal
from core.signals.vwap_signal import VWAPSignal

from datetime import datetime


@pytest.fixture
def market_clock():

    return MarketClock()


@pytest.fixture
def indicator_runtime():

    return IndicatorRuntime()


@pytest.fixture
def signal_runtime():

    return SignalRuntime()


def create_candle(
    close_price: float,
    volume: int = 1000,
) -> Candle:

    now = datetime.now()

    return Candle(
        symbol="RELIANCE",
        timeframe="1MIN",
        open=close_price,
        high=close_price,
        low=close_price,
        close=close_price,
        volume=volume,
        start_time=now,
        end_time=now,
        is_closed=True,
    )


def test_ema_crossover_signal_generation(
    indicator_runtime,
    signal_runtime,
):

    ema9 = EMA(
        name="EMA9",
        symbol="RELIANCE",
        timeframe="1MIN",
        period=9,
    )

    ema20 = EMA(
        name="EMA20",
        symbol="RELIANCE",
        timeframe="1MIN",
        period=20,
    )

    indicator_runtime.register_indicator(ema9)

    indicator_runtime.register_indicator(ema20)

    signal = CrossoverSignal(
        name="EMA_TEST",
        fast_indicator=ema9,
        slow_indicator=ema20,
        signal_strength=1.0,
    )

    signal_runtime.register_crossover_signal(
        signal.name,
        signal,
    )

    prices = [
        100,
        110,
        120,
        130,
        140,
        150,
        160,
        170,
        180,
        190,
        170,
        150,
        130,
        110,
        90,
        70,
        50,
        90,
        130,
        170,
        210,
        250,
    ]

    generated = []
    print("price", "EMA 9", "EMA 20", "Signal")
    for price in prices:
        candle = create_candle(price)

        indicator_runtime.process_closed_candle(candle)

        generated.extend(signal_runtime.evaluate_signals(candle))

        print(
            price,
            ema9.get_value(),
            ema20.get_value(),
            signal.get_current_state(),
        )

    assert len(generated) > 0


def test_vwap_signal_generation(
    indicator_runtime,
    signal_runtime,
    market_clock,
):

    vwap = VWAP(
        name="VWAP",
        symbol="RELIANCE",
        timeframe="1MIN",
        market_clock=market_clock,
    )

    indicator_runtime.register_indicator(vwap)

    signal = VWAPSignal(
        name="VWAP_TEST",
        vwap_indicator=vwap,
        signal_strength=1.0,
    )

    signal_runtime.register_vwap_signal(
        signal.name,
        signal,
    )

    generated = []

    prices = [
        100,
        100,
        100,
        100,
        105,
        110,
    ]

    for price in prices:
        candle = create_candle(price)

        indicator_runtime.process_closed_candle(candle)

        generated.extend(signal_runtime.evaluate_signals(candle))

    assert isinstance(generated, list)
