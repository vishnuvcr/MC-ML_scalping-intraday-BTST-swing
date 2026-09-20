# Phase 9 — NSE-Universe, Stock-Selection, Regime and Cross-Market Analysis

## Question
The Phase 7 TCS result was single-symbol evidence. Phase 9 asks whether the same frozen Monte-Carlo-gated EMA framework survives broad NSE testing and whether its success is conditional on stock selection, liquidity, volatility, trend state, market regime, time-of-day or NSE/BSE relative pricing.

## Primary research questions
**RQ9.1:** Does the TCS 15-minute EMA20/26 + MC result replicate across a broad NSE stock universe?
**RQ9.2:** Does Monte Carlo add incremental value relative to the matched EMA baseline once stock selection is controlled?
**RQ9.3:** Which observable stock characteristics explain positive/negative MC strategy outcomes?
**RQ9.4:** Which market regimes explain strategy success or failure?
**RQ9.5:** Does NSE/BSE relative pricing or lead-lag divergence predict subsequent NSE trade success?
**RQ9.6:** Is there a point-in-time stock-selection rule that improves robustness without becoming post-hoc data mining?

## Data hierarchy
### Tier A — exact short-horizon replication
Use the public indian-stocks-mcp hosted historical source for the advertised 117 NIFTY 100 stock symbols and 1-minute history, then resample to 15-minute bars. This is the closest exact replication of the Phase 7 TCS specification. It is not the full NSE universe.

### Tier B — broad NSE universe
Use tejhq/indian-markets daily raw NSE data. The dataset currently advertises about 2,300 NSE instruments per day and coverage from 4 Jan 2010 to the present. It is sourced from official exchange bhavcopy and provides raw OHLCV plus a point-in-time liquidity-universe tree.

### Tier C — full-NSE intraday proxy
Use Dr-Kitz28/NSE-OHLCV-Data, which publishes daily and hourly OHLCV for NSE stocks in P1/P2/P3. The project states that it covers the NSE universe from listing dates. Its data are CC BY-NC 4.0, so files must remain runner-cache material and must not be copied into this repository.

## Frozen strategy
Do not change the Phase 7 signal to improve the result.

### Intraday/scalping framework
- EMA20/26 crossover.
- Entry at next bar/session open.
- ATR14 stop.
- Phase 7 TCS intraday hold: 20 bars.
- Phase 7 scalping proxy: 4 bars.
- MC gate: after 20 completed trades, bootstrap the latest 30 net trades 250 times; participate only if at least 125/250 paths finish positive.
- Equity-capped position size.
- Compare MC and baseline under identical information and cost assumptions.

### Daily framework
- EMA20/21.
- BTST exactly next-open to next-close.
- Swing maximum 8 sessions with 0.75 ATR stop.
- Same MC gate.

## Point-in-time stock-selection variables
All variables must be calculated using data available no later than signal time:
1. 20/60-day average traded value.
2. 20/60-day volume.
3. Price level and price volatility.
4. ATR/price.
5. Return volatility.
6. Trend strength: EMA20/EMA50 distance and 20/60-day momentum.
7. Volume surprise/z-score.
8. Gap size.
9. Idiosyncratic beta to NIFTY 50.
10. Residual volatility after market beta.
11. Recent trade frequency of the strategy.
12. Signal time bucket for intraday entries.

## Market-regime variables
1. NIFTY trend state: price above/below 50-day and 200-day EMA.
2. NIFTY realized volatility quintile.
3. NIFTY daily drawdown state.
4. INDIA VIX regime where synchronized index data exist.
5. Breadth regime: fraction of universe with positive prior-day returns.
6. Cross-sectional dispersion of prior-day returns.
7. Liquidity regime: median ADV and breadth of liquid names.

## Cross-market inefficiency variables
For stocks with both NSE and BSE observations:
1. NSE-BSE close basis.
2. Absolute NSE-BSE percentage-price divergence.
3. One-day lagged basis.
4. Same-day direction disagreement.
5. BSE-leads-NSE return relationship, using only prior-session information.
6. Basis quintiles and subsequent strategy trade returns.

## Statistical analysis
### Primary comparison
For each horizon, compare baseline EMA versus MC-gated EMA using paired per-symbol and per-period differences.

### Conditional effects
- Quintile stratification for liquidity, volatility, trend, volume surprise and basis.
- Cluster bootstrap by symbol and calendar block.
- Difference-in-means with 95% bootstrap confidence intervals.
- Logistic regression for probability that an MC trade is profitable.
- Regression for continuous net trade return using standardized predictors.
- Interaction terms for MC × regime and MC × stock-selection variable.
- Symbol-clustered and month-clustered uncertainty where feasible.
- Benjamini-Hochberg FDR across the finite factor family rather than selecting the most favorable subgroup post hoc.

### Stability
- Train: earlier data.
- Validation: intermediate period.
- Test: held-out later period.
- The conditional rule, if any, must be selected using training/validation only and then tested once.

## Stock-selection experiments
Three pre-specified universes:
1. All available NSE symbols.
2. Liquidity top-500 point-in-time universe.
3. Liquidity quintiles from the point-in-time universe.

A selection rule may be retained only if it improves the test distribution without materially increasing concentration or depending on future membership.

## Regime experiments
The frozen signal will be evaluated in each pre-specified regime. No regime threshold will be optimized on the final test set.

## Decision gate
Phase 9 can promote a conditional MC strategy only if:
- the conditional rule is positive net OOS;
- the effect remains present in an independent stock/time slice;
- the result survives 5+ bps per leg;
- MC adds incremental value over the matched baseline;
- symbol concentration is controlled;
- the rule is explainable using lagged variables;
- no future information is used for selection.

Otherwise, the result is a descriptive finding, not a trading strategy.

## Important limitation
The exact 15-minute strategy cannot honestly be described as “entire NSE” unless 15-minute/intraday data exist for the entire universe. Phase 9 therefore distinguishes:
- exact 15-minute test on the broadest accessible NIFTY 100 panel;
- hourly full-NSE intraday proxy;
- daily full-NSE validation.

This prevents silently changing time resolution while claiming exact replication.

## Finite stop rule
No new indicator families or parameter searches are permitted. Phase 9 ends after the universe, selection, regime and cross-market tests defined above. If no conditional strategy survives, the conclusion is that the TCS effect is not sufficiently generalizable under the available evidence.