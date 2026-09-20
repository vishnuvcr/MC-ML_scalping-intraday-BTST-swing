# Phase 9 Error Log

| ID | Status | Issue | Correction |
|---|---|---|---|
| P9-E001 | active | The previous +14.33% TCS result was single-symbol evidence. | Reopen the candidate against a broad exact intraday panel and full-NSE daily panel before drawing a generalized conclusion. |
| P9-E002 | controlled limitation | Public exact 15-minute data are not yet verified for every NSE listing. | Use exact 15-minute replication on the published NIFTY-100 panel and label full-NSE intraday results as a separate proxy. |
| P9-E003 | controlled limitation | TejHQ BSE coverage begins 2024-07-08. | Restrict cross-market basis analysis to synchronized NSE/BSE dates after that cutoff. |
| P9-E004 | controlled limitation | Dr-Kitz hourly data are CC BY-NC 4.0. | Use runner cache only; do not commit raw third-party files. |

| P9-E005 | corrected | Hosted NIFTY-100 MCP `list_symbols` returned repeated JSON objects rather than one JSON array; the first parser expected a list and aborted before fetching any candles. | Rewrote the parser to collect repeated symbol objects line-by-line, retry 15-minute/5-minute/1-minute intervals, and resample to 15 minutes when only finer data are returned. |
| P9-E006 | corrected | The independent daily-only workflow omitted `huggingface_hub`, so TejHQ files could not be downloaded. | Added the dependency; the main broad-NSE workflow already verified that the TejHQ download succeeds. |