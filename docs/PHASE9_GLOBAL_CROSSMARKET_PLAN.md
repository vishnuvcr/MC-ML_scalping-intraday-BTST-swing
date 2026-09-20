# Phase 9 Global Cross-Market Extension

Cross-market scope now includes NSE, BSE and global markets.

Global inputs: S&P 500, Nasdaq 100, FTSE 100, DAX, Nikkei 225, Hang Seng, KOSPI, Shanghai Composite, VIX, DXY, USD/INR, WTI and gold.

Leakage control: an Indian signal dated D can use only global observations whose source date is strictly earlier than D. Same-day foreign closes are excluded.

The frozen global condition is: at least 5 of 8 equity benchmarks were positive on the prior completed global session and prior-session VIX change was non-positive.

Variants are compared at 0, 5 and 10 bps per leg: EMA20/26 baseline; EMA20/26 plus the existing Monte Carlo participation gate; EMA20/26 plus the global condition; and both gates together.

The corrected engine resets test capital to INR 100,000 at the 2026 test boundary so earlier path-dependent equity cannot contaminate the out-of-sample denominator.

Analysis includes symbol-level paired results, trade-level global-factor quintiles, risk-on/risk-off conditional returns, lead/lag diagnostics and friction sensitivity.

Global raw data are runner-only. yfinance documentation states that it uses Yahoo Finance public APIs for research/educational use and that actual downloaded data remain subject to Yahoo terms.

Phase exit: observe the corrected broad-intraday workflow, evaluate the 5 bps/leg gate, and integrate the result into the evidence gate without opening an unrestricted parameter search.
