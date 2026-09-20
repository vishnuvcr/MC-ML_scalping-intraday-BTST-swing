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
