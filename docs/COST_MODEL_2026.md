# Phase 2 Cost Model

## Verified public inputs
NSE's current levy page lists SEBI turnover fees at 0.0001% of transaction value, stamp duty at 0.015% for delivery purchases and 0.003% for non-delivery purchases, GST at 18% for stock-broker services, and from 1 April 2026 STT of 0.100% on both delivery purchases and sales and 0.025% on non-delivery equity sales. citeturn350019search0

NSE's current cash-market transaction schedule is treated as 0.00307% per side from 1 March 2026 (Rs 307/crore per side). The final machine-readable source must be archived/hashed during Phase 2 data acquisition.

Paytm Money's live brokerage calculator is the preferred source for account-specific current brokerage and explicitly warns that platform fees, depository charges, auto-square-off charges and other fees may be outside the calculator. citeturn350019search1

Paytm Money's official pricing communication has stated flat Rs 20 brokerage across segments, but account cohorts and historical schedules can differ, so the research config keeps brokerage as a versioned parameter rather than treating Rs 20 as universal. citeturn350019search5turn350019search7

## Research implementation
The engine keeps brokerage, STT, stamp duty, SEBI fee, exchange transaction charges, GST, spread and slippage separate. Gross P&L is always retained alongside net P&L.

## Slippage and spread
Slippage is expressed in basis points per execution leg. Spread is also parameterized per leg. The empirical value will be frozen before Phase 4 using the best available bid/ask or conservative liquidity-based proxies. Scalping and intraday analyses will use stricter slippage sensitivity than BTST/swing where execution frequency is lower.

## Broker-specific charges not yet frozen
DP charges, auto-square-off charges, platform/account-specific fees and MTF interest are not silently assumed to be zero. They remain configurable and will be activated only for strategies where they apply.

## Temporal validity
The model is date-aware. Costs must be switched by effective date when a backtest spans a regulatory/broker pricing change. Applying today's costs unchanged to historical periods is allowed only as a separately labelled stress scenario, not as the primary historical-cost estimate.
