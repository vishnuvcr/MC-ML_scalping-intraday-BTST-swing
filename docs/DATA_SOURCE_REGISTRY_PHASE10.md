# Phase 10 Data-Source Registry

| Source | Use | Coverage / status | License / handling |
|---|---|---|---|
| omerfurkanguney/global-stock-indices-dataset | Independent historical global pilot | 10 indices, daily, 2006–2026; synchronized five-market subset currently ends 10 Feb 2026 | Public GitHub repository; use as secondary research source and record commit/date |
| ibrahimqasimi/global-stock-market-indices-2000-2026 (Kaggle) | Independent cross-check | 14 major indices, 2000–2026, Yahoo/yfinance sourced | Download at runtime where access permits; do not commit raw files |
| benjaminpo/finance-dataset | Broad global daily/intraday pipeline reference | US, Europe, Japan, Korea, Hong Kong, Taiwan, indices, rates, futures, crypto, currencies | Runner/Kaggle workflow data; raw files not copied into this repository |
| Yahoo Finance via yfinance | Primary Phase 10 workflow source | Current global index history; production run records actual end date and failed tickers | Runner cache only |
| NSE Indices / NikhilSuthar indian-market-data | Indian target / independent verification | NIFTY historical OHLC and TRI endpoints; 2026 examples documented | Use runtime download; raw files not committed |
| BSE API / indian-market-data | Indian target / cross-check | SENSEX and BSE indices; documented 2026 historical endpoint | Use runtime download; raw files not committed |

## Primary global tickers

S&P 500 (^GSPC), Nasdaq-100 (^NDX), DAX (^GDAXI), Nikkei 225 (^N225), Hang Seng (^HSI).

## Secondary global factors

FTSE 100 (^FTSE), KOSPI (^KS11), CAC 40 (^FCHI), VIX (^VIX), USDINR (USDINR=X), Brent (BZ=F), Gold (GC=F).

## Timing rule

All foreign-market inputs are lagged so the feature was observable before the Indian entry. Same-session information that becomes available only after the Indian entry is excluded.
## Newly verified independent sources

- Mohammadreza Amani, Global Stock Market Indices Historical Dataset — GitHub release dated 4 Jul 2026. The release notes state that available index histories were refreshed through July 2026, including S&P 500, NASDAQ, DAX, FTSE 100, Nikkei 225, Hang Seng and Sensex, plus VIX and futures. 
- Ibrahim Qasmi, Global Stock Market Indices 2000–2026 — Kaggle. The dataset documentation states daily OHLCV for 14 major indices across 12 countries, sourced via yfinance, with coverage through March 2026 and Apache 2.0 licensing.
- benjaminpo/finance-dataset — GitHub/Kaggle pipeline with daily and intraday global market data across US, Europe, Japan, Korea, Hong Kong, Taiwan, indices, rates, futures and currencies.