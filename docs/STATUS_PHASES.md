# Research Phase Status

Updated: 2026-09-20

- Phase 0 — Governance: COMPLETE (merged to main)
- Phase 1 — Literature and data audit: COMPLETE
- Phase 2 — Data and execution-cost engine: PARTIALLY COMPLETE
- Phase 3 — Baselines and Monte Carlo methods: NOT STARTED
- Phase 4 — Backtests and statistical inference: NOT STARTED
- Phase 5 — Robustness and regime analysis: NOT STARTED
- Phase 6 — Final synthesis and manuscript: NOT STARTED

## Phase 2 completed
- Versioned, direction-aware cost engine implemented in Python.
- Unit tests pass locally.
- Current NSE statutory rates and current transaction-cost assumptions documented.
- Paytm Money brokerage treated as a versioned input; live calculator/account terms remain the final broker-specific verification source.
- Canonical data schema and acquisition manifest defined.
- Manual GitHub Actions workflow added.

## Phase 2 blocker
Empirical high-resolution datasets for scalping/intraday are not yet acquired in this repository because exchange/vendor licensing and access terms must be verified. No empirical profitability claim is made from synthetic or undocumented data.

## Next gate
Proceed to Phase 3 strategy/Monte Carlo implementation while retaining the Phase 4 empirical-backtest gate until licensed/validated market data are available.
