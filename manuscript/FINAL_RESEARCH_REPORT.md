# Monte Carlo Methods for Stock Trading Across Scalping, Intraday, BTST and Swing Horizons

## A data-gated research report and reproducibility manuscript

**Date:** 20 September 2026
**Market context:** Indian equities; NSE/BSE; Paytm Money execution-cost context
**Study status:** Methodology and software validation complete; stock-level empirical profitability estimation blocked by validated market-data access.

## Abstract

This study was designed to determine whether Monte Carlo methods can be used in a statistically defensible and economically meaningful way for stock trading across scalping, intraday, BTST and swing horizons. The research treats Monte Carlo as a family of resampling and simulation methods rather than as a standalone trading strategy. The protocol pre-specifies matched non-Monte-Carlo baselines, realistic brokerage/statutory charges, spread and slippage, point-in-time data handling, out-of-sample evaluation, dependence-aware bootstrap methods, null/placebo tests and data-snooping controls including White Reality Check, Hansen SPA, Deflated Sharpe Ratio and Probability of Backtest Overfitting where appropriate.

The literature review supports Monte Carlo most strongly as a validation, uncertainty-quantification and risk-analysis framework. It does not establish that Monte Carlo alone creates predictive alpha. Current Indian cash-equity costs are material. Under the study's provisional cost configuration, a ₹100,000 buy and ₹100,000 sell round trip is approximately ₹82.68 of intraday cost before spread/slippage and approximately ₹182.68 with 2 basis points of spread plus 3 basis points of slippage per leg. A comparable delivery round trip is approximately ₹269.68 before spread/slippage. These are arithmetic illustrations, not trading results or brokerage quotes.

The empirical stock-level question remains unresolved because the repository does not currently contain licensed/validated datasets sufficient for the required scalping and intraday horizons, and public EOD substitutes may introduce survivorship, corporate-action or licensing problems. The research therefore stops at the pre-defined empirical gate. The defensible conclusion is that Monte Carlo is scientifically appropriate as a validation and risk layer, but no claim of profitable stock trading can be made from this study until the required point-in-time market data are supplied and the full out-of-sample analysis is executed.

## 1. Introduction

Trading-system studies are vulnerable to look-ahead bias, data snooping, multiple testing, serial dependence, execution costs and overfitting. Monte Carlo methods can help quantify uncertainty, stress trade sequences, estimate drawdown distributions, construct dependence-aware resamples and create placebo/null distributions. They can also be misused: naive IID shuffles can destroy dependence, repeated parameter search can create selection bias, and parametric price paths can give a false impression of empirical validation.

This research therefore asks not merely whether Monte Carlo produces attractive simulated equity curves, but whether a Monte Carlo component adds reliable information beyond a matched baseline while surviving realistic implementation frictions.

## 2. Research questions

**RQ1.** Does Monte Carlo add predictive or decision value beyond a matched baseline?

**RQ2.** Which Monte Carlo formulation, if any, is useful for scalping, intraday, BTST and swing horizons?

**RQ3.** Does any gross trading edge survive realistic brokerage, statutory charges, spread and slippage?

**RQ4.** Does an apparent edge survive multiple-testing and backtest-overfitting controls?

**RQ5.** Is performance stable across stocks, time periods and market regimes?

**RQ6.** Can Monte Carlo improve risk control even when it does not improve raw forecasting?

## 3. Aims and objectives

### Aim
Determine whether Monte Carlo methods provide statistically credible and economically meaningful improvement in stock-trading research across four holding horizons.

### Objectives
1. Separate trade-sequence bootstrap, dependent-return bootstrap, permutation/placebo tests, path simulation, parameter perturbation and drawdown/risk estimation.
2. Build a date-aware execution-cost model using current public NSE levy information and versioned Paytm Money inputs.
3. Compare Monte Carlo-enhanced systems with matched non-Monte-Carlo baselines.
4. Use strict train/validation/test separation and selection-aware statistical controls.
5. Measure net return, CAGR, Sharpe/Sortino, drawdown, profit factor, expectancy, turnover and tail risk.
6. Test stability across securities, years, volatility/liquidity regimes and horizons.
7. Produce reproducible code, data manifests, tests and a manuscript.

