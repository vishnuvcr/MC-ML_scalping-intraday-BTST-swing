# Phase 1 Data Source Audit

## Horizon requirements

- Scalping: tick/order-trade or 1-minute data with explicit spread limitations.
- Intraday: 1-minute or finer OHLCV; order/trade data preferred.
- BTST: daily data plus next-session/open context where possible.
- Swing: daily data with corporate-action and symbol-history treatment.

## Primary sources
- NSE historical reports provide security-wise price-volume archives and historical market reports. NSE also offers paid historical order/trade data for the capital-market segment.
- BSE offers EOD, historical trade and corporate/reference data products for back-testing and risk analysis.
- Paytm Money official pricing is the primary source for broker-specific charges.
- SEBI official circulars and documents are the primary regulatory source.

## Data-quality rules
- Point-in-time symbols and corporate actions.
- No survivorship-only universe for final inference.
- Asia/Kolkata timestamps.
- Detect duplicates, out-of-order records and missing bars.
- Do not blindly forward-fill market gaps.
- Record adjustment methodology.
- Create train/test boundaries before feature computation where possible.
- Store source timestamps and data hashes.

## Caching and licensing
Raw licensed data will not be redistributed unless licensing permits. When raw data cannot be committed, retain schema definitions, acquisition manifests, source metadata and cryptographic hashes. Legally redistributable derived datasets may be cached in data/processed/.
