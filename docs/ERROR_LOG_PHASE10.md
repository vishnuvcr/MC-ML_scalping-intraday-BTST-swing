# Phase 10 Error Log

| ID | Status | Issue | Correction |
|---|---|---|---|
| P10-E001 | corrected | “Cross-market inefficiency” had been interpreted too narrowly as NSE/BSE. | Phase 10 explicitly includes global equity markets and cross-session information flow. |
| P10-E002 | controlled | The first global pilot used a 2010–2022 historical source. | Treat it strictly as hypothesis generation; freeze the rule before the 2026 test. |
| P10-E003 | controlled | The independent 2006–2026 global-index repository is synchronized only through 10 Feb 2026 across the chosen five markets. | Use yfinance as the production source for the latest synchronized test and record the actual end date at runtime. |
| P10-E004 | corrected | Ganesh aggregate failed because the aggregator expected mc_return while shard panels produced mc_ret. | Aggregator now reads mc_ret. |
| P10-E005 | corrected | Raw Ganesh 1-minute data can contain mechanical scale breaks around corporate actions, generating impossible percentage returns. | Add a deterministic corporate-action scale normalization before EMA/ATR/resampling. Exclude and log ambiguous breaks rather than treating them as alpha. |
| P10-E006 | corrected | The initial MC implementation used accepted MC trades as its own history, which can permanently suppress participation and makes the comparison non-matched. | MC gate now uses completed baseline trade outcomes as the historical distribution; MC equity is tracked separately. |
| P10-E007 | corrected | The initial short-horizon loop did not enforce one-position-at-a-time accounting. | Candidate generation now advances past each exit before creating the next trade. |
| P10-E008 | controlled | The current branch has not yet observed a successful corrected Phase 9 GitHub Actions aggregate. | No corrected Phase 9 result is presented as final until the workflow artifact is observed. |

| P10-E009 | controlled | Direct container download of public GitHub raw market files failed because the execution environment could not resolve raw.githubusercontent.com. | Keep public-data acquisition in GitHub Actions/yfinance and use web/GitHub metadata for source verification; do not treat local container download failure as missing market data. |