## 4. Literature review synthesis

The Stationary Bootstrap of Politis and Romano provides a resampling framework for weakly dependent stationary data and is preferable to naive IID bootstrap when serial dependence matters. Sullivan, Timmermann and White demonstrate why large technical-rule searches require explicit data-snooping correction. Hansen's Superior Predictive Ability test provides a selection-aware alternative to the Reality Check framework. Bailey and López de Prado's Deflated Sharpe Ratio addresses Sharpe inflation from selection and non-normality, while Bailey et al. propose Probability of Backtest Overfitting using combinatorial cross-validation. Indian high-frequency research by Patnaik and Thomas demonstrates that transaction costs and order execution are material components of short-horizon strategy evaluation.

Recent practitioner and preprint material is useful for implementation ideas, especially for bootstrap distributions, purging/embargoing and Monte Carlo drawdown analysis, but is treated below peer-reviewed statistical and finance evidence.

### Evidence conclusion
The literature supports Monte Carlo most clearly as a **validation and risk-analysis layer**. It does not justify treating Monte Carlo itself as a universal source of alpha.

## 5. Scientific methodology

### 5.1 Horizon-specific data requirements
- **Scalping:** tick/sub-minute data, preferably bid/ask and trade/order-book information.
- **Intraday:** 1-minute or finer data; bid/ask preferred.
- **BTST:** daily OHLCV plus next-session context where feasible.
- **Swing:** daily OHLCV plus point-in-time corporate actions and symbol history.

### 5.2 Baseline strategies
The study freezes simple baselines before optimization: benchmark/hold, moving-average trend, breakout, mean-reversion and volume/volatility filters. Baselines are deterministic and create the reference trade ledger.

### 5.3 Monte Carlo methods
**Trade-sequence bootstrap.** Resample completed trades to estimate terminal wealth and drawdown distributions.

**Stationary/block bootstrap.** Preserve some serial dependence through random-length blocks; used for time-series uncertainty.

**Permutation/placebo null.** Break the signal-return mapping only when the null's exchangeability assumptions are defensible.

**Parameter perturbation.** Vary parameters in a pre-specified neighborhood to reveal robust regions rather than rely on a single optimum.

**Parametric price-path simulation.** Kept separate as model-risk analysis and never substituted for empirical market data.

### 5.4 Execution model
Gross and net P&L are kept separate. The model includes brokerage, STT, stamp duty, SEBI turnover fees, exchange transaction charges, GST, spread and slippage; delivery/DP and MTF/financing components remain configurable.

Paytm Money's current public calculator states that platform fees, depository charges, auto-square-off charges and other fees are not included in the calculator, so the research does not treat the calculator as a complete all-in cost quote.[1]

### 5.5 Out-of-sample design
The intended empirical analysis uses point-in-time features, fixed train/validation/test boundaries, walk-forward testing and purged/embargoed procedures where overlapping labels create leakage risk. The primary test set is frozen before evaluation.

## 6. Statistical analysis plan

Primary outcomes are net CAGR, maximum drawdown, annualized Sharpe, Sortino, profit factor, expectancy, turnover and net return per unit turnover.

Inference uses dependence-aware bootstrap for dependent return streams, IID trade bootstrap only for trade-sequence risk questions, and permutation tests only under justified exchangeability. Strategy-family searches are corrected with White Reality Check and/or Hansen SPA. Deflated Sharpe Ratio is used when Sharpe has been selected from multiple trials. Probability of Backtest Overfitting/CSCV is used where a non-trivial selection process exists.

A result is classified as robustly profitable only if it is net profitable out-of-sample under the primary cost model and remains supported under the pre-specified robustness and cost/slippage sensitivity tests.

## 7. Phase results

