# Final Evidence Gate — Phase 8

**Date:** 20 Sep 2026  
**Status:** CLOSED under the finite public-data protocol.

## Gate criteria

A strategy is considered robust only when all of the following hold:

1. Positive aggregate out-of-sample result.
2. Non-negative median symbol result.
3. Majority of tested symbols are not losing.
4. Same qualitative conclusion survives at least 5 bps per execution leg.
5. Monte Carlo contributes measurable return or risk benefit rather than only reducing participation.
6. No look-ahead, capital-accounting, universe-selection or data-quality violation invalidates the result.

## Observed evidence

### Historical NSE replication — 5 bps/leg

| Horizon | Mean | Median | Positive | Median PF |
|---|---:|---:|---:|---:|
| BTST | -4.97% | -4.61% | 4/19 | 0.50 |
| Swing | -3.69% | -7.51% | 7/19 | 0.62 |

### BSE cross-market replication — 5 bps/leg

| Horizon | Mean | Median | Positive | Median PF |
|---|---:|---:|---:|---:|
| BTST | -2.55% | -2.94% | 4/19 | 0.13 |
| Swing | -3.36% | -3.28% | 6/19 | 0.45 |

Both panels fail the aggregate/median/majority profitability gate. Profit factors remain below one.

The Phase 8 corrected 8-symbol intraday/scalping proxy was also negative at 5 bps/leg. The earlier TCS 15-minute result remains a single-symbol exploratory candidate.

## Decision

**No universal strategy is promoted.**

The project is complete under the finite protocol. Additional indicator mining on the same public samples is prohibited because it would change the study from pre-specified validation into post-hoc search.

The next scientifically valid step, outside this completed protocol, is new data acquisition and an independent holdout: 1-minute/tick/bid-ask data for short horizons and a broader point-in-time universe for BTST/swing.

## Important non-conclusion

The gate does **not** prove that all trading strategies are unprofitable, or that Monte Carlo can never add predictive value. It only rejects the tested frozen strategy family as a robust universal solution under the tested public data and cost scenarios.

## Evidence classification

- **Live-ready strategy:** none.
- **Paper-trading research candidate:** TCS 15-minute EMA20/26 intraday, conditional and single-symbol.
- **Validated BTST strategy:** none.
- **Validated swing strategy:** none.
- **Validated true scalping strategy:** none.
