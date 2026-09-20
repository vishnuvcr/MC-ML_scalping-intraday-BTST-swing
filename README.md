# MC / ML for Scalping, Intraday, BTST & Swing

Research project studying whether Monte Carlo methods can improve the statistical validation and/or decision support of stock-trading systems across scalping, intraday, BTST and swing horizons.

## Current status
**Phase 8 public-data expansion in progress — no universally robust strategy has been established.**

Public Kaggle, Hugging Face, TejHQ and GitHub sources are now part of the protocol. The corrected interim 8-symbol screen is negative for the frozen EMA framework at 5 bps/leg; the independent 214-symbol 1-minute + TejHQ daily run is configured for cached GitHub Actions execution.

The empirical gate was reopened with a secondary public OHLCV dataset. The research then ran a finite strategy screen with transaction costs, brokerage assumptions and Monte Carlo gating. The screen was closed after the pre-specified candidate families failed to produce a robust positive strategy across all four horizons.

## Strongest candidate
A TCS 15-minute EMA20/26 trend system with a 1.5 ATR stop and Monte Carlo participation gate produced +5.59% out-of-sample over 40 trades, PF 1.71, Sharpe 1.17 and max drawdown -2.94%. A longer-hold intraday version produced +14.33%, PF 2.87, Sharpe 2.10 and max drawdown -1.92% over 40 trades. These are research candidates, not live-validated strategies, because the data are 15-minute OHLCV rather than tick/bid-ask data and the result is concentrated in one symbol.

## BTST and swing
The corrected true BTST test (next-open to next-close) did not persist from validation to test. No BTST strategy is classified as usable. A daily HDFCBANK EMA20/21 swing candidate was only weakly positive out of sample (+0.94%, PF 1.08) and is not robust enough for live classification.

## Monte Carlo finding
Monte Carlo consistently acted more like a participation/risk filter than a source of alpha. It reduced trade counts and often reduced drawdown, but did not consistently increase returns. The strongest empirical candidate still depends on the underlying EMA signal.

## Important corrections
- The true BTST holding period was re-run after detecting an earlier 8-day holding-period mismatch.
- A 52-week-high/momentum experiment with overlapping positions was rejected after detecting invalid capital-accounting; its apparently huge returns are excluded.
- 15-minute data are explicitly treated as a scalping proxy, not true scalping evidence.

## Research conclusion
No single consistent, cost-aware and out-of-sample-robust strategy has been established across scalping, intraday, BTST and swing in this finite study. The evidence does support a concrete TCS intraday/15-minute research candidate, but continuing to search indicators on the same sample would become uncontrolled data-mining. Stronger claims require 1-minute/tick/bid-ask data and a broader point-in-time stock universe.

## Key files
- `docs/EMPIRICAL_SCREENING_RESULTS.md`
- `docs/STATUS_PHASES.md`
- `docs/ERROR_LOG.md`
- `manuscript/FINAL_RESEARCH_REPORT.md`
- `research_monte_carlo.py`
- `research_cost_engine.py`
- `.github/workflows/phase-0-governance.yml` through `.github/workflows/phase-6-final-synthesis.yml`


## Phase 8 public-data expansion
- `docs/PHASE8_PUBLIC_DATA_PLAN.md` (phase-8-public-data-expansion)
- `docs/DATA_SOURCE_REGISTRY_PHASE8.md`
- `docs/PHASE8_RESULTS.md`
- `docs/ERROR_LOG_PHASE8.md`
- `scripts/phase8_public_data_screen.py`
- `.github/workflows/phase-8-public-data-expansion.yml`
