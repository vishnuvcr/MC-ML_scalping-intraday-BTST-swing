# Phase 9 Results

Status: **CORRECTED ENGINE — RERUN REQUIRED**

## Scope

Phase 9 tests the previously observed TCS 15-minute EMA20/26 + Monte Carlo candidate against:

1. the broadest accessible exact intraday panel: NIFTY 100 / 117 advertised symbols;
2. the broad NSE daily universe;
3. point-in-time stock-selection characteristics;
4. market and cross-sectional regimes;
5. synchronized NSE/BSE relative-price variables.

## No result is accepted until it comes from the reproducible Phase 9 workflow.

The following outputs will be produced:

- exact 15-minute NIFTY-100 baseline vs MC results;
- full-NSE daily BTST/swing baseline vs MC results;
- liquidity/volatility/trend quintile tables;
- regime tables;
- NSE/BSE basis quintiles;
- regression coefficients and bootstrap confidence intervals;
- concentration diagnostics;
- strategy conditional-decision gate.

## Important distinction

"Entire NSE" is interpreted literally for the daily EOD panel. The 15-minute experiment is explicitly labelled NIFTY-100 unless a true entire-NSE intraday feed becomes available.


## Execution status — 20 Sep 2026

| Test | Universe | Resolution | Status | Accepted result? |
|---|---|---|---|---|
| Exact replication | NIFTY-100 advertised panel | 15-minute | queued in clean workflow | No |
| Broad intraday | 2,500+ NSE stocks / indices | 1-minute → 15-minute | queued in clean workflow | No |
| Full NSE EOD | ~2,300 NSE instruments/day | Daily | queued in clean workflow | No |
| NSE/BSE basis | synchronized NSE/BSE subset | Daily | part of full-NSE EOD workflow | No |

The earlier TCS +14.33% figure remains a **single-symbol research candidate**. No NSE-wide claim has been made from it.

### Conditional variables locked before the final test

Liquidity: ADV20/ADV60, price/volatility, ATR/price, volume surprise.

Stock selection: all available NSE names versus point-in-time liquidity top-500 and liquidity quintiles.

Regimes: lagged market breadth, cross-sectional dispersion, rolling volatility and trend state.

Cross-market: lagged NSE/BSE closing-price basis for synchronized symbols.

Statistics: paired baseline-vs-MC comparison, factor quintiles, cluster-aware bootstrap, conditional logistic/OLS models, and false-discovery-rate control across the finite pre-specified factor family.

### Acceptance rule

A factor or stock-selection condition is not promoted because it has a high return in one subgroup. It must improve the matched baseline, remain positive out of sample, survive at least 5 bps/leg, avoid concentration in a few symbols, and use only information available before the trade.


## 2026-only Nifty500 forward path

The 2026 repository contains 535 Parquet files and is being used as an independent forward-testing source. The analysis includes 2026 test performance, liquidity/volatility/trend/regime factor tables, MC-vs-baseline uplift, and lagged NSE-BSE basis where synchronized TejHQ observations exist. Results remain pending until the corrected workflow artifact is available.


## Run-6 artifact disposition — 20 Sep 2026

The 12 shard jobs in the initial Ganesh run completed, but the aggregate failed on a column-name error. Review of the uploaded shard outputs additionally identified corporate-action scale discontinuities and MC/position-accounting issues. Those outputs are retained only for debugging and are **not accepted as empirical results**. The corrected engine is synced in this branch and a fresh workflow artifact is required before Phase 9 can close.

## Corrected-run disposition — 20 Sep 2026

The corrected workflow completed successfully and produced the final artifact, but the artifact is **not accepted as empirical evidence**. Inspection of the 2026 signal panel found repeated mechanically implausible returns in individual symbols (for example ZFCVINDIA shows multiple approximately +500% / -83% moves). The current corporate-action detector only catches daily-open versus previous-close scale breaks and therefore misses some intraday discontinuities. Because the aggregate compounds equity, those bad observations contaminate universe-level means and MC results. The entire aggregate is quarantined pending an intraday scale-break correction and fresh rerun.
