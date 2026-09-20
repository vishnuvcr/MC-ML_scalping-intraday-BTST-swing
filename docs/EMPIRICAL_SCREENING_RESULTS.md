# Phase 7 — Empirical Screening Results

## Data used
Secondary public dataset from the MIT-licensed `scriptkidakash81/stocks-data` research pipeline. The pipeline states that its market data are sourced through Yahoo Finance and stores NSE stock OHLCV at 15-minute and daily resolutions. The data were used as a research/validation source only; they are not treated as official exchange tick/order-book data.

15-minute data were used as a proxy for short-horizon research because the accessible 1-minute files were too large for the available repository-fetch interface. Therefore the scalping results are **15-minute scalping proxies**, not true tick/1-minute scalping evidence.

## Strategy architecture screened
The main candidate was a deliberately simple Monte Carlo-gated trend system:
- EMA(20/26) crossover for short horizons;
- EMA(20/21) crossover for daily horizons;
- ATR(14)-scaled stop;
- fixed maximum holding period by horizon;
- enter at next bar/day open;
- net P&L after the versioned transaction-cost model;
- Monte Carlo gate based on the last 30 completed net trades and 250 bootstrap resamples, requiring at least 50% of simulated cumulative paths to be positive once the minimum trade history exists.

Additional pre-specified families screened and rejected: range breakout, RSI/Bollinger mean reversion, VWAP mean reversion, opening-range breakout, cross-sectional relative strength, gap momentum/reversal, and event-driven overnight rules.

## Results from the corrected screening

| Horizon | Configuration / data | Validation | Out-of-sample | Interpretation |
|---|---|---:|---:|---|
| Scalping proxy | 15m EMA20/26, 1.5 ATR stop, max 4 bars, TCS | +0.74%, PF 1.14, 32 trades | +5.59%, PF 1.71, Sharpe 1.17, max DD -2.94%, 40 trades | Positive candidate, but single-symbol and only a 15m proxy |
| Intraday | 15m EMA20/26, 1.5 ATR stop, max 20 bars, TCS | +3.00%, PF 1.49, 33 trades | +14.33%, PF 2.87, Sharpe 2.10, max DD -1.92%, 40 trades | Strongest empirical candidate in this run, still needs broader replication |
| BTST | True one-overnight EMA20/21, next-open to next-close | HDFCBANK +7.54%, PF 3.56, but only 13 trades | HDFCBANK -2.50%, PF 0.53, 14 trades | Failed validation-to-test persistence; no usable BTST strategy found |
| Swing | EMA20/21, 8-day max hold, 0.75 ATR stop | HDFCBANK +6.75%, PF 1.38, 25 trades | HDFCBANK +0.94%, PF 1.08, Sharpe 0.15, 28 trades | Weak positive candidate, not strong enough for robust classification |

## Cross-stock finding
The same simple EMA architecture is highly heterogeneous. TCS generated the strongest short-horizon positive out-of-sample result. HDFCBANK generated the only clearly positive daily validation and a small positive later test. Several other large liquid stocks lost money after costs. This prevents claiming a universal stock-agnostic strategy.

## Monte Carlo finding
Monte Carlo generally reduced the number of trades and often reduced drawdown, but it did not consistently improve net return. In the strongest TCS intraday candidate, the MC gate acted primarily as a risk/participation filter rather than a return generator. This supports the research thesis that Monte Carlo is more defensible as a validation/risk layer than as the alpha source.

## Important rejected result
A preliminary 52-week-high/momentum experiment produced very large apparent returns on some symbols. It was rejected because the implementation allowed overlapping positions while treating sequential compounded capital as if the positions did not overlap. That is a material portfolio-accounting error. The result is not used in the final conclusions.

## Final strategy status
No single strategy passed the study's full robustness criterion across scalping, intraday, BTST and swing after costs. The **TCS 15-minute EMA20/26 system is a research candidate for short-horizon paper testing**, not a validated live strategy. BTST has no validated candidate in the present data. Swing has only a weak HDFCBANK candidate.

## Stop decision
The empirical screening phase is closed here. Continuing to add indicator families would become uncontrolled data-mining rather than the finite research plan. The next legitimate improvement requires better data—especially 1-minute/tick/bid-ask data for scalping and a broader point-in-time universe for BTST/swing—rather than more parameter searching on the same public sample.
