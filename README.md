# MC / ML for Scalping, Intraday, BTST & Swing

Research project studying whether Monte Carlo methods can improve the statistical validation and/or decision support of stock-trading systems across scalping, intraday, BTST and swing horizons.

## Current status
**Phase 1 — Literature and data audit: complete (2026-09-20).**

Phase 0 governance and Phase 1 evidence/data audits are documented and ready for the Phase 2 data-engineering gate.

## Research question
Can Monte Carlo methods be used as a statistically defensible component of trading systems for Indian equities across scalping, intraday, BTST and swing horizons, while remaining economically profitable after realistic brokerage, statutory charges, spread, slippage and execution frictions?

## Key finding so far
Monte Carlo is not treated as a stand-alone source of guaranteed trading alpha. Its strongest research role is validation, resampling, uncertainty quantification, null testing and drawdown/risk analysis. Strategy profitability must be demonstrated separately and must survive dependence-aware inference, data-snooping controls and realistic execution costs.

## Phase progress
1. Governance, protocol and repository scaffolding — complete
2. Literature review and data-source audit — complete
3. Data engineering and execution-cost model — next
4. Baseline strategies and Monte Carlo methodology
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
- docs/SOURCE_REGISTRY.md
- docs/ERROR_LOG.md
- docs/CHAT_LOG.md
- PROJECT_WORKING_RULES.md
- .github/workflows/phase-0-governance.yml
- .github/workflows/phase-1-literature-data-audit.yml
