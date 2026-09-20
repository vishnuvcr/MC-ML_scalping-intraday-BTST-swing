# Phase 2 Data Acquisition Manifest

| Dataset | Horizon | Resolution | Preferred source | License status | Current status |
|---|---|---|---|---|---|
| NSE cash EOD | BTST/swing | Daily | NSE historical reports | Exchange terms to verify | Required |
| NSE intraday | Intraday | 1 min | Licensed exchange/vendor feed | Must verify | Required |
| NSE tick/order-trade | Scalping | Tick/order-book | NSE paid historical/order-trade feed | Must verify | Required |
| BSE EOD/corporate | Cross-check/supplement | Daily | BSE historical products | Exchange terms to verify | Optional |
| Corporate actions | All | Event | Exchange/company filings | Public-source terms | Required |
| Point-in-time symbol master | All | Event/snapshot | Exchange listings and historical reference | Public-source terms | Required |

## Reproducibility requirements
Every downloaded dataset must record source, retrieval timestamp, requested period, file hash, schema version, adjustment method, timezone, license/usage note and transformation code version.

## Caching policy
Do not redownload identical immutable historical files in every workflow run. Cache or commit only data that may legally be redistributed. Otherwise commit manifests, hashes and deterministic acquisition scripts.

## Universe rule
The final study must not use today's constituents as a proxy for historical stock membership without explicitly labelling the experiment as current-constituent-only. A point-in-time universe is the primary target.
