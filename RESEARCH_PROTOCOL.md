# Research Protocol — Monte Carlo for Stock Trading

## Status
Bootstrap in progress (2026-09-20, Asia/Kolkata).

## Research question
Can Monte Carlo methods be used as a statistically defensible component of profitable and robust trading systems for stocks across scalping, intraday, BTST, and swing horizons, after accounting for transaction costs, brokerage, taxes/fees where applicable, slippage, liquidity, and model/data uncertainty?

## Core principle
Monte Carlo is a family of resampling/simulation methods, not a trading strategy by itself. The study will test specific Monte Carlo uses against appropriate baselines and out-of-sample controls.

## Required controls
- No look-ahead bias and no leakage across train/test boundaries.
- Point-in-time data handling and corporate-action adjustments.
- Explicit brokerage, statutory charges, spread and slippage assumptions; Paytm Money cost assumptions must be sourced and versioned.
- Multiple-testing and data-snooping controls.
- Block/bootstrap methods suitable for dependent financial returns, not only IID shuffles.
- Walk-forward and, where appropriate, purged/embargoed cross-validation.
- Null-model and placebo tests.
- Robustness across securities, market regimes, periods, and trading horizons.

## Evidence standard
A result is considered useful only if it survives the pre-specified statistical tests and remains positive after realistic costs and conservative execution assumptions. Statistical significance alone is insufficient; economic significance, stability and reproducibility are required.

## Deliverables
1. Research protocol and hypotheses.
2. Literature/data inventory.
3. Reproducible data pipeline with cached datasets.
4. Baseline strategies and Monte Carlo variants.
5. Statistical evaluation and robustness/stress tests.
6. Final research manuscript with tables, charts, appendices and limitations.

## Phases
- Phase 0 — Governance, protocol, repository scaffolding.
- Phase 1 — Literature review and data-source audit.
- Phase 2 — Data engineering and execution-cost model.
- Phase 3 — Baselines and Monte Carlo methodology.
- Phase 4 — Backtests, null tests and statistical inference.
- Phase 5 — Robustness, sensitivity and regime analysis.
- Phase 6 — Final synthesis, manuscript and reproducibility package.

Each phase uses a dedicated Git branch and has a manual GitHub Actions workflow. Progress, errors and key decisions are logged after each substantive step.
