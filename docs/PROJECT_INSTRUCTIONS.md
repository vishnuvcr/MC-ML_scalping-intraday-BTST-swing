# Project Research Instructions

This repository follows a finite, auditable research protocol for Monte Carlo, scalping, intraday, BTST and swing studies.

## Required operating rules
- Read the current research plan, phase status, error log and relevant prior results before changing a phase.
- Keep each research phase on its own Git branch and provide a manual GitHub Actions workflow for the phase.
- Keep large third-party raw market files out of the repository unless licensing explicitly permits them; prefer runner cache and derived artifacts.
- Version data provenance, hashes, schema assumptions and cost assumptions.
- Include brokerage, statutory charges, spread, slippage, latency and partial-fill assumptions where relevant.
- Separate train, validation and test periods. Do not tune on the final test set.
- Log every material error and correction, including failures that produced no accepted result.
- Update phase status and decision logs after material steps.
- Do not promote a strategy from a single symbol, one regime, or one data source.
- Stop when the finite research plan and evidence gate are complete; do not expand indicator/parameter searches indefinitely.
- Final outputs must include methods, statistical analysis, results, limitations, conclusion and future research directions.

## Conversation log policy
The repository stores a concise reproducible decision and outcome log. Private chain-of-thought is never copied into repository files; the log records requests, decisions, evidence, errors and outcomes only.