### 7.1 Software verification
- Cost-engine unit tests: **4/4 pass**.
- Monte Carlo method tests: **4/4 pass**.
- Statistical utility tests: **2/2 pass**.
- Manual GitHub Actions workflows exist for Phases 0–5.

These are software verification results, not market-performance results.

### 7.2 Cost sensitivity illustration

| Scenario | Approx. cost on ₹100k buy + ₹100k sell | Cost as % of initial ₹100k capital |
|---|---:|---:|
| Intraday, no spread/slippage | ₹82.68 | 0.0827% |
| Intraday, 2 bps spread + 3 bps slippage per leg | ₹182.68 | 0.1827% |
| Delivery/BTST/swing, no spread/slippage | ₹269.68 | 0.2697% |
| Delivery/BTST/swing, 2 bps spread + 3 bps slippage per leg | ₹369.68 | 0.3697% |

The delivery case is strongly affected by the current 0.10% STT on both delivery purchase and sale. The intraday case has 0.025% STT on the non-delivery equity sale side. Current NSE levy information also lists 0.015% delivery stamp duty and 0.003% non-delivery stamp duty on the buyer, 0.0001% SEBI turnover fee and 18% GST on stock-broker services.[2]

### 7.3 Empirical profitability results
**Not estimable in this run.** No stock-level CAGR, Sharpe, p-value, confidence interval, win rate, drawdown or profitability classification is reported because the required validated market datasets are not present.

## 8. Inferences

1. Monte Carlo is methodologically useful even when it does not improve prediction: it can quantify drawdown, trade-sequence uncertainty and the stability of conclusions.
2. A Monte Carlo overlay can become another source of overfitting if the simulation design, block length or parameter choices are tuned against the same backtest.
3. Short-horizon profitability is highly sensitive to execution assumptions. The cost illustration shows that a strategy producing only a few basis points of gross edge per round trip could be economically fragile.
4. Delivery/BTST/swing strategies face a different cost structure from intraday/scalping, so a single Monte Carlo configuration should not be assumed to transfer across horizons.
5. There is currently insufficient evidence to say that Monte Carlo itself generates profitable stock-trading alpha.

## 9. Discussion

The central finding is methodological: **Monte Carlo should be evaluated as a conditional research component, not as the trading thesis itself.** The key scientific comparison is baseline versus matched Monte Carlo treatment under identical information sets and execution assumptions.

For scalping and intraday, the primary challenge is not merely statistical significance but microstructure realism. If bid/ask, delay, partial fills and market impact are not measured, a backtest may overstate economic performance. For BTST and swing, daily data can support a meaningful empirical study, but point-in-time universes and corporate actions remain essential.

The most defensible future experiment is therefore a four-horizon, multi-stock, walk-forward study in which the same baseline signal is evaluated with and without Monte Carlo risk/selection layers. The empirical question should be framed as an incremental-value test rather than a search for a universally profitable Monte Carlo strategy.

## 10. Strengths

- Pre-specified finite research plan.
- Explicit separation of Monte Carlo from the trading signal.
- Dependence-aware resampling included from the start.
- Realistic cost/slippage model with versioned inputs.
- Multiple-testing and backtest-overfitting controls pre-specified.
- Dedicated Git branches and manual workflows for phases.
- Tests and reproducibility logs kept in the repository.
- No fabricated empirical results when required data were unavailable.

## 11. Limitations

- No validated high-frequency stock dataset was available in the repository during this study run.
- The Paytm Money public calculator is not a complete all-in cost quote; account-specific and additional charges must be verified before final backtesting.[1]
- The cost illustration uses a provisional ₹20/order brokerage input and is not a personalized brokerage quote.
- Without out-of-sample market data, no statement about actual profitability, effect size or statistical significance can be made.
- Some advanced inference methods require careful implementation once the size of the strategy family and data structure are known.

## 12. Conclusion

The evidence supports a **qualified yes** to Monte Carlo's usefulness in stock-trading research, but **not a conclusion that Monte Carlo itself is a profitable trading strategy**. Monte Carlo is well suited to estimating uncertainty, drawdown, null distributions and robustness, while profitability must come from an underlying trading signal that survives out-of-sample testing and realistic execution costs.

