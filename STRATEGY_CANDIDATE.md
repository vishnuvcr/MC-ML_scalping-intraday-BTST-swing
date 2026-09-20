# MC-Gated EMA Strategy — Research Candidate

## Status
**Paper-trading research candidate only. Not validated for live trading.**

## Common signal
- Price series: NSE equity OHLCV.
- Trend signal: EMA(20) versus EMA(26) for 15-minute horizons; EMA(20) versus EMA(21) for daily horizons.
- Long signal: fast EMA crosses above slow EMA.
- Short signal: fast EMA crosses below slow EMA for intraday/scalping only.
- Entry: next bar/session open after the crossover.
- Risk stop: 1.5 × ATR(14) for the short-horizon candidate.
- Monte Carlo participation gate: once at least 20 previous net trades exist, resample the most recent 30 trades 250 times; participate only when at least 50% of simulated cumulative paths are positive.
- Position notional in research: ₹100,000 per trade.
- All reported results are after the study's brokerage/statutory/spread/slippage cost assumptions.

## Horizon rules
### 15-minute scalping proxy — TCS
Maximum hold: 4 bars. This is a 15-minute proxy, not true tick/1-minute scalping.

Validation: +0.74%, PF 1.14, 32 trades.
Test: +5.59%, PF 1.71, Sharpe 1.17, max drawdown -2.94%, 40 trades.

### Intraday — TCS
Maximum hold: 20 bars, with the same EMA20/26 signal and MC gate.

Validation: +3.00%, PF 1.49, 33 trades.
Test: +14.33%, PF 2.87, Sharpe 2.10, max drawdown -1.92%, 40 trades.

### BTST
**No live candidate.** The corrected true BTST test (next open to next close) failed to persist out of sample. The framework should therefore remain in cash rather than forcing BTST trades.

### Swing
EMA20/21 with an 8-session maximum hold and the daily cost model produced only weak evidence in HDFCBANK (+0.94% test, PF 1.08, Sharpe 0.15). Treat as exploratory only.

## Why the MC layer is retained
The MC layer is useful as a participation/risk filter. It should not be described as the source of the observed TCS return; in the strongest TCS intraday result it primarily reduced trade participation.

## Paper-trading gate before live consideration
1. Reproduce the exact strategy on licensed 1-minute/tick/bid-ask data.
2. Keep the stock universe fixed before observing the next holdout.
3. Require a fresh holdout period not used in screening.
4. Re-estimate realistic spread/impact and partial-fill assumptions.
5. Require the same direction of effect after costs and data-snooping correction.
