# Phase 9 Literature Addendum

Phase 9 variables are grounded in prior Indian-market evidence rather than chosen solely from the current sample.

1. Intraday liquidity in NSE equities exhibits strong time-of-day structure, with volume/spread measures tending to show U-shaped patterns. This supports controlling for entry-time bucket and liquidity rather than treating all intraday signals as exchange-time homogeneous.
2. High-frequency Indian-market research finds that time-varying illiquidity interacts asymmetrically with returns across market conditions and volatility. This motivates liquidity × volatility interaction terms.
3. Recent Indian-equity regime-adaptive work explicitly uses market-regime classification, but its short stock sample and lack of walk-forward validation make it a methodological precedent rather than evidence of general profitability.
4. Research on cross-listed Indian securities shows order-flow competition across trading venues and suggests that market fragmentation can affect information transmission. This motivates a lagged NSE/BSE basis variable, while avoiding any claim that a same-day price gap is directly tradable.
5. Contemporary reporting around the August 2026 NSE closing-auction change describes short-lived NSE/BSE price divergences in some large-cap names. This is useful context for a date-bounded cross-market test, not proof of a persistent arbitrage opportunity.

Phase 9 therefore tests liquidity, volatility, regime and cross-market basis jointly with the frozen MC strategy instead of adding ad-hoc technical indicators.
