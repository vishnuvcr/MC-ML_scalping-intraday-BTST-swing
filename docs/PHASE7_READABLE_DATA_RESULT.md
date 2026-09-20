# Phase 7 — Readable Empirical Data Result

## RELIANCE.NS

The public scriptkidakash81/stocks-data repository was directly readable through the GitHub connector.

- 15-minute file: 578,672 bytes; first observed timestamp 2025-11-20 09:15 IST; last observed timestamp 2026-09-18 15:15 IST.
- Daily file: 983,099 bytes; first observed timestamp 1996-01-01; last observed timestamp 2026-09-18.
- Both files contain OHLCV fields plus dividends, stock splits and symbol.

## Decision
The files are sufficient to execute a single-symbol exploratory backtest, but the current connector execution environment timed out during an initial broad multi-stock simulation. Therefore no profitability result is promoted to the research conclusion yet.

The next run will use a narrow, deterministic candidate family and produce per-horizon result artifacts before expanding.
