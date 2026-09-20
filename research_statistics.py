import numpy as np


def max_drawdown(returns):
    equity = np.cumprod(1.0 + np.asarray(returns, dtype=float))
    peaks = np.maximum.accumulate(equity)
    return float(np.min(equity / peaks - 1.0))


def annualized_sharpe(returns, periods_per_year):
    r = np.asarray(returns, dtype=float)
    if r.size < 2 or np.std(r, ddof=1) == 0:
        return np.nan
    return float(np.sqrt(periods_per_year) * np.mean(r) / np.std(r, ddof=1))


def annualized_sortino(returns, periods_per_year):
    r = np.asarray(returns, dtype=float)
    downside = r[r < 0]
    if r.size < 2 or downside.size == 0 or np.std(downside, ddof=0) == 0:
        return np.nan
    return float(np.sqrt(periods_per_year) * np.mean(r) / np.std(downside, ddof=0))


def profit_factor(trade_returns):
    r = np.asarray(trade_returns, dtype=float)
    losses = -r[r < 0].sum()
    gains = r[r > 0].sum()
    return float(gains / losses) if losses > 0 else np.inf


def block_bootstrap_ci(values, statistic=np.mean, n_paths=5000, block_mean=20, alpha=0.05, seed=20260920):
    x = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    n = x.size
    p = 1.0 / block_mean
    stats = np.empty(n_paths)
    for b in range(n_paths):
        sample = np.empty(n)
        i = rng.integers(0, n)
        for t in range(n):
            sample[t] = x[i]
            i = rng.integers(0, n) if rng.random() < p else (i + 1) % n
        stats[b] = statistic(sample)
    return float(np.quantile(stats, alpha / 2)), float(np.quantile(stats, 1 - alpha / 2))
