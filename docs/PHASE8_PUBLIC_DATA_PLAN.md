# Phase 8 — Public Data Expansion and Cross-Source Validation

## Status
INITIATED — 20 September 2026

## Reason for protocol amendment
Phase 7 stopped because the available connector could not reliably consume the required high-frequency datasets. A new user-directed data-acquisition step is now added: public datasets from Kaggle, Hugging Face and GitHub may be used for exploratory empirical research when their provenance and licence are recorded. These results remain separate from licensed/exchange-grade evidence.

## Objective
Determine whether the Phase 7 findings persist across a broader, independently sourced NSE universe and finer intraday resolution, without increasing indicator/parameter search.

## Frozen data-source hierarchy
1. PRIMARY DAILY UNIVERSE: tejhq/indian-markets — NSE/BSE official bhavcopy derived, point-in-time symbol history and liquidity universe.
2. PRIMARY HIGH-FREQUENCY EXPLORATORY: voletiramu/nse-fno-1min-data v1.0.0 — 214 NSE F&O underlying stocks, 1-minute OHLCV, 2024-04-01 to 2026-04-30, source stated as Zerodha Kite API.
3. INDEPENDENT HIGH-FREQUENCY CROSS-CHECK: hk7797/stock-market-india on Kaggle — 150 NSE stocks and 9 indices, 1-minute data from 2017.
4. INDEPENDENT BROAD INTRADAY CANDIDATE: rahulkrraj/indian-stock-market-minute-data / xxparthparekhxx/indian-stock-market-minute-data on Hugging Face — 2,500+ NSE stocks/indices, minute data 2022-2026, daily 2000-2026.
5. SECONDARY GITHUB HISTORICAL FILES: ShabbirHasan1/nse-data-1 and ShabbirHasan1/NSE-Data where individual files are technically accessible.

## Research design
### Dataset validation
For every source, record URL, retrieval date, coverage, resolution, license, source lineage, checksum where available, timezone, duplicate/missing-bar rate and corporate-action treatment.

### Symbol universe
Use a pre-frozen liquid/F&O subset for the first screen. Do not select symbols because of observed profitability. Candidate symbols must be determined from the dataset's documented universe or a date-fixed liquidity rule.

### Horizon mapping
- Scalping proxy: 1-minute and 5-minute bars.
- Intraday: 15-minute bars.
- BTST: next-session-open to next-session-close, exactly one overnight.
- Swing: daily, 8-session maximum hold.

### Frozen signal families
No new indicator mining. Re-run the Phase 7 family:
- EMA(20/26) trend system for short horizons.
- EMA(20/21) daily system for BTST/swing.
- ATR(14) stop.
- Phase-7 maximum-hold rules.
- Monte Carlo participation/risk gate exactly as previously specified.
Matched no-MC baselines are mandatory.

### Execution and costs
Use explicit Paytm Money brokerage inputs plus current NSE statutory/exchange levies. Run primary and adverse spread/slippage stress: 0, 2.5, 5 and 10 bps per leg. For delivery/overnight trades, include configured delivery STT/stamp/DP assumptions and clearly flag account-specific uncertainty.

### Validation splits
Initial fixed split for 1-minute/15-minute studies:
- Train: 2024-04-01 to 2025-06-30
- Validation: 2025-07-01 to 2025-12-31
- Test: 2026-01-01 to 2026-04-30
The test period is never used to choose symbols, thresholds or parameters.

Daily cross-universe studies use a separate calendar split consistent with Phase 7 and preserve point-in-time universe membership.

### Statistical endpoints
Primary: median net test return across symbols; percentage of symbols with positive net test return; median profit factor; median Sharpe; equal-weight aggregate return for the pre-frozen universe.
Secondary: bootstrap confidence intervals; paired baseline-vs-MC differences; drawdown/trade-count distributions; sensitivity to slippage.

### Robustness gate
A candidate proceeds only if, on a fixed holdout:
1. Net test return is positive at the aggregate level.
2. Median symbol result is not materially negative.
3. The majority of symbols are not loss-making.
4. The same direction of effect persists under at least 5 bps/leg stress.
5. MC adds measurable incremental value versus its matched baseline or improves a pre-specified risk metric without materially harming return.
6. No accounting, overlap, look-ahead or universe-selection invariant fails.
A positive single-stock result is never sufficient.

## Data handling and caching
Large raw releases will not be committed to the repository unless redistribution is clearly permitted. GitHub Actions will cache immutable release assets by SHA-256. Small derived datasets and manifests may be versioned in data/processed/. Every run writes data hashes and experiment metadata.

## Stop condition
Phase 8 is finite. It ends after one broad daily universe screen; one 1-minute/5-minute/15-minute F&O screen; cross-source checks on a small independently available symbol set; full cost/slippage sensitivity; baseline-vs-MC comparison; and statistical/robustness summary.
No additional indicator families are permitted without a new protocol amendment.