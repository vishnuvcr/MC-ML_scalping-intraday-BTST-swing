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
