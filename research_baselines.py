def moving_average_signal(close, fast=20, slow=50):
    fast_ma = close.rolling(fast).mean()
    slow_ma = close.rolling(slow).mean()
    return (fast_ma > slow_ma).astype(int)


def breakout_signal(high, close, lookback=20):
    prior_high = high.shift(1).rolling(lookback).max()
    return (close > prior_high).astype(int)


def mean_reversion_signal(close, lookback=20, z=1.5):
    mean = close.rolling(lookback).mean()
    std = close.rolling(lookback).std(ddof=0)
    score = (close - mean) / std.replace(0, float('nan'))
    return (score < -z).astype(int)