For the specific question of whether Monte Carlo can be significantly used to trade stocks profitably across scalping, intraday, BTST and swing, the present study reaches a **data-gated conclusion**: the method is scientifically appropriate for the planned evaluation, but stock-level profitability remains unestablished until licensed/validated market data are supplied and the empirical phases are run.

## 13. Future research

1. Obtain licensed NSE/BSE historical data for tick/sub-minute/intraday and daily horizons with explicit redistribution/usage rights.
2. Freeze a point-in-time multi-stock universe and corporate-action history.
3. Run the pre-registered four-horizon matched baseline-vs-Monte-Carlo experiment.
4. Apply White Reality Check/SPA, DSR and PBO where applicable.
5. Repeat across volatility, liquidity and market regimes.
6. Add measured bid/ask and partial-fill execution simulation for scalping.
7. Validate the entire process on an independent future holdout before any live deployment consideration.

## 14. Reproducibility appendix

### Repository artifacts
- `RESEARCH_PROTOCOL.md`
- `docs/RESEARCH_PLAN.md`
- `docs/LITERATURE_REVIEW.md`
- `docs/DATA_SCHEMA.md`
- `docs/DATA_ACQUISITION_MANIFEST.md`
- `docs/COST_MODEL_2026.md`
- `docs/PHASE3_METHODS.md`
- `docs/PHASE4_STATISTICAL_PLAN.md`
- `docs/PHASE5_ROBUSTNESS_PLAN.md`
- `research_cost_engine.py`
- `research_monte_carlo.py`
- `research_statistics.py`
- `test_cost_engine.py`
- `test_monte_carlo.py`
- `test_statistics.py`
- `.github/workflows/phase-0-governance.yml` through `.github/workflows/phase-5-robustness-design.yml`

### Core references
[1] Paytm Money, Brokerage Calculator and pricing disclosures: https://www.paytmmoney.com/stocks/brokerage-calculator

[2] NSE India, SEBI Turnover Fees, STT and Other levies, updated 17 Apr 2026: https://www.nseindia.com/static/invest/first-time-investor-sebi-turnover-fees-stt-other-levies

[3] NSE India, Revision in Transaction Charges, Circular NSE/FA/73061, 27 Feb 2026: https://nsearchives.nseindia.com/content/circulars/FA73061.pdf

[4] Politis, D. N., & Romano, J. P. (1994). The Stationary Bootstrap. Journal of the American Statistical Association, 89(428), 1303–1313. https://doi.org/10.1080/01621459.1994.10476870

[5] Sullivan, R., Timmermann, A., & White, H. (1999). Data-Snooping, Technical Trading Rule Performance, and the Bootstrap. Journal of Finance, 54, 1647–1691. https://doi.org/10.1111/0022-1082.00163

[6] Hansen, P. R. (2005). A Test for Superior Predictive Ability. Journal of Business & Economic Statistics, 23(4), 365–380. https://doi.org/10.1198/073500105000000063

[7] Bailey, D. H., & López de Prado, M. (2014). The Deflated Sharpe Ratio. Journal of Portfolio Management, 40(5), 94–107. https://doi.org/10.3905/jpm.2014.40.5.094

[8] Bailey, D. H., Borwein, J., López de Prado, M., & Zhu, Q. J. (2017). The Probability of Backtest Overfitting. Journal of Computational Finance. https://doi.org/10.21314/JCF.2016.322

[9] Patnaik, T. C., & Thomas, S. (2004). Profitability of Trading Strategies on High-Frequency Data, with Trading Costs. SSRN 568363. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=568363

[10] Park, C.-H., & Irwin, S. H. (2010). A Reality Check on Technical Trading Rule Profits in the U.S. Futures Markets. Journal of Futures Markets, 30(7), 633–659. https://doi.org/10.1002/fut.20435

## Final research status
**Stopped at the pre-defined empirical gate on 20 September 2026.** The next research step is data acquisition/validation, not strategy invention or parameter optimization.


