# Research Phase Status

Updated: 20 September 2026

| Phase | Branch | Status | Result |
|---|---|---|---|
| 0 Governance | phase-0-governance | COMPLETE | Governance and auditability established. |
| 1 Literature/Data Audit | phase-1-literature-data-audit | COMPLETE | Literature, public sources and data requirements documented. |
| 2 Data/Cost Engine | phase-2-data-cost-engine | COMPLETE FOR AVAILABLE PUBLIC DATA | Cost-aware engine established; licensed microstructure data unavailable. |
| 3 Baselines/Monte Carlo | phase-3-baselines-monte-carlo | COMPLETE | Baselines and MC gate specified and tested. |
| 4 Statistical Inference | phase-4-statistical-inference | COMPLETE FOR FINITE PUBLIC SCREEN | Statistical/OOS framework applied to available data. |
| 5 Robustness Design | phase-5-robustness-design | COMPLETE FOR AVAILABLE DATA | Cost/slippage and replication controls applied; microstructure robustness remains data-limited. |
| 6 Final Synthesis | phase-6-final-synthesis | SUPERSEDED BY PHASE 8 EVIDENCE UPDATE | Final synthesis amended after empirical replication. |
| 7 Empirical Screening | phase-7-empirical-screening | COMPLETE | No universal robust strategy; TCS intraday remains exploratory candidate. |
| 8 Public Data Expansion | phase-8-public-data-expansion | COMPLETE WITH EXECUTION LIMITATION | Corrected 8-symbol screen complete; large 1-minute/F&O and TejHQ workflow artifacts not observable from current interface. |
| 8 Cross-Market Replication | phase-8-crossmarket-replication | COMPLETE | Historical NSE and BSE daily replication fail the robustness gate at 5 bps/leg. |
| 8 Final Synthesis | phase-8-final-synthesis | COMPLETE | Final evidence gate closed; manuscript updated; no universal strategy promoted. |

## Final scientific conclusion

No universally consistent, cost-aware, out-of-sample-robust strategy was established across scalping, intraday, BTST and swing.

Monte Carlo remains supported as a validation/participation/risk-control layer rather than a stand-alone alpha source.

The strongest remaining candidate is a TCS 15-minute EMA20/26 intraday system. It is a paper-trading research candidate only, not a live-validated or universal strategy.

## Evidence gate

See [docs/FINAL_EVIDENCE_GATE_PHASE8.md](FINAL_EVIDENCE_GATE_PHASE8.md).

## Final manuscript

See [manuscript/FINAL_RESEARCH_REPORT.md](../manuscript/FINAL_RESEARCH_REPORT.md).

## Future evidence required

- 1-minute/tick/bid-ask data for scalping/intraday.
- Broader point-in-time NSE/BSE universe for BTST/swing.
- Independent future holdout and execution-quality measurement.


## Phase 9 — universe, stock-selection, regime and cross-market analysis

**Status: ACTIVE.** The TCS +14.33% result is explicitly treated as single-stock evidence. Phase 9 now tests the frozen framework on an exact NIFTY-100 15-minute panel plus the full available NSE daily universe, with pre-specified liquidity/volatility/trend/regime/cross-market factors. See [PHASE9_PLAN.md](PHASE9_PLAN.md), [PHASE9_RESULTS.md](PHASE9_RESULTS.md), and [PHASE9_MANUSCRIPT_ADDENDUM.md](PHASE9_MANUSCRIPT_ADDENDUM.md).


## Phase 9.1 — Ganesh Nifty500 intraday replication

**Status: ACTIVE.** A 499-symbol intersection of the 2018-2025 and 2026 Ganesh Nifty500 1-minute datasets is now the primary exact broad-intraday replication panel. The frozen TCS 15-minute EMA20/26 candidate is being tested across the panel with stock-selection, liquidity, volatility, trend, beta/residual-risk, market-regime, breadth/dispersion and time-of-day factors. See [Phase 9 plan](PHASE9_PLAN.md) and [Ganesh source registry](DATA_SOURCE_REGISTRY_PHASE9.md).


## Phase 9.2 — 2026-only Nifty500 forward path

**Status: ACTIVE.** Uses the 535-file 2026 Ganesh Nifty500 1-minute panel and the frozen EMA20/26 intraday system. It splits 2026 into an early calibration window, March-April primary conditional test, and May-onward holdout; lagged NSE-BSE basis from TejHQ is included as a pre-trade factor. No result is accepted until the workflow completes.

## Phase 10 — Global-market information / cross-market inefficiency

Status: ACTIVE. Global-market scope is explicit. The first candidate is a prior-session five-market sign-consensus >= +3 filter applied to the frozen Indian EMA20/26 intraday framework. Historical and independent-source pilots support the hypothesis, but the currently synchronized 2026 independent sample is small and does not support promotion.

See [PHASE10_PLAN.md](PHASE10_PLAN.md), [PHASE10_RESULTS.md](PHASE10_RESULTS.md), and [phase-10-global-market-inefficiency.yml](../.github/workflows/phase-10-global-market-inefficiency.yml).

## Phase 9 correction gate

The initial Ganesh Nifty500 workflow is not accepted as final empirical evidence. Corporate-action scaling, MC-gate history and overlapping-position accounting were corrected; a fresh workflow artifact is required before Phase 9 can close.