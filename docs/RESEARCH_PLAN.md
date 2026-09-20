# Detailed Research Plan

## Aim
Determine whether Monte Carlo methods provide statistically credible and economically meaningful improvement in stock-trading research across scalping, intraday, BTST and swing horizons.

## Objectives
1. Separate Monte Carlo use-cases: trade-sequence resampling, dependent-return bootstrap, permutation/placebo tests, price-path simulation, parameter perturbation, and drawdown/risk estimation.
2. Establish realistic Indian-equity execution-cost models including brokerage, STT, stamp duty, exchange/SEBI charges, GST, spread, slippage and optional financing/MTF cost.
3. Compare Monte Carlo-enhanced systems against matched non-Monte-Carlo baselines.
4. Test out-of-sample performance and control data snooping/backtest overfitting.
5. Measure net return, CAGR, Sharpe/Sortino, drawdown, profit factor, expectancy, turnover and tail risk.
6. Test robustness across securities, years, volatility regimes, liquidity buckets and horizons.
7. Produce a reproducible manuscript and code/data package.

## Research questions
RQ1. Does Monte Carlo add predictive or decision value beyond a matched baseline?
RQ2. Which Monte Carlo formulation, if any, is useful for each horizon?
RQ3. Does any gross edge survive realistic costs and slippage?
RQ4. Does the edge survive multiple-testing and backtest-overfitting controls?
RQ5. Is performance stable across stocks, periods and market regimes?
RQ6. Can Monte Carlo improve risk control even if it does not improve raw prediction?

## Planned phases
### Phase 0 — Governance
Freeze scope, research questions, hypotheses framework, repository conventions and logging.

### Phase 1 — Literature and data audit
Collect peer-reviewed papers, preprints, official exchange/regulatory material, broker pricing, and selected practitioner/video sources. Record source date, method, population, evidence, limitations and relevance.

### Phase 2 — Data and costs
Build point-in-time datasets at appropriate resolutions. Daily OHLCV supports BTST/swing; intraday bars/ticks support intraday/scalping where licensed and available. Record corporate actions, symbol changes and survivorship rules. Build a parameterized cost engine.

### Phase 3 — Baselines and Monte Carlo
Define simple baselines before optimization. Candidate baselines: benchmark/buy-and-hold, trend, breakout/momentum, mean-reversion and volatility/volume filters. Keep simulation separate from signal logic.

### Phase 4 — Backtests and inference
Use strict train/validation/test separation. Run null/placebo tests, bootstrap intervals, White Reality Check or Hansen SPA/stepwise variants as appropriate, DSR/PSR, and PBO/CSCV where strategy selection is present.

### Phase 5 — Robustness
Stress slippage, spread, delay, partial fills, liquidity, turnover, costs and regime shifts. Repeat across stocks and time blocks. Evaluate parameter stability and trade-order Monte Carlo drawdown distributions.

### Phase 6 — Synthesis
Freeze code/data versions. Prepare manuscript, methods/statistical appendices, reproducibility instructions, charts/tables, negative results and future research.

## Statistical analysis
Primary outcomes: net compound return/CAGR, annualized Sharpe, maximum drawdown, Calmar/Sortino, profit factor, expectancy per trade, turnover and net return per unit turnover.

Inference should use dependence-aware bootstrap when observations are dependent, permutation tests only where exchangeability is justified, and multiple-testing-aware procedures for strategy selection. Report effect sizes and uncertainty, not only p-values.

A strategy will be classified as robustly profitable only if it is net profitable out-of-sample under the primary cost model and remains supported by pre-specified robustness tests. The research will report evidence, not rank or recommend trading choices.

## Execution assumptions
Brokerage per executed order, statutory charges, spread, slippage, order type, latency and partial fills will be explicit and parameterized. Paytm Money pricing will be stored with source date and version rather than embedded as undocumented constants.

## Reproducibility
- Python for research/statistics; Rust where performance-critical simulation justifies it.
- Manual GitHub Actions workflow for every phase.
- Deterministic random seeds recorded per experiment.
- Data hashes and schema versions recorded.
- Cached data preferred over repeated downloads subject to licensing.
- Every material outcome and error appended to project logs.
