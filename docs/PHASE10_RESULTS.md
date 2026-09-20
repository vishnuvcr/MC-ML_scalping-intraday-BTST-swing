# Phase 10 Results

## 1. Historical pilot — hypothesis generation

A previous 2010–2022 common-date pilot using S&P 500, Nasdaq-100, Nikkei 225, Hang Seng and DAX showed:

| Prior-session global sign consensus | N | Next-day NIFTY mean return | Win rate |
|---|---:|---:|---:|
| +5 | 415 | +0.3479% | 62.65% |
| +3 | 473 | +0.2365% | 63.21% |
| +1 | 579 | +0.0651% | 54.58% |
| -1 | 502 | -0.0470% | 51.00% |
| -3 | 378 | -0.0996% | 47.88% |
| -5 | 313 | -0.2151% | 43.13% |

The +5 versus -5 mean-return difference was about 0.563 percentage points in that historical pilot. This was hypothesis-generation only and is not a live/OOS result.

## 2. Independent current-source pilot

A second global-index repository documents ten daily global indices from 2006 to 2026. Using the synchronized subset of S&P 500, DAX, FTSE 100, Hang Seng and KOSPI to predict the next synchronized SENSEX session:

- Train (2006–2023): consensus >= +3 mean SENSEX return +0.2140%, versus consensus <= -3 at -0.1632%.
- Validation (2024–2025): consensus >= +3 mean +0.1536%, versus <= -3 at -0.0824%.
- Current 2026 synchronized sample through 10 Feb 2026: only 25 common target days; consensus >= +3 mean -0.1592%.

### Interpretation

The training and validation samples show a repeatable directional association, but the available 2026 synchronized sample is small and does not reproduce the positive directional mean. This is exactly why Phase 10 must not promote a global filter from historical correlation alone.

## 3. Phase 9 execution correction

The first Ganesh Nifty500 Phase 9 workflow produced successful shard artifacts but its aggregate job failed on a column-name mismatch. Review of the artifacts also exposed corporate-action scale breaks in raw 1-minute series, a Monte-Carlo gate history implementation that was not strictly baseline-relative, and overlapping-position/capital-accounting risk.

These observations invalidate that aggregate as final strategy evidence. A corrected engine has now been frozen on the Phase 10 branch; no result from the failed aggregate is promoted.

## Evidence gate

Current Phase 10 status: NO GLOBAL FILTER PROMOTED.

The useful result at this stage is that global lead/lag is empirically detectable in long historical samples, but current forward evidence is insufficient to claim a stable profitable edge. The next decisive test is the frozen global filter applied to the corrected Phase 9 trade engine with 2026 forward data and full cost accounting.
