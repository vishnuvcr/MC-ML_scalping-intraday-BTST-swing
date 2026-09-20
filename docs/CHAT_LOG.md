# Conversation / Decision Log

## 2026-09-20 — Research initiated
User request: study whether Monte Carlo methods can be used profitably/significantly for stock scalping, intraday, BTST and swing trading using the linked GitHub repository.

Material decisions:
- Treat Monte Carlo as a family of simulation/resampling methods, not a single trading strategy.
- Evaluate scalping, intraday, BTST and swing separately.
- Require realistic brokerage, statutory charges, spread and slippage; Paytm Money is the named broker context.
- Require out-of-sample testing, multiple-testing controls and robustness analysis.
- Use separate Git branches and manual workflows per research phase.
- Maintain a finite research plan and stop after the pre-specified phases.
- Record errors and research status in repository files after substantive steps.

Private chain-of-thought is not copied into project files. This log records requests, material decisions, evidence and outcomes in a reproducible decision-trace format.


## 2026-09-20 — continuation

User instructed: “Ok proceed”. Work continued from Phase 8. The repository state and workflow capability were rechecked. The large 214-symbol release could not be dispatched from the available GitHub interface, and the runtime cannot resolve GitHub's large-release host. A cross-market replication branch was therefore created using independently accessible public CSV panels. A corrected reproducible workflow/script was added, with explicit finite-value aggregation and deterministic Monte-Carlo seeds. Public BSE replication showed negative 2025 test medians at 5 bps/leg for both BTST and swing. No hidden/internal reasoning is copied here; only auditable actions and results are recorded.
