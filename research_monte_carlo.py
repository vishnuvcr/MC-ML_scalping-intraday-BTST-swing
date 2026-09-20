import numpy as np


def iid_trade_bootstrap(trade_returns, n_paths=5000, seed=20260920):
    x = np.asarray(trade_returns, dtype=float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), size=(n_paths, len(x)))
    return x[idx]


def stationary_bootstrap(x, n_paths=5000, block_mean=20, seed=20260920):
    x = np.asarray(x, dtype=float)
    rng = np.random.default_rng(seed)
    n = len(x)
    p = 1.0 / block_mean
    out = np.empty((n_paths, n), dtype=float)
    for b in range(n_paths):
        i = rng.integers(0, n)
        for t in range(n):
            out[b, t] = x[i]
            if rng.random() < p:
                i = rng.integers(0, n)
            else:
                i = (i + 1) % n
    return out


def permutation_null(signal, future_return, n_paths=5000, seed=20260920):
    s = np.asarray(signal)
    r = np.asarray(future_return, dtype=float)
    if len(s) != len(r):
        raise ValueError('signal and future_return must have equal length')
    rng = np.random.default_rng(seed)
    out = np.empty((n_paths, len(r)), dtype=float)
    for b in range(n_paths):
        out[b] = r[rng.permutation(len(r))]
    return out


def max_drawdown(equity):
    equity = np.asarray(equity, dtype=float)
    peaks = np.maximum.accumulate(equity)
    return np.min(equity / peaks - 1.0)


def bootstrap_drawdown(trade_returns, n_paths=5000, method='iid', seed=20260920):
    paths = iid_trade_bootstrap(trade_returns, n_paths, seed) if method == 'iid' else stationary_bootstrap(trade_returns, n_paths, seed=seed)
    equity = np.cumprod(1.0 + paths, axis=1)
    return np.array([max_drawdown(row) for row in equity])
