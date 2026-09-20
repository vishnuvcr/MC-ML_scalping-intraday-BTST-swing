# Phase 5 — Robustness and Regime Analysis

Phase 5 is specified but not executed because Phase 4 has no validated market dataset.

## Required stress dimensions when data become available
- slippage: primary, conservative and adverse bands;
- spread: measured bid/ask where possible and conservative proxy otherwise;
- order delay and partial fills;
- liquidity/turnover buckets;
- symbol concentration;
- market regimes based on volatility/trend states;
- bull/bear/sideways periods;
- parameter perturbation around selected settings;
- block lengths for dependent bootstrap;
- sub-period and walk-forward stability;
- transaction-cost changes over time.

## Replication design
A positive finding must be repeated across independent stocks and time blocks. A result confined to one stock, one regime or one parameter setting will be treated as exploratory.

## Fragility criteria
The final report will flag a strategy when performance changes sign under modest cost/slippage changes, depends on a small number of trades, collapses out-of-sample, or requires an unusually narrow parameter range.

## Regime analysis
Results will be stratified by volatility and trend regimes defined without future information. Regime definitions are frozen before test evaluation.

## Output
Phase 5 will produce a robustness matrix, sensitivity charts, regime tables and a consolidated fragility assessment if/when Phase 4 data are unlocked.
