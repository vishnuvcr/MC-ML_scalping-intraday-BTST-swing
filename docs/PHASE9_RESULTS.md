# Phase 9 Results

Status: **EXECUTION IN PROGRESS**

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
