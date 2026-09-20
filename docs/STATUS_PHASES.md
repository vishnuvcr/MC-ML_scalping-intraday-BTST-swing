# Research Phase Status

Updated: 2026-09-20

- Phase 0 — Governance: COMPLETE
- Phase 1 — Literature and data audit: COMPLETE
- Phase 2 — Data and execution-cost engine: PARTIALLY COMPLETE
- Phase 3 — Baselines and Monte Carlo methods: COMPLETE
- Phase 4 — Backtests and statistical inference: EMPIRICALLY SCREENED ON SECONDARY PUBLIC OHLCV
- Phase 5 — Robustness and regime analysis: EMPIRICALLY SCREENED ON SECONDARY PUBLIC OHLCV; FULL MICROSTRUCTURE ROBUSTNESS NOT POSSIBLE
- Phase 6 — Final synthesis and manuscript: COMPLETE
- Phase 7 — Empirical re-opening and finite strategy screen: COMPLETE
- Phase 8 — Public-data expansion and cross-source validation: IN PROGRESS (source audit + corrected 8-symbol interim screen complete; independent 214-symbol/TejHQ GitHub Actions run pending)

## Phase 7 outcome
A common Monte Carlo-gated EMA framework was tested across scalping (15-minute proxy), intraday, true one-overnight BTST, and swing. Alternative breakout, mean-reversion, VWAP, opening-range, gap and cross-sectional families were also screened.

## Strongest empirical candidate
TCS, 15-minute EMA20/26 with 1.5 ATR stop and Monte Carlo gate: validation +0.74% with PF 1.14; subsequent out-of-sample +5.59%, PF 1.71, Sharpe 1.17 and max drawdown -2.94% over 40 trades.

## Intraday candidate
TCS, 15-minute EMA20/26 with 1.5 ATR stop and 20-bar maximum hold: validation +3.00%, PF 1.49; subsequent out-of-sample +14.33%, PF 2.87, Sharpe 2.10, max drawdown -1.92% over 40 trades.

## BTST result
The corrected true BTST test (next-open to next-close) did not produce a candidate that persisted from validation to test. No BTST strategy is classified as usable.

## Swing result
HDFCBANK EMA20/21 with 8-session max hold produced validation +6.75%, PF 1.38 and test +0.94%, PF 1.08. This is too weak for a robust/live classification.

## Final evidence status
No single strategy passed the robustness standard across all four horizons. The project therefore stops strategy search here rather than expand into uncontrolled data-mining. The remaining bottleneck is data quality: true 1-minute/tick/bid-ask scalping data and broader point-in-time multi-stock datasets are needed for stronger claims.


## Phase 8 interim status
Public Kaggle, Hugging Face, TejHQ and GitHub datasets have been identified and provenance recorded. The accessible 8-symbol mirror screen is negative for the frozen EMA family at 5 bps/leg across intraday/scalping/BTST/swing; this is not treated as independent replication. The corrected engine and manual GitHub Actions workflow are now in place for the independent public-source run.


## Latest Phase 8 update
- Public-source expansion: COMPLETE for discovery/audit step.
- Corrected interim execution: COMPLETE on 8 accessible symbols using the existing public GitHub mirror.
- True 1-minute bulk execution: BLOCKED in the current connector/runtime by file-size limits; no invalid result accepted.
- Independent 214-symbol F&O and TejHQ run: IMPLEMENTED in GitHub Actions workflow; execution artifact still pending because the available interface cannot manually dispatch Actions.
