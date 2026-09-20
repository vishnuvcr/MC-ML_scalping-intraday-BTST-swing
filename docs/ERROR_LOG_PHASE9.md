# Phase 9 Error Log

| ID | Status | Issue | Correction |
|---|---|---|---|
| P9-E001 | active | The previous +14.33% TCS result was single-symbol evidence. | Reopen the candidate against a broad exact intraday panel and full-NSE daily panel before drawing a generalized conclusion. |
| P9-E002 | controlled limitation | Public exact 15-minute data are not yet verified for every NSE listing. | Use exact 15-minute replication on the published NIFTY-100 panel and label full-NSE intraday results as a separate proxy. |
| P9-E003 | controlled limitation | TejHQ BSE coverage begins 2024-07-08. | Restrict cross-market basis analysis to synchronized NSE/BSE dates after that cutoff. |
| P9-E004 | controlled limitation | Dr-Kitz hourly data are CC BY-NC 4.0. | Use runner cache only; do not commit raw third-party files. |

| P9-E005 | corrected | Hosted NIFTY-100 MCP `list_symbols` returned repeated JSON objects rather than one JSON array; the first parser expected a list and aborted before fetching any candles. | Rewrote the parser to collect repeated symbol objects line-by-line, retry 15-minute/5-minute/1-minute intervals, and resample to 15 minutes when only finer data are returned. |
| P9-E006 | corrected | The independent daily-only workflow omitted `huggingface_hub`, so TejHQ files could not be downloaded. | Added the dependency; the main broad-NSE workflow already verified that the TejHQ download succeeds. |
| P9-E007 | corrected | TejHQ BSE files are not available for 2018-2023; extending the daily workflow naively to 2018 caused a 404. | Download NSE from 2018 onward but BSE only from 2024-07 coverage; restrict cross-market analysis to synchronized BSE dates. |
| P9-E008 | controlled | Repeated push commits initially created many overlapping Phase 9 Actions runs; this saturated the runner pool and obscured the newest result. | Added per-workflow concurrency cancellation and separated the fast daily and broad-minute workflows. The old runs are treated as non-authoritative. |
| P9-E008 | controlled data limitation | Ganesh datasets cover Nifty500 rather than the literal entire NSE universe; the older repository has no declared license in GitHub metadata. | Use them for broad intraday replication only; use TejHQ for full-NSE EOD; keep raw files runner-only and record provenance/hashes. |
| P9-E010 | corrected | Nifty500 intraday script used timezone-aware signal timestamps against naive phase boundaries and could merge timezone-aware daily regimes with naive signal dates. | Normalize timestamps to Asia/Kolkata for market calculations but strip timezone only at the train/validation/test boundary and cross-section merge layer. |
| P9-E011 | corrected | The first 2026-only forward wrapper passed `--tej-root` to a copied script that did not declare the argument. | Added the argument and retained the already-acquired 2026 dataset; no empirical result from the failed run is accepted. |
| P9-E008 | corrected | Ganesh Nifty500 workflow manifest omitted the `os` import. | Added the import before regenerating the matrix. |
| P9-E009 | corrected | Ganesh shard analysis assumed the daily resample index was unnamed; the files carried a `ts` index name, causing `date` selection failures. | Reset the index and rename the actual first index column to `date`; discard all affected shard results. |

## P9-E011 — 2026-09-20 — Ganesh aggregate schema mismatch
**Status:** corrected.
All 12 Ganesh shards completed in workflow run 35509860780, but the aggregate job failed because the aggregator expected `mc_return` while the shard panel emitted `mc_ret`. The shard-derived data were retained; the aggregate failure was a code/schema error, not a research result. A compatibility wrapper was added so aggregation aliases `mc_ret` to the expected field without rewriting the historical shard artifacts.

## P9-E012 — 2026-09-20 — OOS capital-path contamination
**Status:** corrected in the Phase 9 global branch.
The first Ganesh aggregate contained implausibly extreme baseline returns for some symbols. Investigation showed that test trade returns were calculated using an equity path accumulated from 2018 onward, so earlier path distortions could change 2026 position size and percentage returns. The corrected engine resets evaluation equity to INR 100,000 at the 2026 test boundary. Earlier aggregate figures are non-authoritative.

## P9-E013 — 2026-09-20 — Global cross-market scope was incomplete
**Status:** corrected by protocol amendment.
The original Phase 9 cross-market variables were NSE/BSE-centric. The user's intended cross-market concept includes global markets. The active Phase 9 branch therefore adds strictly lagged global features from S&P 500, Nasdaq 100, FTSE 100, DAX, Nikkei 225, Hang Seng, KOSPI, Shanghai Composite, VIX, DXY, USD/INR, WTI and gold. Only source observations strictly before the Indian signal date are used. Raw Yahoo-derived files remain runner-only because yfinance explicitly cautions that the downloaded data are subject to Yahoo terms and are intended for personal/research use.

## P9-E014 — 2026-09-20 — Global gate selection control
**Status:** frozen.
The global gate is not optimized on the test set. It is a pre-specified binary risk-on condition: at least 5 of 8 global equity indices had positive prior-session returns and prior-session VIX change was non-positive. The same rule is evaluated at 5 and 10 bps/leg and compared with baseline and Monte Carlo-filtered variants.
