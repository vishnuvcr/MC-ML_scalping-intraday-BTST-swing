# Phase 9 Data Source Registry

## Tier A — exact short-horizon replication
Source: https://github.com/vishalmdi/indian-stocks-mcp  
Hosted endpoint: https://vjaiswal-nifty-mcp.hf.space/mcp

Published documentation states that the hosted server provides 117 NIFTY 100 stock symbols, historical 1-minute candles, 6+ years of history, Asia/Kolkata timestamps, and read-only historical backtests/data access. Phase 9 will request 15-minute candles where supported; otherwise it will resample 1-minute candles.

This is a NIFTY-100 panel, not the entire NSE.

## Tier B — broad/full NSE daily
Source: https://huggingface.co/datasets/tejhq/indian-markets

The dataset documents raw NSE EOD OHLCV from official bhavcopy, roughly 2,300 instruments per day, from 2010-01-04 onward. It also provides turnover, volume, trades where available, corporate-action trees, symbol history, and point-in-time liquidity-universe data. Phase 9 will use the raw NSE tree for signal/execution prices and independently derive point-in-time liquidity features.

## Tier C — cross-market
Source: same TejHQ dataset, BSE raw tree. BSE coverage begins 2024-07-08. Same-symbol/ISIN cross-market basis variables are therefore restricted to dates on which synchronized BSE and NSE observations exist.

## Tier D — broad intraday proxy
Source: https://github.com/Dr-Kitz28/NSE-OHLCV-Data

The project documents daily and hourly OHLCV across its NSE stock universe. The repository license is CC BY-NC 4.0. Hourly files are therefore runner-cache inputs only and must not be committed or redistributed in this research repository.

## Data licensing rule

Raw third-party market data are not copied into the repository. Workflows may cache them on runners subject to source terms. Only derived aggregate research results, provenance, hashes and code are committed.


## Tier A2 — broad NSE minute universe

Source: https://huggingface.co/datasets/rahulkrraj/indian-stock-market-minute-data

The dataset publishes ~720 million minute rows covering 2,500+ NSE stocks and indices, describes coverage as 99.4% of active/suspended NSE equities and provides 1-minute candles from 2022-01-03 through 2026-01-21. The minute files are eight large ~1.4–1.6 GB Parquet shards sorted by symbol then timestamp. License is MIT. Phase 9 will process one shard at a time to avoid repeatedly downloading/caching 10.5 GB of raw files and will retain only derived results in the repository. citeturn893748search0turn893748search1

## Tier A3 — Ganesh Biyer broad intraday Nifty 500

### `ganeshbiyer/Nse_Historical_Data`
- README states 1-minute historical data for Nifty 500 stocks, 2018 through 31 Dec 2025.
- README states 1-minute files are Parquet and includes NIFTY, BankNifty, FinNifty and MidcapNifty indexes.
- Current Git tree contains 552 Parquet files; current blob sizes sum to about 5.87 GB.
- Repository has no declared license in GitHub metadata. Raw data will therefore never be copied into the project repository; runner-only use.

### `ganeshbiyer/Nse_Historical_Data_2026`
- README/repository description states 1-minute historical data for Nifty 500 stocks for 2026.
- Current Git tree contains 535 Parquet files; current blob sizes sum to about 1.19 GB.
- GitHub metadata declares GPL-3.0 for this repository. Raw data remains runner-only.

### Use in Phase 9
The two repositories will be treated as a continuous broad intraday panel: 2018–2025 from the first repository plus 2026 from the second. The frozen TCS EMA20/26 15-minute strategy is resampled from 1-minute data. Because the universe is Nifty 500 rather than all NSE listings, results will be labelled **Nifty-500 intraday replication**, not full-NSE intraday validation.

### Regime inputs
The Ganesh data include NIFTY50-INDEX, NIFTYBANK, FINNIFTY-INDEX and MIDCPNIFTY-INDEX files, enabling market-regime and cross-sectional benchmark variables directly inside the same intraday source family.

## Phase 9 global markets — added 2026-09-20

Global daily benchmarks are retrieved with yfinance from Yahoo Finance public APIs for research and educational analysis. The active tickers are S&P 500 (^GSPC), Nasdaq 100 (^NDX), FTSE 100 (^FTSE), DAX (^GDAXI), Nikkei 225 (^N225), Hang Seng (^HSI), KOSPI (^KS11), Shanghai Composite (000001.SS), VIX (^VIX), DXY (DX-Y.NYB), USD/INR (INR=X), WTI (CL=F) and gold (GC=F).

Raw global downloads are runner-only. The yfinance project documentation states that it is not affiliated with Yahoo Finance, is intended for research and educational use, and that actual downloaded data are governed by Yahoo terms. Source: https://ranaroussi.github.io/yfinance/

Alignment is strictly lagged to the Indian signal date to avoid time-zone leakage.
