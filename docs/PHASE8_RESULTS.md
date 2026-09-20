# Phase 8 — Public Data Expansion: Corrected Interim Results

## Scope
This is an interim empirical record for the user-requested public-data expansion. It does not replace the planned independent-source run; it records what was reproducibly executed from an accessible GitHub mirror and what remains pending on GitHub Actions.

## Public data availability finding
Three materially useful public-data families were verified:
1. A Kaggle dataset with 1-minute data for 150 NSE stocks and 9 indices from 2017.
2. A Hugging Face minute/daily dataset with 2,500+ NSE stocks and indices, about 715 million minute rows for 2022–2026, plus daily data to 2000.
3. A GitHub release containing 214 NSE F&O underlying stocks at 1-minute resolution from 2024-04-01 to 2026-04-30.

A fourth source, TejHQ, provides exchange-derived daily NSE/BSE data, corporate actions, symbol history and a survivorship-bias-free liquidity universe.

## Accessible execution used for the interim screen
Source: `scriptkidakash81/stocks-data` GitHub mirror, using eight pre-selected liquid symbols:
TCS, RELIANCE, HDFCBANK, INFY, ICICIBANK, SBIN, AXISBANK, BHARTIARTL.

This mirror is from the same public-source family used in Phase 7 and therefore is not treated as independent confirmation. It is used here to validate the corrected engine and to avoid stopping merely because bulk external download is unavailable in the current runtime.

### 15-minute intraday, EMA20/26, ATR14 1.5 stop, max 20 bars
All figures are test-period net return per ₹100,000 starting equity with equity-capped sizing.

| Friction / leg | Mean test return | Median test return | Positive symbols | Median PF | Best | Worst |
|---:|---:|---:|---:|---:|---:|---:|
| 0 bps | -1.92% | -2.21% | 2/8 | 0.86 | +11.43% | -11.38% |
| 2.5 bps | -3.89% | -4.56% | 2/8 | 0.73 | +8.78% | -12.96% |
| 5 bps | -5.70% | -6.68% | 1/8 | 0.62 | +6.32% | -14.43% |
| 10 bps | -8.82% | -10.36% | 1/8 | 0.45 | +1.95% | -16.85% |

### 5-minute scalping proxy, EMA20/26, ATR14 1.5 stop, max 12 bars
| Friction / leg | Mean test return | Median test return | Positive symbols | Median PF | Best | Worst |
|---:|---:|---:|---:|---:|---:|---:|
| 0 bps | -3.71% | -3.74% | 1/8 | 0.58 | +2.73% | -8.86% |
| 2.5 bps | -5.79% | -5.82% | 1/8 | 0.42 | +0.60% | -11.07% |
| 5 bps | -7.65% | -7.68% | 0/8 | 0.31 | -1.39% | -13.03% |
| 10 bps | -10.79% | -10.81% | 0/8 | 0.18 | -4.79% | -16.25% |

### Daily BTST, exact one overnight, EMA20/21
| Friction / leg | Mean test return | Median test return | Positive symbols | Best | Worst |
|---:|---:|---:|---:|---:|---:|
| 0 bps | -1.87% | -1.43% | 1/8 | +0.34% | -4.95% |
| 2.5 bps | -1.89% | -1.45% | 1/8 | +0.30% | -4.85% |
| 5 bps | -1.89% | -1.45% | 1/8 | +0.26% | -4.73% |
| 10 bps | -1.89% | -1.45% | 1/8 | +0.18% | -4.48% |

### Daily swing, EMA20/21, 0.75 ATR stop, max 8 sessions
| Friction / leg | Mean test return | Median test return | Positive symbols | Best | Worst |
|---:|---:|---:|---:|---:|---:|
| 0 bps | -3.91% | -2.95% | 2/8 | +2.43% | -14.65% |
| 2.5 bps | -3.86% | -2.90% | 2/8 | +2.27% | -14.21% |
| 5 bps | -3.83% | -2.83% | 2/8 | +2.12% | -13.78% |
| 10 bps | -3.68% | -2.74% | 2/8 | +1.88% | -12.86% |

## Monte Carlo gate observation
With the pre-specified 250-bootstrap / 50%-positive-path gate, the corrected 5 bps screen was highly restrictive. All eight symbols had zero validation/test trades after the gate had accumulated at least 20 historical trades; the gate therefore acted as a participation filter rather than producing incremental alpha in this interim screen.

## Interpretation
The corrected interim screen materially weakens the earlier single-symbol TCS result when the same frozen signal is applied across a pre-selected multi-stock set and realistic costs. It does not establish that the underlying idea is universally loss-making because the accessible mirror begins in late 2025 for intraday data and is not the planned independent 214-symbol release. It does establish that the Phase 7 single-symbol result cannot be generalized from the current evidence.

## Remaining Phase 8 execution
The GitHub Actions workflow is configured to:
- cache the 214-symbol 1-minute release by SHA-256;
- extract a frozen 20-symbol subset;
- fetch TejHQ daily data;
- run the same frozen strategies at 5m/15m/daily horizons;
- compare no-MC and MC variants;
- sweep 0/2.5/5/10 bps friction;
- upload a reproducible result artifact.

Until that workflow is executed, the public-source expansion remains partially complete rather than fully closed.

## Phase 8.1 cross-market replication update — 20 Sep 2026

### Corrected preliminary historical-NSE panel

Twenty project symbols were fetched from the public historical NIFTY-50 repository. Test window: 2019-01-01 to 2022-12-31. At 5 bps/leg, the corrected exploratory aggregate was BTST mean -4.97%, median -4.61%, 4/19 positive symbols, median PF 0.50; swing mean -3.69%, median -7.51%, 7/19 positive symbols, median PF 0.62. These preliminary values are internally consistent after explicit finite-value filtering but remain subordinate to the GitHub Actions artifact when that run is observable.


An independently accessible BSE panel covering 19 requested project symbols for 2023-2025 produced negative 2025 test medians under the frozen EMA20/21 daily rules at 5 bps/leg: BTST median -2.94% with 4/19 positive symbols and median PF 0.13; swing median -3.28% with 6/19 positive symbols and median PF 0.45. The Monte-Carlo gate was not materially exercised because most symbols did not reach the 20-trade warm-up; this is recorded as a limitation.

A separate 20-symbol historical NSE panel (roughly 2012-2022, test 2019-2022) was also fetched and screened. Its first exploratory aggregation exposed a non-finite-summary handling error, which is now corrected in the reproducible workflow. Those exploratory NSE aggregate values are not treated as final evidence; the workflow artifact is authoritative.

**Phase 8 decision status:** no cost-aware, cross-source universal BTST/swing strategy has been established. Continue only through the finite pre-planned validation/failure-mechanism path, not open-ended indicator mining.
