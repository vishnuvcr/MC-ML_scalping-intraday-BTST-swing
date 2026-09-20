# Phase 7 Error Correction 001 — Backtest Accounting Bug

## Problem
The first narrow exploratory simulator produced impossible returns (orders of magnitude above 100%) and zero drawdown. The result is invalid.

## Root cause
The simulator treated a fixed ₹100,000 position size as if the full gross P&L could be compounded without accounting correctly for the capital/equity relationship across sequential trades. The scoring function therefore became numerically explosive.

## Resolution
Do not use the output. Rebuild the engine around explicit portfolio cash/equity, share quantity, entry/exit notional, realized net P&L, and mark-to-market drawdown. The corrected engine must also prevent overlapping positions and cap position size by available equity.

## Research rule
No strategy result from this run is promoted to evidence. The invalid output is retained only as an error-log artifact.
