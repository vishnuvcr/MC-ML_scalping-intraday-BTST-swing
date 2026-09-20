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