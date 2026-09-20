# Phase 8 Error / Correction Log

Updated: 20 September 2026

| ID | Step | Issue | Effect | Correction / disposition |
|---|---|---|---|---|
| E0010 | Public-data acquisition | Direct runtime could not resolve github.com DNS while attempting the 486 MB F&O release. | Full public release could not be loaded into this runtime. | Retained source manifest; use GitHub Actions runner for bulk download and cache; accessible GitHub mirror used for an 8-symbol verification screen. |
| E0011 | First HF screen | Fixed-notional position sizing allowed cumulative losses to exceed starting capital. | Invalid negative-capital-like returns. | Entire output discarded. Re-ran with equity-capped quantity=floor(equity/entry) and equity-based drawdown. |
| E0012 | First daily screen | BTST and swing branches shared a holding-period path. | BTST could inherit swing-like holding periods. | Entire daily output discarded. Re-ran BTST as exactly next-open to next-close and swing as 8-session max hold. |
| E0013 | Phase 8 workflow | Workflow was committed to the phase branch but no workflow run was observed through the available GitHub read interface. | New-source bulk screen not yet independently executed in this runtime. | Workflow retained with manual `workflow_dispatch`; next execution is intended on GitHub Actions. |
| E0014 | HF parser review | F&O release uses Unix `time` seconds and one gzipped CSV per symbol. Initial parser expected a conventional datetime column. | Workflow would fail or misparse source timestamps. | Parser corrected to detect `time`, parse Unix seconds, then convert UTC→Asia/Kolkata. |
| E0015 | HF extraction review | Initial workflow extracted all symbol files into one directory while the Python engine expects one directory per symbol. | Source resolution would fail for most symbols. | Workflow corrected to extract each symbol into `raw/fno/<SYMBOL>/`. |

## Rule
All discarded outputs are excluded from the research conclusion. Only corrected reruns are eligible for synthesis.
| E0016 | True 1-minute interim screen | Connector rejected the 1m CSV payload as too large before contents could be processed. | No 1m backtest result accepted from that attempt. | Keep 1m work in GitHub Actions/cache; use only corrected 5m/15m and daily interim results here. |
