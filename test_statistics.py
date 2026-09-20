import numpy as np
from research_statistics import max_drawdown, annualized_sharpe, profit_factor, block_bootstrap_ci


def test_metrics_are_finite_on_nonconstant_data():
    r = np.array([0.01, -0.005, 0.02, -0.01, 0.005])
    assert max_drawdown(r) <= 0
    assert np.isfinite(annualized_sharpe(r, 252))
    assert profit_factor(r) > 0


def test_block_bootstrap_ci_contains_reasonable_scale():
    rng = np.random.default_rng(1)
    r = rng.normal(0.0005, 0.01, 250)
    lo, hi = block_bootstrap_ci(r, statistic=np.mean, n_paths=200, block_mean=10, seed=2)
    assert lo < hi
    assert -0.01 < lo < 0.01
    assert -0.01 < hi < 0.01
