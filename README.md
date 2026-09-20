# MC / ML for Scalping, Intraday, BTST & Swing

Research project studying whether Monte Carlo methods can improve the statistical validation and/or decision support of stock-trading systems across scalping, intraday, BTST and swing horizons.

## Current status
**Phase 3 — Baselines and Monte Carlo methodology: complete. Phase 4: blocked pending validated market data.**

Protocol, literature/data audit, cost engine, canonical data schema, baseline signals, Monte Carlo resamplers, tests and manual workflows are now in the repository. No stock-level profitability result has been fabricated.

## Research question
Can Monte Carlo methods be used as a statistically defensible component of trading systems for Indian equities across scalping, intraday, BTST and swing horizons, while remaining economically profitable after realistic brokerage, statutory charges, spread, slippage and execution frictions?

## Key finding so far
The evidence supports Monte Carlo mainly as a validation, resampling, uncertainty and risk framework. It is not evidence of guaranteed alpha. Robust profitability must be demonstrated with net out-of-sample data and multiple-testing controls.

## Phase progress
- Phase 0: complete
- Phase 1: complete
- Phase 2: partially complete; empirical high-resolution data access pending
- Phase 3: complete
- Phase 4: blocked pending validated market data
- Phase 5: pending
- Phase 6: pending

## Key files
RESEARCH_PROTOCOL.md; docs/RESEARCH_PLAN.md; docs/STATUS_PHASES.md; docs/LITERATURE_REVIEW.md; docs/DATA_SCHEMA.md; docs/DATA_ACQUISITION_MANIFEST.md; docs/COST_MODEL_2026.md; docs/PHASE3_METHODS.md; research_cost_engine.py; research_baselines.py; research_monte_carlo.py; test_cost_engine.py; test_monte_carlo.py
