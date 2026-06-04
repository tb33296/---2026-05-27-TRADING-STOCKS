# tests/test_indicator_signal_runtime.py

from datetime import datetime

from core.market_data.candle import Candle

from core.indicators.moving_average import MovingAverage

from runtime.indicator_runtime import IndicatorRuntime

from runtime.signal_runtime import SignalRuntime

from core.signals.crossover_signal import CrossoverSignal


def test_indicator_signal_runtime() -> None:

    print("\n=== INDICATOR -> SIGNAL TEST ===\n")

    # ----------------------------------
    # Runtime Setup
    # ----------------------------------

    indicator_runtime = IndicatorRuntime()

    signal_runtime = SignalRuntime()

    # ----------------------------------
    # Indicators
    # ----------------------------------

    ema_fast = MovingAverage(
        name="EMA3", symbol="RELIANCE", timeframe="1m", period=3, ma_type="EMA"
    )

    ema_slow = MovingAverage(
        name="EMA5", symbol="RELIANCE", timeframe="1m", period=5, ma_type="EMA"
    )

    indicator_runtime.register_indicator(ema_fast)

    indicator_runtime.register_indicator(ema_slow)

    # ----------------------------------
    # Signal Generator
    # ----------------------------------

    crossover_signal = CrossoverSignal(
        name="EMA_CROSS", fast_indicator=ema_fast, slow_indicator=ema_slow
    )

    signal_runtime.register_crossover_signal("EMA_CROSS", crossover_signal)

    # ----------------------------------
    # Price Series
    # ----------------------------------

    prices = [100, 99, 98, 97, 96, 110, 120, 130]

    generated_signals = []

    # ----------------------------------
    # Feed Closed Candles
    # ----------------------------------

    for price in prices:
        candle = Candle(
            symbol="RELIANCE",
            timeframe="1m",
            open=price,
            high=price,
            low=price,
            close=price,
            volume=100,
            start_time=datetime.now(),
            end_time=datetime.now(),
            is_closed=True,
        )

        indicator_runtime.process_closed_candle(candle)

        signals = signal_runtime.evaluate_signals()

        if signals:
            generated_signals.extend(signals)

            for signal in signals:
                print(f"Signal Generated: {signal.signal_type}")

    # ----------------------------------
    # Validation
    # ----------------------------------

    print()

    print(f"EMA3 Ready: {ema_fast.is_ready()}")

    print(f"EMA5 Ready: {ema_slow.is_ready()}")

    print(f"EMA3 Value: {ema_fast.get_value()}")

    print(f"EMA5 Value: {ema_slow.get_value()}")

    print(f"Signals Generated: {len(generated_signals)}")

    assert ema_fast.is_ready()

    assert ema_slow.is_ready()

    assert len(generated_signals) >= 1

    print("\n=== TEST COMPLETE ===")
