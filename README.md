# MC / ML for Scalping, Intraday, BTST & Swing

Research project studying whether Monte Carlo methods can improve the statistical validation and/or decision support of stock-trading systems across scalping, intraday, BTST and swing horizons.

## Current status
**Phase 2 — Data and execution-cost engine: partially complete (2026-09-20).**

Phase 0 and Phase 1 are complete. The cost engine and data schema are reproducibly implemented and tested. High-resolution empirical data access remains a documented gate for final scalping/intraday profitability inference.

## Research question
Can Monte Carlo methods be used as a statistically defensible component of trading systems for Indian equities across scalping, intraday, BTST and swing horizons, while remaining economically profitable after realistic brokerage, statutory charges, spread, slippage and execution frictions?

## Key findings so far
Monte Carlo is strongest as a validation, resampling, uncertainty and risk-analysis framework; it is not assumed to create alpha by itself. Current NSE charges and execution costs can be material, especially for short-horizon trading. For a ₹100,000/₹100,000 round trip, the provisional model gives about ₹82.68 intraday cost before spread/slippage and about ₹182.68 with 2 bps spread plus 3 bps slippage per leg. These are arithmetic illustrations, not trading results.

## Phase progress
1. Governance, protocol and repository scaffolding — complete
2. Literature review and data-source audit — complete
3. Data engineering and execution-cost model — partially complete; empirical high-resolution data access pending
4. Baseline strategies and Monte Carlo methodology — next
5. Backtests, null tests and statistical inference
6. Robustness, regime and sensitivity analysis
7. Final synthesis, manuscript and reproducibility package

## Repo map
- RESEARCH_PROTOCOL.md
- docs/RESEARCH_PLAN.md
- docs/RESEARCH_QUESTIONS.md
- docs/STATUS_PHASES.md
- docs/LITERATURE_REVIEW.md
- docs/DATA_SOURCE_AUDIT.md
- docs/DATA_SCHEMA.md
- docs/DATA_ACQUISITION_MANIFEST.md
- docs/COST_MODEL_2026.md
- docs/COST_SENSITIVITY_ILLUSTRATION.md
- COST_CONFIG_2026.txt
- research_cost_engine.py
- test_cost_engine.py
- docs/SOURCE_REGISTRY.md
- docs/ERROR_LOG.md
- docs/CHAT_LOG.md
- PROJECT_WORKING_RULES.md
- .github/workflows/phase-0-governance.yml
- .github/workflows/phase-1-literature-data-audit.yml
- .github/workflows/phase-2-data-cost-engine.yml