## 15. Phase 7 empirical continuation requested by the user

The empirical gate was reopened using a secondary public OHLCV dataset from the MIT-licensed `scriptkidakash81/stocks-data` research pipeline, which documents Yahoo Finance as its market-data source. Because the available 1-minute files were too large for the repository-fetch interface, 15-minute bars were used as a scalping proxy. This means the short-horizon results are not equivalent to tick/1-minute microstructure evidence.

### 15.1 Final common candidate framework
The primary candidate used:
- EMA(20/26) crossover for short horizons;
- EMA(20/21) crossover for daily horizons;
- ATR(14) stop;
- next-bar/day-open entry;
- fixed maximum holding period;
- Monte Carlo gate based on the last 30 net trades, 250 bootstrap resamples, and a 50% positive-path threshold once at least 20 prior trades exist;
- full transaction-cost treatment from the study cost engine.

### 15.2 Scalping proxy
For TCS, the 15-minute version with a 4-bar maximum hold and 1.5 ATR stop produced validation return of +0.74% (PF 1.14, 32 trades) and subsequent out-of-sample return of +5.59% (PF 1.71, Sharpe 1.17, maximum drawdown -2.94%, 40 trades).

This is the strongest short-horizon candidate from the screen, but it is not a validated true scalping strategy because bid/ask, latency, partial fills and 1-minute/tick data were not available.

### 15.3 Intraday
For TCS, the same EMA framework with a 20-bar maximum hold produced validation return of +3.00% (PF 1.49, 33 trades) and subsequent out-of-sample return of +14.33% (PF 2.87, Sharpe 2.10, maximum drawdown -1.92%, 40 trades).

This result is promising within the tested sample but is concentrated in one stock and one 15-minute dataset window. It therefore remains a research candidate rather than a live-validated system.

### 15.4 BTST correction and result
A previous daily experiment incorrectly reused an 8-session holding period for both BTST and swing. The BTST analysis was re-run correctly as exactly one overnight holding period: enter at the next session open after the signal and exit at that next session close.

The corrected results did not persist out of sample. For example, HDFCBANK had +7.54% validation return (PF 3.56) but -2.50% subsequent test return (PF 0.53). TCS had +0.39% validation and -9.35% test. No BTST strategy is therefore classified as usable.

### 15.5 Swing
The daily EMA(20/21), 8-session maximum-hold candidate produced HDFCBANK validation return of +6.75% (PF 1.38) and subsequent test return of +0.94% (PF 1.08, Sharpe 0.15). This is a weak positive observation, not robust evidence of deployable profitability.

Other stocks were heterogeneous, and SBIN's strong validation result did not persist into the test period. This prevents a universal swing-strategy claim.

### 15.6 Monte Carlo contribution
Across the tested families, the Monte Carlo gate usually reduced the number of trades and sometimes reduced drawdown. It did not consistently improve raw return. In the TCS intraday candidate, the MC component should therefore be interpreted mainly as a participation/risk filter rather than as the source of alpha.

### 15.7 Rejected 52-week-high experiment
A separate 52-week-high/momentum screen generated very large apparent returns on several symbols. It was rejected after identifying an invalid accounting design: overlapping positions were treated as sequentially compounded fixed-notional trades. That can dramatically inflate reported capital growth. The entire result is excluded from the research conclusion.

### 15.8 Final empirical conclusion
The requested finite empirical extension is complete. **No single cost-aware, out-of-sample-robust strategy was established across scalping, intraday, BTST and swing.** The strongest remaining research candidate is the TCS 15-minute EMA20/26 intraday system with the Monte Carlo gate. It is not sufficient to establish a general stock-trading strategy because of the single-symbol concentration, limited 15-minute history, lack of bid/ask/tick execution data and absence of a broad independent holdout.

The research therefore stops here rather than continue searching indicators on the same sample. That stop preserves the statistical validity of the project. A genuinely stronger next step would require new data—1-minute/tick/bid-ask history and a broader point-in-time stock universe—rather than additional parameter mining.
