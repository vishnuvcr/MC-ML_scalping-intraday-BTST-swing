# Error Log

## E0001 — Empty repository
The repository was initially empty. Resolution: initialized research protocol and created the governance branch.

## E0002 — Paytm Money pricing page
The official pricing page did not expose all cash-equity brokerage fields in static HTML. Resolution: treat broker charges as versioned external inputs and re-verify before the cost model is frozen.

## E0003 — Local bootstrap script quoting error
A multi-file repository write script failed before execution because Markdown backticks conflicted with JavaScript template literals. Resolution: rewrote the payload with plain strings.

## E0004 — Repository write guard blocked longer data/cost files
Two longer Phase 1 writes were blocked by the repository tool safety layer before mutation. Resolution: reduced the data audit to a smaller atomic file and deferred detailed broker-cost configuration to a later phase where inputs can be verified and versioned cleanly.

## E0005 — Out-of-scope file handle in update script
A follow-up update referenced a file handle from a previous tool invocation. No repository mutation occurred. Resolution: refetched the file and used the fresh blob SHA.

## E0006 — Empirical data gate reopened with secondary public OHLCV
The user requested empirical continuation, so a public secondary OHLCV dataset was used. It is not exchange-grade tick/order-book data and 15-minute bars were used as the scalping proxy. This limitation is now explicit in the results.

## E0007 — First multi-stock run exceeded execution time
The initial six-stock multi-family run timed out before emitting results. No repository mutation occurred. Resolution: reduced each experiment to fixed, bounded parameter grids and aggregated only completed results.

## E0008 — True BTST holding-period mismatch
A previous daily run reused an 8-session holding configuration for both BTST and swing. That was not a true BTST test. Resolution: reran BTST as exactly next-open to next-close; the corrected BTST result did not persist out of sample.

## E0009 — Overlapping-position accounting error in a 52-week-high experiment
A preliminary momentum experiment allowed overlapping positions while sequentially compounding fixed notional capital. That produced exaggerated apparent returns and is invalid for portfolio inference. Resolution: rejected the result and excluded it from conclusions.

## E0010 — Available repository-fetch interface could not return the very large 1-minute files
The accessible 1-minute file existed in the public research dataset but exceeded the file-fetch interface limit. Resolution: use 15-minute data as a clearly labelled scalping proxy and do not claim true tick/1-minute scalping validation.


## E0021 — 2026-09-20
Status: controlled limitation.
The available GitHub interface can create/push workflows but cannot manually dispatch a workflow run; the research therefore treats the workflow as reproducibility infrastructure and does not claim its artifact has executed until a run is observable.
Correction: use independently accessible public-source replication for interim evidence and retain the manual workflow for runner execution.
