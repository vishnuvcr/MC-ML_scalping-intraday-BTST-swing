# Phase 1 Literature Review — Monte Carlo, Backtesting and Trading

## Scope
The review focuses on Monte Carlo and bootstrap methods used for trading-strategy validation, statistical inference, drawdown/risk analysis, and simulated price paths. It also covers data-snooping, backtest overfitting, Indian market transaction costs, and execution/microstructure.

## Evidence map

| Source | Evidence type | Main contribution | Relevance |
|---|---|---|---|
| Politis & Romano (1994), The Stationary Bootstrap | Peer-reviewed statistics | Resamples weakly dependent stationary observations | Supports dependence-aware bootstrap instead of IID shuffles |
| Sullivan, Timmermann & White (1999/2002), Data-Snooping, Technical Trading Rule Performance, and the Bootstrap | Journal of Finance | Applies White Reality Check to a large universe of technical rules | Essential for multiple-testing/data-snooping control |
| Hansen (2005), A Test for Superior Predictive Ability | Journal article | SPA improves on Reality Check by reducing sensitivity to poor alternatives | Candidate strategy-family inference |
| Bailey & Lopez de Prado (2014), Deflated Sharpe Ratio | Journal of Portfolio Management | Adjusts Sharpe evidence for selection bias and non-normality | Required when many variants are tested |
| Bailey et al. (2014/2017), Probability of Backtest Overfitting | Journal of Computational Finance | CSCV/PBO estimates chance that a selected backtest is overfit | Strategy-selection audit |
| Arian, Norouzi Mobarekeh & Seco (2024) | Knowledge-Based Systems | Controlled comparison of OOS methods; reports CPCV advantages in their synthetic setting | Motivates purging/embargoing and CPCV sensitivity tests |
| Patnaik & Thomas (2004) | Indian-market research | High-frequency Indian equity strategies tested with actual order-book execution and transaction costs | Direct precedent for Indian intraday cost-aware testing |
| Hsu & Kuan (2005) | Technical-analysis research | Reality Check and SPA used on trading-rule universes | Supports data-snooping-aware rule evaluation |
| Park & Irwin (2010) | Journal of Futures Markets | Reality Check and SPA applied to technical-rule profits | Demonstrates that apparent best rules can lose significance after correction |
| Brock, Lakonishok & LeBaron (1992) | Journal of Finance | Early technical-rule study using bootstrap-based inference | Historical precedent for bootstrap trading research |
| Wijesinghe (2026) | SSRN preprint | Walk-forward, DSR, bootstrap CIs and Monte Carlo trade resampling under realistic costs | Very recent practitioner-research precedent; treat as preprint, not settled evidence |
| Physica A (2025), MC with jump-diffusion | Peer-reviewed article | Monte Carlo with jump process and adaptive sampling | Relevant to price-path simulation; reported high returns require independent replication and strict OOS scrutiny |
| QuantInsti (2025) YouTube session | Educational video | Demonstrates return bootstrapping and thousands of simulated paths for drawdown/Sharpe analysis | Methodology reference, not proof of profitability |
| Surbhi Verma (2026) YouTube | Educational video | Explains purged/embargoed CV, CPCV and DSR | Supplemental methodology reference, not primary evidence |

## Synthesis
1. The strongest literature support is for Monte Carlo/bootstrap as an uncertainty, robustness and risk-analysis tool, not as a guaranteed alpha generator.
2. IID resampling is insufficient when serial dependence, volatility clustering or regime structure matters; stationary/block bootstrap methods are therefore primary candidates.
3. When many strategies/parameters are explored, naive p-values and Sharpe ratios are biased by selection. White Reality Check, SPA, DSR and PBO/CSCV address different aspects of this problem and should be treated as complementary rather than interchangeable.
4. Short-horizon Indian trading research has demonstrated that transaction costs and execution prices can materially change conclusions. This makes a realistic cost engine a first-class part of the study.
5. Price-path Monte Carlo based on a parametric stochastic process is a different research question from resampling observed trades/returns. The protocol will keep these uses separate to avoid conflating model-risk evidence with empirical resampling evidence.
6. Recent practitioner material emphasizes robustness testing, but educational content is lower evidence tier than peer-reviewed statistical and market-microstructure studies.

## Proposed evidence hierarchy
Tier 1: peer-reviewed statistical/finance literature and official exchange/regulatory documentation.
Tier 2: working papers/preprints with transparent methods and data.
Tier 3: technical implementations and repositories used only to cross-check methods.
Tier 4: educational videos/blogs used for implementation ideas, not as proof of efficacy.

## Gaps this project will address
- A unified, cost-aware comparison of Monte Carlo uses across scalping, intraday, BTST and swing on Indian equities.
- Dependence-aware resampling and multiple-testing controls in the same experimental framework.
- Explicit sensitivity to Paytm Money execution charges and slippage assumptions.
- Cross-stock and cross-regime replication rather than single-strategy examples.

## Key references
- Politis, D. N., & Romano, J. P. (1994). The Stationary Bootstrap. Journal of the American Statistical Association, 89(428), 1303–1313. DOI: 10.1080/01621459.1994.10476870
- Sullivan, R., Timmermann, A., & White, H. (1999/2002). Data-Snooping, Technical Trading Rule Performance, and the Bootstrap. Journal of Finance, 54, 1647–1691. DOI: 10.1111/0022-1082.00163
- Hansen, P. R. (2005). A Test for Superior Predictive Ability. Journal of Business & Economic Statistics, 23(4), 365–380. DOI: 10.1198/073500105000000063
- Bailey, D. H., & López de Prado, M. (2014). The Deflated Sharpe Ratio. Journal of Portfolio Management, 40(5), 94–107. DOI: 10.3905/jpm.2014.40.5.094
- Bailey, D. H., Borwein, J., López de Prado, M., & Zhu, Q. J. (2017). The Probability of Backtest Overfitting. Journal of Computational Finance. DOI: 10.21314/JCF.2016.322
- Patnaik, T. C., & Thomas, S. (2004). Profitability of Trading Strategies on High-Frequency Data, with Trading Costs. SSRN 568363.
- Hsu, P.-H., & Kuan, C.-M. (2005). Re-Examining the Profitability of Technical Analysis with White's Reality Check and Hansen's SPA Test.
- Park, C.-H., & Irwin, S. H. (2010). A Reality Check on Technical Trading Rule Profits in the U.S. Futures Markets. Journal of Futures Markets, 30(7), 633–659. DOI: 10.1002/fut.20435
