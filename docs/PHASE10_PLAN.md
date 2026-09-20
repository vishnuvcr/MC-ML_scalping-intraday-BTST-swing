# Phase 10 — Global-Market Information and Cross-Market Inefficiency

## Status
ACTIVE — hypothesis generation completed; out-of-sample implementation is being frozen.

## Scope correction
“Cross-market inefficiency” includes global markets, not only NSE/BSE. Phase 10 therefore studies whether information available from foreign equity markets before the Indian session adds incremental value to the frozen Indian intraday signal.

## Primary research questions
1. Does prior-session global-market direction contain incremental information for the frozen NSE EMA20/26 intraday signal?
2. Does a pre-specified global-market consensus filter improve net trade outcomes after brokerage, statutory charges, spread/slippage and 5/10 bps-per-leg stress?
3. Is the effect incremental to the Monte-Carlo participation gate?
4. Does the effect persist across symbols and market regimes rather than being concentrated in a few stocks?
5. Does the effect survive a strictly later time holdout?

## Frozen Indian strategy
No indicator or parameter mining is permitted in Phase 10:
- LONG ONLY EMA20/26 crossover.
- Entry at next 15-minute bar open.
- ATR14 stop at 1.5 ATR.
- Maximum hold: 20 bars.
- One position per symbol at a time.
- Equity-capped sizing.
- MC gate: after 20 completed baseline trades, bootstrap the latest 30 completed baseline net trade returns 250 times; accept only if at least 125/250 terminal paths are positive.
- Primary friction: 5 bps per leg; stress: 10 bps per leg.
- Brokerage/statutory charges remain explicit in the existing cost engine.

## Global information set
The workflow will fetch daily closes for S&P 500, Nasdaq-100, DAX, Nikkei 225 and Hang Seng. A larger secondary set may include FTSE 100, KOSPI, CAC 40, VIX and USDINR when data are available, but the primary five-market rule is fixed to prevent post-hoc feature selection.

## Frozen candidate global rule
The historical pilot supports testing a simple prior-session sign-consensus filter. The candidate rule is:
- compute the sign of the previous trading session return in each of the five global markets;
- consensus score ranges from -5 to +5;
- for LONG Indian entries, the candidate participation filter is consensus >= +3.

This threshold is NOT to be optimized on the 2026 test.

## Timing discipline
Only information that was available before the Indian entry is permitted. All global features are lagged by at least one calendar/trading day. No same-session foreign close that occurred after the Indian entry is allowed.

## Data hierarchy
A. Primary production source for the workflow: yfinance/Yahoo daily index history, cached on the GitHub Actions runner.
B. Secondary historical research source: omerfurkanguney/global-stock-indices-dataset, which documents 10 global indices from 2006–2026.
C. Earlier 2010–2022 cross-market pilot from VickykciV/Stock-Market-Network is hypothesis-generation only.

Raw third-party data are not committed to this repository. Derived summaries, hashes, provenance and code are committed/artifacted.

## Time split
- Train: 2006 through 2023.
- Validation: 2024–2025.
- Test: 2026 through the latest synchronized date available at execution.

The rule must be frozen before test evaluation. The 2026 window is a forward validation of the already-specified +3 rule; it is not a basis for choosing another threshold.

## Statistical analysis
Primary: mean/median per-trade net return, win rate, profit factor, maximum drawdown, paired trade-level difference where signals are matched, symbol-level bootstrap, block bootstrap by calendar month, Newey-West/HAC regressions for daily cross-market pilot, logistic/OLS models for conditional effects, and Benjamini-Hochberg correction over the finite pre-specified factor family.

## Promotion gate
A global filter can be promoted only if:
1. it improves the matched frozen baseline net of costs;
2. the improvement remains positive in the held-out period;
3. it remains positive under 5 and 10 bps-per-leg stress;
4. the effect is not concentrated in a few symbols;
5. the information set is available before entry;
6. the result survives an independent data-source comparison.

Otherwise the result is a descriptive cross-market effect, not a promoted trading rule.

## Stop rule
Phase 10 ends after the global pilot, one frozen OOS implementation, independent-source validation where feasible, and final evidence gate. No new indicator families or alternative threshold searches are allowed after the first OOS result.
