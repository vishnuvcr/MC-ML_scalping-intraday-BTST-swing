# Phase 8 Cross-Market Error Log

| ID | Status | Error / observation | Correction |
|---|---|---|---|
| E0017 | corrected in workflow | First ad-hoc historical-NSE aggregation propagated non-finite return values into the mean summary. | Final script filters all summary statistics to finite values before aggregation. |
| E0018 | known limitation | BSE panel contains 19/20 requested files because the M&M raw file URL required encoded '&'. | Workflow uses `M%26M.csv`; missing-file status is recorded rather than silently excluded. |
| E0019 | known limitation | BSE 2023-2025 panel rarely reaches the pre-specified 20-trade MC warm-up, so MC does not materially filter trades. | Do not interpret BSE MC equality with baseline as evidence of no MC effect. |
| E0020 | known limitation | Historical/public CSVs do not reconstruct bid/ask spreads or historical Paytm Money pricing. | Keep 0/5/10 bps sensitivity and the current Paytm Money/statutory cost model; label results as public-data research evidence. |
