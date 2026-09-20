# Phase 7 Error Log

## E0007 — Phase-7 first branch creation argument mismatch
The initial branch creation call used the wrong base parameter. No mutation occurred. Resolution: reissued with the repository connector's base_ref field.

## E0008 — Multi-stock simulation timeout
The first all-symbol simulation attempted too many parameter combinations and timed out before producing results. No repository mutation occurred. Resolution: reduce experiment scope per run, freeze smaller candidate grids, and aggregate completed runs.

## E0009 — Large CSV connector limit
The connector could list large CSVs but could not read their full contents. Resolution: use moderate-sized readable files for exploratory execution and record the limitation rather than silently substitute data.
