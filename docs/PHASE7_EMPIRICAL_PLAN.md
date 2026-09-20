# Phase 7 — Empirical Research Re-entry

## Objective
Re-open the empirical gate using publicly inspectable NSE-equity OHLCV research datasets while preserving source provenance and explicitly separating exploratory public data from validated/licensed production data.

## Data sources inspected
1. scriptkidakash81/stocks-data: individual NSE symbols with 1-minute, 2-minute, 5-minute, 15-minute, 60-minute and daily CSVs. The RELIANCE.NS files were directly readable through the GitHub connector; 15-minute data extend through 2026-09-18 and daily data through 2026-09-18.
2. ShabbirHasan1/NSE-Data: NSE minute-data repository containing many individual stock files, including RELIANCE, but the connector cannot read the large CSV payload directly.
3. voletiramu/nse-fno-1min-data: public release v1.0.0 containing 214 NSE F&O underlying stocks, 1-minute OHLCV, 2024-04-01 through 2026-04-30, source stated as Zerodha Kite API. The release asset is ~464 MB compressed and was not downloaded into this repository during this run.

## Evidence rule
Public GitHub data are suitable for exploratory research and software validation, not automatically equivalent to licensed exchange-grade data. Any strategy that survives here must still pass a separate live/paper or licensed-data validation gate before deployment.

## Horizon mapping
- Scalping: 1m/5m where accessible; 15m fallback for exploratory screening.
- Intraday: 15m/5m.
- BTST: daily close-to-next-session-open.
- Swing: daily multi-day holding.

## Strategy family frozen before evaluation
The initial family is a simple trend-breakout system: prior-N-bar breakout + EMA trend filter + ATR stop/target, with Monte Carlo used as a trade-sequence/risk filter rather than as a predictive price generator.

## Monte Carlo filter
For a candidate entry, bootstrap recent realized trade returns with replacement and estimate the probability that the mean simulated trade return is positive. The filter is allowed only as a risk/quality gate; it cannot use future test returns.

## Cost model
All reported results must include brokerage, statutory charges, and explicit spread/slippage stress. Exact broker charges remain versioned inputs and are not assumed universal.

## Stop condition
Do not declare a usable strategy from one stock, one regime, or one parameter set. A candidate must survive multi-symbol out-of-sample tests and adverse execution-cost stress. If no candidate does, report that negative result rather than manufacture a strategy.
