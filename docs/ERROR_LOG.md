# Error Log

## E0001 — Empty repository
The repository was initially empty. Resolution: initialized research protocol and created the governance branch.

## E0002 — Paytm Money pricing page
The official pricing page did not expose all cash-equity brokerage fields in static HTML. Resolution: treat broker charges as versioned external inputs and re-verify before the cost model is frozen.

## E0003 — Local bootstrap script quoting error
A multi-file repository write script failed before execution because Markdown backticks conflicted with JavaScript template literals. Resolution: rewrote the payload with plain strings.
