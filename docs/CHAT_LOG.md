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


## 2026-09-20 — final synthesis
The finite public-data protocol was closed. Phase 8 cross-source daily replication failed the robustness gate at 5 bps/leg. The final manuscript, evidence gate, cross-market script/workflow, final synthesis workflow and status artifacts were synchronized to main. No universal live-ready strategy was promoted.
## 2026-09-20 — global-market scope correction and Phase 10

User clarified that cross-market inefficiency includes global markets, not only NSE/BSE. The research scope was amended accordingly. A 2010–2022 pilot and an independent 2006–2026 global-index pilot were evaluated; the global-consensus hypothesis is now frozen for OOS testing rather than being further tuned.

During Phase 9 troubleshooting, the initial Ganesh Nifty500 aggregate was found invalid because of an mc_return/mc_ret column mismatch and additional corporate-action / accounting defects. Those corrections were logged and synced before further empirical claims.