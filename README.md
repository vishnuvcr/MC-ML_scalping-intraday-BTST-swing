# MC / ML for Scalping, Intraday, BTST & Swing

Research project studying whether Monte Carlo methods can improve the statistical validation and/or decision support of stock-trading systems across scalping, intraday, BTST and swing horizons.

## Current status
**Phase 1 — Literature and data audit:** In progress (2026-09-20, Asia/Kolkata).

Phase 0 governance is merged into `main`. Phase 1 currently contains the literature evidence map, data-source audit, source registry, phase status tracker, and manual workflow.

## Research question
Can Monte Carlo methods be used as a statistically defensible component of trading systems for Indian equities across scalping, intraday, BTST and swing horizons, while remaining economically profitable after realistic brokerage, statutory charges, spread, slippage and execution frictions?

## Planned phases
1. Governance, protocol and repository scaffolding — complete
2. Literature review and data-source audit — in progress
3. Data engineering and execution-cost model
4. Baseline strategies and Monte Carlo methodology
5. Backtests, null tests and statistical inference
6. Robustness, regime and sensitivity analysis
7. Final synthesis, manuscript and reproducibility package

## Key Phase 1 finding
The literature supports Monte Carlo mainly as a resampling, uncertainty, validation and risk-analysis framework. Profitability claims need independent out-of-sample evidence and controls for dependence, data snooping, multiple testing and execution costs.

## Repo map
- RESEARCH_PROTOCOL.md
- docs/RESEARCH_PLAN.md
- docs/RESEARCH_QUESTIONS.md
- docs/STATUS_PHASES.md
- docs/LITERATURE_REVIEW.md
- docs/DATA_SOURCE_AUDIT.md
- docs/SOURCE_REGISTRY.md
- docs/ERROR_LOG.md
- docs/CHAT_LOG.md
- PROJECT_WORKING_RULES.md
- .github/workflows/phase-0-governance.yml
- .github/workflows/phase-1-literature-data-audit.yml
