# Phase 7 Corrected Engine Specification

1. Start with fixed initial equity of ₹100,000.
2. At each entry, allocate at most 100% of current equity; quantity = floor(equity / entry price).
3. Keep exactly one position per symbol in the initial validation engine.
4. Record entry notional and exit notional separately.
5. Deduct brokerage, statutory charges, spread and slippage from every completed round trip.
6. Update cash/equity by realized net P&L; no artificial compounding of gross returns.
7. For drawdown, mark open positions to current close and calculate equity peak-to-trough.
8. Entries occur only after a signal is fully formed; execution is at the next available bar/open.
9. Stops/targets are evaluated conservatively when both are touched in the same OHLC bar: stop is assumed first.
10. No future test data may influence parameters, Monte Carlo thresholds or cost assumptions.
11. All random seeds and parameter sets are recorded.
12. A candidate is rejected if accounting invariants fail.
