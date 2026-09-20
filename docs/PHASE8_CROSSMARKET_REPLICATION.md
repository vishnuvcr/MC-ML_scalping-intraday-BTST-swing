# Phase 8 Cross-Market Replication

Status: active on `phase-8-crossmarket-replication` (20 Sep 2026).

## Purpose

The large 214-symbol NSE 1-minute release cannot be dispatched from the current GitHub interface, and the execution runtime cannot resolve GitHub's large-release host. This amendment therefore adds two independently accessible public historical panels without changing the frozen EMA/Monte-Carlo decision rules:

1. **NSE/NIFTY historical panel:** 20 project symbols from `Ram9219/NIFTY-50-Stock-Market-Data-2000---2022-`, covering roughly 2012-2022. Test window: 2019-2022.
2. **BSE cross-market panel:** 19 available project symbols from `JashPancholi/BSE_STOCK_DATA`, covering 2023-2025. Test window: 2025.

These panels are validation evidence, not exchange-grade tick/bid-ask data.

## Frozen strategy rules

- EMA20/21 long-only crossover for BTST and swing.
- Entry at next-session open after the crossover.
- BTST: exit at the same day's close after the overnight hold.
- Swing: 0.75 ATR(14) stop and eight-session maximum holding period.
- Equity-capped position size: floor(equity / entry).
- Monte Carlo gate: 250 bootstrap paths using the last 30 realized trade returns, participation requires at least 125/250 positive paths after 20 historical trades.
- Friction scenarios: 0, 5 and 10 bps per leg.
- Paytm Money/statutory cost model remains the project model; historical exchange-specific fees are not reconstructed.

## Temporal design

### Historical NSE panel

- Model history: data through 2018.
- Test: 2019-01-01 through 2022-12-31.

### BSE panel

- Model history: 2023-01-01 through 2024-12-31.
- Test: 2025-01-01 through 2025-12-31.

## Exploratory runtime result before workflow rerun

An independently fetched BSE panel (19/20 requested files available) produced the following 2025 test results at 5 bps/leg:

| Horizon | Mean return | Median return | Positive symbols | Median PF |
|---|---:|---:|---:|---:|
| BTST | -2.55% | -2.94% | 4/19 | 0.13 |
| Swing | -3.36% | -3.28% | 6/19 | 0.45 |

The Monte-Carlo gate was not meaningfully exercised in this BSE replication because most symbols had fewer than 20 historical trades under the frozen EMA rule; MC therefore matched the baseline. This is an important limitation rather than evidence that MC has no value.

The historical NSE 20-symbol runtime check also showed a negative median test profile for both BTST and swing at 5 bps/leg. Its first ad-hoc aggregation exposed a NaN handling issue in the summary calculation; those exploratory values are retained only as a diagnostic and are **not** treated as final results. The workflow below reruns the calculation with explicit finite-value filtering.

## Decision rule

This amendment does not introduce new indicators or parameter searches. The frozen formulation is retained. If the two cross-market panels remain negative after the corrected workflow rerun, the evidence against the current EMA/MC formulation strengthens and the research should move to the pre-planned failure-mechanism analysis rather than uncontrolled indicator mining.

## Reproducibility

- Script: `scripts/phase8_crossmarket_replication.py`
- Workflow: `.github/workflows/phase-8-crossmarket-replication.yml`
- Source repository 1: https://github.com/Ram9219/NIFTY-50-Stock-Market-Data-2000---2022-
- Source repository 2: https://github.com/JashPancholi/BSE_STOCK_DATA
