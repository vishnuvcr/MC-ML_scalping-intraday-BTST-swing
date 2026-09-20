# Phase 10 Literature Addendum — Global Lead/Lag and Market Integration

## Why global lead/lag is a legitimate hypothesis

Recent work on India and global equity markets documents time-varying integration, spillovers and contagion, including regime-dependent relationships between Indian and major global indices. This motivates testing lagged global information as a conditioning variable rather than assuming independence.

The literature also contains direct evidence that lead–lag predictability can arise when assets trade at different times or on different venues. Studies using cross-listed index futures and high-frequency order-book data show that information can propagate sequentially across markets, while transaction costs, latency and execution risk can erase apparent arbitrage.

## Relevance to this project

Phase 10 does not assume that observed correlation equals exploitable inefficiency. It separates statistical lead/lag association, incremental prediction of the frozen Indian signal, economic profitability after costs, and robustness across symbols/time.

The global filter is therefore tested as an information/timing condition on an existing Indian strategy, not as a free-standing signal-mining exercise.

## Evidence sources

- Global/India regime-dependent integration and contagion: 2026 empirical research covering long-run integration, Granger causality and dynamic conditional correlation.
- Lead–lag arbitrage under market frictions: recent work on Asian index futures and high-frequency cross-market delay.
- High-frequency lead–lag arbitrage with execution costs: evidence from DAX-related markets showing that predictability and profitability are distinct questions.

The repository records exact source links in the final manuscript and provenance file.

## Key current sources

1. Bhardwaj, Miklošević & Gambhir (2026), “Regime-Dependent Integration, Connectedness and Contagion Between India and Global Equity Markets,” International Journal of Financial Studies 14(8), 210, DOI 10.3390/ijfs14080210. The study uses daily India/global data through 2025 and reports regime-dependent integration, Granger causality and crisis-period connectedness. https://doi.org/10.3390/ijfs14080210

2. Krishnan V.K., Thomas & Kumar (2026), “Trading on delay: Information frictions and cross-market arbitrage in index futures,” Finance Research Letters 98, 109842, DOI 10.1016/j.frl.2026.109842. The paper studies information transmission in cross-listed Asian index futures and reports different convergence speeds, including an India transmission window measured in minutes. https://doi.org/10.1016/j.frl.2026.109842

3. Poutré, Dionne & Yergeau (2024), “The profitability of lead–lag arbitrage at high frequency,” International Journal of Forecasting 40(3), 1002–1021, DOI 10.1016/j.ijforecast.2023.09.001. The study uses DAX 30 cross-listed limit-order-book data and explicitly evaluates costs, latency and execution risk. https://doi.org/10.1016/j.ijforecast.2023.09.001
## Fresh literature checks — 20 Sep 2026

- Bhardwaj, Miklošević & Gambhir (2026), *Regime-Dependent Integration, Connectedness and Contagion Between India and Global Equity Markets*, International Journal of Financial Studies 14(8), 210. Daily data 2002–2025; the paper reports regime-dependent connectedness and directional relationships between India and major global markets. DOI: 10.3390/ijfs14080210.
- Krishnan V.K., Thomas & Kumar (2026), *Trading on delay: Information frictions and cross-market arbitrage in index futures*, Finance Research Letters 98, 109842. Using transaction-level data, the paper reports that the convergence window for informed trading in Indian cross-listed index futures can extend to about 15 minutes. DOI: 10.1016/j.frl.2026.109842.
- Poutré, Dionne & Yergeau (2024), *The profitability of lead–lag arbitrage at high frequency*, International Journal of Forecasting 40(3), 1002–1021. The study uses level-1 order-book data and explicitly incorporates trading costs, latency and execution risk. DOI: 10.1016/j.ijforecast.2023.09.001.
- Iwanaga & Sakemoto (2026), *Does overnight return predict the first half-hour return for U.S. market indices?*, North American Journal of Economics and Finance 86, 102707. The paper reports predictive content from overnight returns into the first half-hour of the cash session, with regime/time-period dependence. DOI: 10.1016/j.najef.2026.102707.
- Bahcivan, Dam & Gonenc (2026), *Dark side of the day: Overnight price jumps and short-term return predictability*, Journal of Behavioral and Experimental Finance 51, 101220. The study finds short-term predictability after overnight jumps but shows that the apparent effect can reverse as the holding period changes, reinforcing the need for horizon-specific validation. DOI: 10.1016/j.jbef.2026.101220.