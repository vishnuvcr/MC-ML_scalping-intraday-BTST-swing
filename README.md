# MC / ML for Scalping, Intraday, BTST & Swing

Research project studying whether Monte Carlo methods can improve the statistical validation and/or decision support of stock-trading systems across scalping, intraday, BTST and swing horizons.

## Current status
**Phase 0 — Governance and protocol:** In progress (2026-09-20, Asia/Kolkata).

Key project files: RESEARCH_PROTOCOL.md, docs/RESEARCH_PLAN.md, docs/RESEARCH_QUESTIONS.md, docs/STATUS_PHASES.md, docs/ERROR_LOG.md and docs/CHAT_LOG.md.

## Research question
Can Monte Carlo methods be used as a statistically defensible component of trading systems for Indian equities across scalping, intraday, BTST and swing horizons, while remaining economically profitable after realistic brokerage, statutory charges, spread, slippage and execution frictions?

## Planned phases
1. Governance, protocol and repository scaffolding
2. Literature review and data-source audit
3. Data engineering and execution-cost model
4. Baseline strategies and Monte Carlo methodology
5. Backtests, null tests and statistical inference
6. Robustness, regime and sensitivity analysis
7. Final synthesis, manuscript and reproducibility package

Each research phase will use a dedicated Git branch and a manually triggerable GitHub Actions workflow. Cached/derived datasets will be versioned rather than re-downloaded on every run where licensing and repository size permit.

## Important distinction
Monte Carlo is not assumed to be a profitable strategy by itself. The study will compare concrete Monte Carlo applications against non-Monte-Carlo baselines and determine whether any observed edge survives out-of-sample testing, multiple-testing controls and costs.

## Repo map
- RESEARCH_PROTOCOL.md
- docs/RESEARCH_PLAN.md
- docs/RESEARCH_QUESTIONS.md
- docs/STATUS_PHASES.md
- docs/ERROR_LOG.md
- docs/CHAT_LOG.md
- PROJECT_WORKING_RULES.md
- .github/workflows/phase-0-governance.yml
