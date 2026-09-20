# Phase 2 Canonical Market Data Schema

## Required fields
- timestamp_ist: timezone-aware session timestamp.
- symbol: point-in-time exchange symbol.
- open, high, low, close: numeric prices.
- volume: traded volume.
- turnover: traded value where available.
- bid, ask, bid_size, ask_size: required for tick/order-book research; optional for EOD data.
- corporate_action_id: reference to the adjustment/event table.
- source_id: immutable source identifier.

## Derived metadata
- session_date
- bar_interval
- data_source_version
- raw_file_sha256
- adjustment_method
- quality_flags

## Horizon rules
Scalping requires tick/sub-minute data when available. Intraday minimum is 1-minute bars for the baseline study. BTST and swing can use EOD data, but the universe and corporate actions must remain point-in-time.

## Validation
Reject or flag duplicate timestamps, negative/zero prices, impossible OHLC relationships, non-monotonic timestamps, suspicious volume jumps, missing sessions and symbol changes. Do not forward-fill prices across trading-session gaps.
