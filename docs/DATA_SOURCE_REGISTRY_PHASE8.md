# Phase 8 Data Source Registry

| Source | Resolution | Coverage | License / terms | Lineage | Role |
|---|---|---|---|---|---|
| tejhq/indian-markets | Daily | NSE ~2010-today; BSE 2024-today | MIT pipeline; verify exchange terms for commercial use | Official NSE/BSE bhavcopy + corporate actions | Primary daily universe |
| voletiramu/nse-fno-1min-data v1.0.0 | 1-minute | 214 NSE F&O underlyings; 2024-04-01 to 2026-04-30 | Public GitHub release; terms require review | Source stated as Zerodha Kite API | Primary HF exploratory |
| Kaggle hk7797/stock-market-india | 1-minute | 150 NSE stocks + 9 indices; from 2017 | CC BY-NC-SA 4.0 | Dataset card states Indian NSE minute data | Independent HF cross-check |
| HF rahulkrraj/indian-stock-market-minute-data | 1-minute + daily | 2,500+ NSE stocks/indices; minute 2022-2026, daily 2000-2026 | MIT | Dataset card; upstream provenance audit required | Broad HF candidate |
| GitHub ShabbirHasan1/nse-data-1 | Minute historical | Many NSE securities | Repository source/licence terms require review | Described as Zerodha/Kite historical research data | Secondary cross-check |

## Required metadata
Exact URL; retrieval timestamp; source coverage; file size; checksum/digest; schema; timezone; adjustment policy; licence/usage note; transformation version; filtered symbol count; filtered row count.

## Evidence classification
EXPLORATORY_PUBLIC = research screening only, not exchange-certified.

CROSS_SOURCE = independently reproduced or compared across two public sources.

LICENSED_VALIDATED = licensed/verified dataset meeting the original protocol.

Only LICENSED_VALIDATED supports a production/live-data equivalence claim.
## Auxiliary candidate sources identified during expansion
- TusharQLab/market-data: public GitHub pipeline for about 150 Nifty 200 stocks with 1-minute, 5-minute and 1-hour data and automated refresh.
- vishalmdi/indian-stocks-mcp: public service advertising 117 NIFTY 100 stock symbols at 1-minute resolution with 6+ years and 187M+ candles, refreshed from Kaggle-backed sources.
- SantoshSrinivas79/NSE-FNO-Data-bank: validated NSE F&O bhavcopy archive from April 2020 through August 2026; useful for official daily derivatives cross-check.
- Kaggle ramamet4/nse-stocks-database: older 1-minute NIFTY 50 and Bank Nifty data for 2013-2016; historical robustness only.