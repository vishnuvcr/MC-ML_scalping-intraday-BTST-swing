# Phase 9 Literature Addendum — Why These Factors Are Tested

## Liquidity and time-of-day

Krishnan and Mishra's empirical study of NIFTY-stock trade/quote data found that most NSE volume- and spread-related liquidity measures display U-shaped intraday patterns. That supports conditioning intraday results on time-of-day and liquidity instead of assuming a stationary trading-cost environment. citeturn354050search3turn354050search7

## Regime dependence

Recent Indian-market work explicitly studies regime-dependent price formation. A 2026 Nifty-500 study reports volatility clustering and stronger herding in high-volatility/down-market states using Markov-regime-switching and related models. This supports testing whether the MC/EMA result changes with volatility, breadth, and cross-sectional dispersion rather than treating the sample as one homogeneous regime. citeturn354050search0

A separate 2026 Indian-equity paper reports that the relative effectiveness of momentum and reversal varies across calm and crash states and uses an HMM with filtered probabilities to avoid look-ahead. We use this as methodological motivation for lagged regime variables, not as evidence that the present EMA/MC rule should work. citeturn354050search5turn354050search6

Historical Indian evidence also finds time-varying return comovement across economic regimes, including higher probability of extreme comovement in contraction regimes. citeturn354050search1

## Stock selection and lead-lag structure

Indian research has documented lead/lag differences associated with market capitalization and thin trading: large-cap portfolios can lead smaller-cap portfolios, with thin trading contributing to the observed lag. This motivates explicit liquidity, traded-value, volatility, and market-beta controls rather than assuming every NSE constituent is equally suitable for the same signal. citeturn215514search1

## Cross-market and price discovery

Indian price-discovery research documents lead-lag relationships between spot and futures markets and shows that information transmission can depend on trading costs, trading hours, information access and market structure. citeturn215514search3turn215514search8

More general cross-listing research shows how relative market contributions to price discovery can be assessed with information-share or error-correction methods. The present project uses a deliberately simpler, lagged NSE/BSE basis test because the available public data do not support a full tick-level Hasbrouck/VECM analysis across the entire universe. citeturn215514search5

## Current data sources

The broad minute dataset used for the new intraday test reports 720,421,072 rows, 2,500+ NSE stocks/indices, 1-minute data from 2022-01-03 through 2026-01-21, and states 99.4% coverage of active/suspended NSE equities and indices. Its dataset card shows an MIT license. citeturn460910search0turn460910search6

The TejHQ dataset reports end-of-day data for every NSE and BSE listed equity, sourced from official exchange bhavcopy, with about 2,300 NSE instruments/day from 2010-01-04 onward and BSE coverage beginning 2024-07-08. It also provides a survivorship-bias-free liquidity universe. citeturn460910search2

## Interpretation rule

These literature findings justify the variables being tested. They do **not** justify a favorable trading conclusion in advance. The present result must be determined by the frozen out-of-sample experiments and cost model.
