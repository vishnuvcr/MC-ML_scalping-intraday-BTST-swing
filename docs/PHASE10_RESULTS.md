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

## 4. Effect-size / significance check on the independent pilot

For the SENSEX pilot, the high-consensus (>= +3) versus low-consensus (<= -3) mean-return difference was:

- Train: +0.377 percentage points, Welch t ≈ 6.42.
- Validation: +0.236 percentage points, Welch t ≈ 2.01.
- 2026 synchronized sample: -0.154 percentage points, Welch t ≈ -0.40, with only 11 high-consensus and 2 low-consensus observations.

These calculations are descriptive split-sample diagnostics, not proof of a tradable strategy. The very small 2026 low-consensus sample makes the test-period comparison particularly unstable.

## Execution status — 20 Sep 2026

The first Phase 10 Actions runs failed in the OOS artifact-download path because the workflow expression was malformed and the pilot path did not need that artifact. This was an infrastructure failure, not a market-data result. The workflow has been simplified to a deterministic pilot-only run; OOS joining is intentionally deferred until the corrected Phase 9 authoritative artifact exists.

## 5. Fresh full-period workflow result — 20 Sep 2026

The corrected Phase 10 pilot completed successfully using Yahoo Finance/yfinance data through **18 Sep 2026**.

The pre-specified rule remains unchanged: **prior-session five-market sign consensus >= +3**.

### NIFTY 50

| Split | All days | Consensus >= +3 | Consensus <= -3 | High-minus-low |
|---|---:|---:|---:|---:|
| Train 2006–2023 | +0.0488% | +0.5580% | -0.6068% | +1.1649 pp |
| Validation 2024–2025 | +0.0406% | +0.2536% | -0.3111% | +0.5647 pp |
| Test 2026 through 18 Sep | -0.1090% | **+0.2962%** | -0.5312% | **+0.8274 pp** |

The 2026 test contains 48 high-consensus observations and 36 low-consensus observations. The positive high-consensus mean therefore survives into the currently available 2026 forward sample, unlike the earlier independent dataset that ended in February and had only 11 high-consensus observations.

### SENSEX

| Split | All days | Consensus >= +3 | Consensus <= -3 | High-minus-low |
|---|---:|---:|---:|---:|
| Train 2006–2023 | +0.0541% | +0.5652% | -0.6258% | +1.1910 pp |
| Validation 2024–2025 | +0.0365% | +0.2528% | -0.3020% | +0.5549 pp |
| Test 2026 through 18 Sep | -0.1202% | **+0.2709%** | -0.5315% | **+0.8025 pp** |

### Interpretation

This is materially stronger evidence for the **global-information hypothesis** than the February-only snapshot. The direction is consistent across NIFTY 50 and SENSEX and across train, validation and the currently available 2026 test.

However, this remains a **market-index conditioning result**, not a completed trading strategy. It has not yet been demonstrated that the filter increases the net expectancy of the stock-level EMA20/26 strategy after realistic execution costs. That requires joining the global feature to the corrected Phase 9 stock-level trade panel.

A crude 20-bps round-trip subtraction from the 2026 high-consensus index means gives approximately +0.096 percentage points for NIFTY 50 and +0.071 percentage points for SENSEX. This is only a stress illustration; it is not the final execution-cost model.

**Phase 10 conclusion is therefore: GLOBAL FILTER = PROMISING, NOT YET PROMOTED.**
