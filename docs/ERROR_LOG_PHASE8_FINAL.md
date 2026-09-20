# Phase 8 Final Synthesis Error Log

| ID | Status | Issue | Correction |
|---|---|---|---|
| F001 | corrected | Final manuscript still stated that stock-level profitability was not estimable after empirical screening had produced results. | Manuscript rewritten to incorporate Phase 7/8 empirical evidence and explicitly distinguish exploratory candidates from robust strategies. |
| F002 | corrected | Historical-NSE exploratory aggregation first allowed non-finite values to contaminate the mean. | Reproducible script explicitly filters non-finite summary inputs; exploratory values were not treated as authoritative. |
| F003 | controlled limitation | 214-symbol 1-minute/F&O and TejHQ workflows could not be manually dispatched or independently observed from the current interface. | Workflows retained as reproducibility artifacts; no executed-result claim is made. |
