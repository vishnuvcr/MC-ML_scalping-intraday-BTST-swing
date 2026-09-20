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

| P9-E011 | corrected | Run 6 aggregate failed with KeyError: mc_return although shard signal_panel.csv used mc_ret. | Aggregator changed to consume mc_ret; previous aggregate is non-authoritative and must not be used as final evidence. |
| P9-E012 | corrected | Raw Ganesh 1-minute data contained obvious corporate-action scale breaks that produced impossible trade returns in affected symbols. | Added deterministic split/consolidation scale normalization before indicator/resampling; ambiguous breaks are logged/excluded. |
| P9-E013 | corrected | MC gate history was updated only from accepted MC trades, making the MC comparison self-referential and capable of suppressing all later trades. | MC gate now uses completed baseline trade returns as the historical distribution and tracks MC equity separately. |
| P9-E014 | corrected | Short-horizon loop could create overlapping candidate positions before the previous position exited. | Candidate generation now advances past each exit and enforces one position at a time per symbol. |

| P9-E015 | invalidated | Corrected aggregate completed, but independent artifact inspection still shows impossible intraday returns (e.g. repeated ~+490% and ~-83% moves in ZFCVINDIA) and compounded returns reaching tens of millions %. These are inconsistent with ordinary NSE trading and indicate remaining corporate-action/data-scale discontinuities not caught by the daily-open detector. | Do not use this aggregate for strategy inference. Extend scale-break detection to intraday bars and rerun from raw data. |
