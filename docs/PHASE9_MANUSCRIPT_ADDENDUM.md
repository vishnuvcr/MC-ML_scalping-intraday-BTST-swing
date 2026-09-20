# Phase 9 Manuscript Addendum — Universe, Selection, Regime and Cross-Market Analysis

## Hypothesis

The prior TCS result may be conditional rather than universal. A broad test is required to determine whether success depends on stock liquidity, volatility, trend, market regime, time-of-day or cross-market divergence.

## Primary estimand

For each pre-specified subgroup, estimate the paired incremental effect:

**MC net trade return − baseline net trade return**

under the same signal, same entry/exit rules, same symbol and same execution-cost assumptions.

The main statistical unit is the symbol-period block rather than treating every trade as independent.

## Conditional factors

- average traded value;
- realized volatility;
- ATR/price;
- trend distance from EMA20/EMA50;
- momentum;
- volume surprise;
- gap;
- market beta and residual volatility;
- entry-time bucket;
- market breadth;
- market volatility regime;
- cross-sectional dispersion;
- NSE/BSE closing-price basis.

## Guard against selection bias

Features are lagged to the decision time. Quintile boundaries are formed from training/validation observations only where a subgroup becomes a potential decision rule. The final test set is evaluated once. FDR correction is applied across the finite pre-specified factor family.

## Interpretation rule

A conditional effect is not promoted to a trading rule merely because one subgroup has a high return. It must:

1. have positive net OOS performance;
2. improve on the matched baseline;
3. persist in an independent stock/time slice;
4. survive at least 5 bps/leg friction;
5. avoid excessive symbol concentration;
6. use only lagged information.
