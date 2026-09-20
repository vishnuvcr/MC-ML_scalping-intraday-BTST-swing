import numpy as np
from research_monte_carlo import iid_trade_bootstrap, stationary_bootstrap, permutation_null, bootstrap_drawdown


def test_shapes_and_reproducibility():
    x = np.array([0.01, -0.005, 0.02, -0.01])
    a = iid_trade_bootstrap(x, 100, 123)
    b = iid_trade_bootstrap(x, 100, 123)
    assert a.shape == (100, 4)
    assert np.array_equal(a, b)


def test_stationary_bootstrap_shape():
    x = np.linspace(-0.01, 0.01, 20)
    paths = stationary_bootstrap(x, 50, block_mean=5, seed=1)
    assert paths.shape == (50, 20)


def test_permutation_null_preserves_values():
    s = np.array([1, 0, 1, 0, 1])
    r = np.array([0.1, -0.1, 0.2, -0.2, 0.05])
    paths = permutation_null(s, r, 25, 2)
    assert paths.shape == (25, 5)
    assert np.all(np.sort(paths, axis=1) == np.sort(r))


def test_drawdown_is_non_positive():
    x = np.array([0.02, -0.01, 0.03, -0.02])
    dd = bootstrap_drawdown(x, 100, 'iid', 3)
    assert np.all(dd <= 1e-12)
