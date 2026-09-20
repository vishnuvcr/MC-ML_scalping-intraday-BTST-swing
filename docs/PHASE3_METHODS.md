# Phase 3 — Baselines and Monte Carlo Methodology

## Baseline strategy families
The empirical study will pre-register simple, interpretable baselines before tuning.

1. Benchmark/hold: buy-and-hold or market benchmark for contextual comparison, not as a trading recommendation.
2. Trend: moving-average crossover with fixed lookbacks.
3. Breakout: rolling high/low breakout with fixed exit rule.
4. Mean reversion: distance from rolling mean with fixed band and holding period.
5. Volatility/volume filter: baseline signal gated by liquidity/volatility thresholds.

Each baseline produces a deterministic trade ledger before any Monte Carlo layer is applied.

## Monte Carlo variants
### A. Trade-sequence bootstrap
Resample completed trades to estimate distributions of terminal wealth, drawdown and ruin. Useful for risk questions but does not prove the trade-generation process is stationary.

### B. Stationary/block bootstrap
Resample dependent returns or blocks so serial dependence is partially retained. This is the primary inferential resampling method for time-series outcomes.

### C. Permutation/placebo null
Randomize the mapping between a signal and future returns only where the null justifies exchangeability. This tests whether the observed relation could arise under a no-signal construction.

### D. Parameter perturbation
Run pre-specified neighborhoods around the chosen parameter values. Robust regions are evidence of stability; a single sharp optimum is a warning sign, not a positive result.

### E. Price-path simulation
Use explicit stochastic models only as a separate model-risk experiment. Parametric paths will never substitute for empirical out-of-sample market data.

## Required comparison
For every strategy and horizon, report:
- baseline deterministic backtest;
- matched Monte Carlo version;
- gross and net performance;
- uncertainty interval/distribution;
- execution-cost assumptions;
- out-of-sample result;
- multiple-testing adjustment when a strategy family is searched.

## Randomness controls
All experiments record a fixed seed, simulation count, bootstrap type, block-length rule, software version and configuration hash.

## Primary scientific question at this phase
Does adding Monte Carlo improve the quality of inference/risk control without simply creating another layer of model selection that overfits historical data?
