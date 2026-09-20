# Phase 4 — Statistical Inference Plan

## Primary outcomes
1. Net CAGR/compound return.
2. Maximum drawdown.
3. Annualized Sharpe and Sortino.
4. Profit factor and expectancy per trade.
5. Turnover and net return per unit turnover.
6. Tail loss and drawdown duration.

## Primary comparisons
For each horizon, compare a Monte Carlo-enhanced method against its matched baseline on the same point-in-time test set and the same execution-cost model.

## Inference
- Use stationary/block bootstrap for dependent return series.
- Use IID trade bootstrap only for the narrower trade-sequence risk question.
- Use permutation/placebo tests only where the null preserves the relevant exchangeability assumptions.
- Report effect sizes with confidence intervals.
- When many strategies or parameter combinations are searched, apply data-snooping controls such as White Reality Check and/or Hansen SPA and report selection-adjusted evidence.
- Use Deflated Sharpe Ratio for Sharpe comparisons affected by multiple trials/non-normality.
- Use PBO/CSCV when a model-selection process exists and there are enough candidate configurations.
- Pre-specify the primary test set before seeing test results.

## Multiple testing hierarchy
The analysis will distinguish: (1) one pre-registered comparison, (2) a family of related parameter variants, and (3) exploratory searches. Exploratory findings cannot be promoted to confirmatory results without a fresh holdout or independent replication.

## Decision rule
Robust profitability requires positive net out-of-sample economics plus statistical support and stability under the pre-specified cost/slippage band. A statistically significant result with economically trivial return or unstable execution is not sufficient.

## Missing-data rule
No imputation that could create tradable information. Missing market sessions, symbols or quotes are handled by source-specific rules and logged.

## Empirical status
This plan is ready for execution but stock-level statistics remain blocked until validated market data are available.
