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
