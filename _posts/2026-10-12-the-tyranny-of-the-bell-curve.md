---
layout: post
title: "The Tyranny of the Bell Curve"
summary: "Why finance still measures risk with standard deviation, what that misses, and how a proposed alternative measure performs against it."
date: 2026-10-12
# Publish on Monday Oct 12, 2026: change the next line from false to true.
published: false
author: Diego Rodriguez
image: /assets/brand/banner.png
description: >-
  Why finance still measures risk with standard deviation, what that misses,
  and how a proposed alternative measure (DRT) performs against it.
downloads:
  - label: Article PDF
    href: /downloads/article.pdf
  - label: results.csv
    href: /downloads/results.csv
    note: "(summary results, long format)"
  - label: Data archive (data.zip)
    href: /downloads/data.zip
  - label: Results archive (results.zip)
    href: /downloads/results.zip
  - label: analysis.py
    href: /downloads/analysis.py
  - label: download_data.py
    href: /downloads/download_data.py
  - label: make_formula.py
    href: /downloads/make_formula.py
  - label: requirements.txt
    href: /downloads/requirements.txt
  - label: Reproducibility notes
    href: /downloads/REPRODUCE.md
---

# The Tyranny of the Bell Curve

### Why finance still measures risk with standard deviation, what that misses, and how a proposed alternative measure performs against it

*By Diego Rodriguez · October 2026 · All data, code and results are reproducible (see the end of the article)*

## 1. A 17-sigma day

On October 19, 1987, the S&P 500 fell 20.5% in a single session. Measured against the index's own history (24,803 daily returns from 1928 to September 2026), that drop was a 17.2 standard-deviation event. If daily returns really followed the bell curve that sits under most of modern finance, the probability of a day that bad would be about 1.6 × 10⁻⁶⁶, or roughly one such day every 10⁶³ years, in a universe that is about 1.4 × 10¹⁰ years old.

There are only two ways to read that number. Either markets were extraordinarily unlucky that day, or the model that produced the probability is wrong. Most people in finance would accept the second reading, and yet standard deviation (volatility, sigma, σ) remains the default measure of risk on fund factsheets, broker risk reports, robo-advisor questionnaires and first-year finance textbooks. It is the denominator of the Sharpe ratio, the input to mean-variance optimizers, and the risk axis on every efficient-frontier chart.

In this article, I want to work through three questions. The first is how standard deviation became the default, and why the reasons were (and partly still are) good ones. The second is where it breaks when confronted with real market data: fat tails, skew, the floor at a 100% loss, and volatility clustering. The third is whether a better measure is available, which the article examines by proposing an alternative (DRT) and testing it against standard deviation, downside deviation and CVaR, with the results reported in full, including the tests the proposed measure lost. As you will see, the bell curve fails one of those tests badly, but on the others the answer is more nuanced than a simple replacement of the old with the new.

## 2. How standard deviation became "risk"

### 1952: two papers, one winner

Modern portfolio theory has an unusual origin, since two people published the core idea in the same year. Harry Markowitz's "Portfolio Selection" (*Journal of Finance*, March 1952) proposed that investors should care about both the expected return of a portfolio and its variance, and showed that the variance of a portfolio depends on the covariances between the assets in it. That insight, that a portfolio's risk is not the sum of the risks of its parts, is the mathematics of diversification, and it earned Markowitz the Nobel Prize in 1990.

A few months later, A. D. Roy's "Safety First and the Holding of Assets" (*Econometrica*, July 1952) came at the problem from the opposite end. Roy argued that investors mainly want to avoid disaster, and that they should therefore minimize the probability that returns fall below some catastrophic level *d*. Since that probability cannot be computed without knowing the full distribution of returns, Roy bounded it with Chebyshev's inequality, which leads to a rule of maximizing (μ − d)/σ, a close ancestor of the Sharpe ratio.

There is an irony here that is worth noting. A theory built around avoiding downside disaster ended up expressed in standard deviation, because σ was the only summary of the distribution that could be worked with at the time. Markowitz later wrote that Roy could claim an equal share of the credit for portfolio theory (Markowitz, 1999).

### 1958–1966: the edifice

James Tobin (1958) showed that if investors choose portfolios using only mean and variance, every efficient portfolio is a combination of a single risky portfolio and cash, a result now known as the separation theorem. Tobin was explicit about the conditions under which this choice is fully rational: utility has to be quadratic, or returns have to follow a two-parameter distribution such as the normal.

William Sharpe (1964), John Lintner (1965) and Jan Mossin (1966) built on this foundation to develop the Capital Asset Pricing Model (CAPM), in which the only risk that is priced is covariance with the market (beta), and the entire framework rests on investors who care only about mean and variance. Sharpe (1966) then introduced the "reward-to-variability" ratio for evaluating mutual funds, excess return divided by standard deviation, which later became known as the Sharpe ratio (Sharpe, 1994) and is probably the most quoted number in investing.

### The forgotten chapter: Markowitz's semivariance

Markowitz was aware that variance had problems. In his 1959 book, *Portfolio Selection: Efficient Diversification of Investments*, he devoted a chapter to semivariance, which counts only returns below a target, and argued that it could be the better measure, because investors dislike losses rather than upside surprises. He nevertheless built the framework on variance, mainly for practical reasons: it was cheaper to compute, more convenient to work with, and more familiar.

The cost of computation was a real constraint in that era. In the 1950s and 1960s, solving a full covariance problem for a few hundred securities was expensive, and Sharpe's single-index model (1963) was designed largely to reduce the number of estimates and calculations that portfolio analysis required. Semivariance, whose "co-semivariance" matrix depends on the portfolio weights themselves, was considerably harder to work with.

### Why it stuck

Standard deviation won for reasons that had little to do with how well it described the experience of losing money. The first is tractability: portfolio variance is a quadratic form, w′Σw, which is easy to optimize, aggregates neatly, and yields closed-form answers. The second is theory, since CAPM, Black and Scholes (1973, which assumes lognormal prices with constant volatility) and most asset-pricing models are written in σ, and changing the risk measure means rebuilding the framework.

The third reason is standardization and regulation. J.P. Morgan's RiskMetrics (1994 and 1996) made volatility-based Value-at-Risk an industry standard, the Basel Committee's 1996 market-risk rules based capital requirements on VaR, and European UCITS funds reported a risk score (SRRI) based on volatility bands. The fourth is software and education: every spreadsheet has a STDEV() function, and every CFA candidate learns the efficient frontier.

The fifth reason is that standard deviation is not useless. Levy and Markowitz (1979) showed that mean-variance choices come very close to full expected-utility maximization for many realistic utility functions, and as the results later in this article show, σ remains a reasonable tool for ranking assets by risk. Put simply, standard deviation became the default because it was the most convenient measure that was good enough most of the time, and its weakness is concentrated in the periods when risk measurement matters most.

## 3. What you implicitly assume when you use σ as risk

Using standard deviation as the measure of risk quietly brings with it a set of assumptions, summarized in the table below, along with what the data in the next section says about each.

| Assumption | What it means | Reality check (data below) |
|:-|:-|:-|
| Normal (or elliptical) returns, or quadratic utility | Mean and σ describe the whole distribution (Tobin, 1958; Chamberlain, 1983) | All 49 assets in the analysis reject normality |
| Symmetry | A +3% surprise is as risky as a 3% loss | Investors do not experience it that way, and upside is penalized |
| Only two moments matter | Skewness and kurtosis are irrelevant | Investors pay for positive skew and fear crash risk (Kraus & Litzenberger, 1976; Harvey & Siddique, 2000) |
| Finite, stable variance | σ exists and is a fixed property of the asset | Mandelbrot (1963) questioned even finiteness, and volatility moves around a great deal |
| Stationarity | The past window represents the future | SPY's 1-month volatility has ranged from 3.4% to 94.5% annualized |
| i.i.d. returns | Today's return says nothing about tomorrow's risk | Volatility clusters strongly |
| Path does not matter | Only the distribution of returns counts, not their order | Drawdowns, margin calls and redemptions depend on the path |

Quadratic utility deserves particular attention, because its implications are strange. It implies that beyond some level of wealth, investors prefer less money to more, and that wealthier investors hold fewer risky assets (increasing absolute risk aversion). Nobody defends it as a description of how people behave, and its role in the theory is to make the mathematics work.

## 4. Where it breaks: the evidence

The data used throughout is daily adjusted closing prices from Yahoo Finance (via `yfinance`) for 49 series, each over its longest available history through September 30, 2026. The series include the S&P 500 index (from 1928), SPY, QQQ, IWM, EFA, EEM, TLT, IEF, LQD, HYG, GLD, VNQ and DBC, the nine original SPDR sector ETFs, 26 large-cap stocks (AAPL, MSFT, AMZN, JPM, XOM, JNJ, KO, GE, IBM and others, several going back to 1962), and Bitcoin (from 2014).

### 4.1 Fat tails: the bell curve is a poor map of the tails

![SPY daily returns vs normal](/assets/charts/01_spy_hist_vs_normal.png)

SPY's daily returns (8,474 days since 1993) have an excess kurtosis of 11.9, where a normal distribution has 0. The left panel of the chart shows the classic pattern of too many quiet days, too few medium-sized days, and far too many extreme days, and the log-scale panel on the right makes the tails visible. Under the normal curve with the same mean and standard deviation, SPY should have had 0.06 days worse than a 5% loss in 33 years, whereas it actually had 22 such days, along with 22 days of gains above 5%.

Formal tests are unambiguous. The Jarque-Bera test rejects normality for 49 out of 49 assets at daily frequency (p < 0.01), with a test statistic of 308,630 for the S&P 500 since 1928. Median excess kurtosis across the 49 assets is 10.8 at daily frequency and 1.6 at monthly frequency, which tells you that tails get thinner as returns are aggregated over longer periods, but they do not disappear: 45 of 49 assets still reject normality on monthly returns, with IEF, GLD, XLV and JNJ the only exceptions.

![QQ plots](/assets/charts/02_qq_plots.png)

The QQ plots tell the same story visually. If returns were normal, the points would lie on the red line, and the way the ends curl away from it is the signature of fat tails.

To see what this means in practice, consider the count of large down days in the S&P 500 since 1928, compared with what a normal distribution with the same mean and standard deviation would predict.

![Tail counts](/assets/charts/03_tail_counts.png)

| Daily move worse than | Observed | Expected if normal |
|:-|:-|:-|
| −3σ | 221 | 33 |
| −4σ | 100 | 0.79 |
| −5σ | 50 | 0.0071 |
| −6σ | 28 | 0.000024 |
| −7σ | 16 | 0.00000003 |

Under normality, a day worse than −5σ should occur about once every 13,800 years, and the S&P 500 has had 50 of them in 98 years, along with 53 days of +5σ or more. This is the context for a remark by Goldman Sachs CFO David Viniar in August 2007, explaining heavy losses at the firm's quantitative hedge funds: "We were seeing things that were 25-standard deviation moves, several days in a row" (*Financial Times*, August 13, 2007). Dowd et al. (2008) calculate that under a normal distribution, a single 25σ day should occur about once every 10¹³⁵ years, which makes a model failure a far more plausible explanation than bad luck.

The academic recognition of this problem goes back six decades. Benoit Mandelbrot (1963) showed that changes in cotton prices were far too fat-tailed to be normal and proposed "stable Paretian" distributions, some of which have infinite variance, so that the sample standard deviation never settles down. Eugene Fama's (1965) doctoral work on the Dow 30 stocks confirmed the excess kurtosis. Later research generally settled on distributions that are fat-tailed but have finite variance (Cont, 2001), but the central finding held up: the bell curve gets the tails wrong.

| Event | S&P 500 daily return | σ-move (full-sample σ) | σ-move (trailing 1-yr σ) |
|:-|:-|:-|:-|
| Black Monday, 1987-10-19 | −20.5% | −17.2 | −19.4 |
| 1929-10-28 | −12.9% | −10.9 | −9.2 |
| COVID, 2020-03-16 | −12.0% | −10.1 | −8.3 |
| GFC, 2008-10-15 | −9.0% | −7.6 | −4.8 |
| GFC rally, 2008-10-13 | +11.6% | +9.7 | +6.7 |
| Tariff shock, 2025-04-04 | −6.0% | −5.0 | −6.4 |
| Tariff-pause rally, 2025-04-09 | +9.5% | +8.0 | +9.5 |

The rallies in this table are as revealing as the crashes. Of the 20 best days in S&P 500 history, 13 came within 30 days of one of the 20 worst days, which indicates that extreme days arrive in clusters, in both directions, a pattern that the next section examines in more detail.

### 4.2 Volatility clustering: risk is not a constant

![Volatility clustering](/assets/charts/04_vol_clustering.png)

SPY's 21-day realized volatility has ranged from 3.4% (October 2017) to 94.5% (October 2008), annualized, with a median of 13.3%. The single full-sample number of 18.6% describes almost no actual month in that history.

Returns themselves are nearly unpredictable (SPY's lag-1 autocorrelation is −0.08), but the size of returns is highly persistent. The autocorrelation of absolute returns is 0.28 at a lag of one day and still 0.09 at a lag of 100 days, and all of the first 100 lags are significantly positive. A Ljung-Box test on absolute returns (10 lags) produces a statistic of 7,662, and Engle's ARCH-LM test produces 1,813, both with p-values that are effectively zero.

This is the behavior that Robert Engle's ARCH model (1982) and Tim Bollerslev's GARCH model (1986) were built to capture, in which today's variance depends on yesterday's shocks. A GARCH(1,1) model with Student-t errors fitted to SPY gives α = 0.116 and β = 0.879, for a persistence (α + β) of 0.995, which implies that a volatility shock has a half-life of about 150 trading days. The fitted Student-t degrees of freedom are ν = 6.0, so even after accounting for clustering, the remaining shocks are fat-tailed.

The asymmetric GJR-GARCH model (Glosten, Jagannathan & Runkle, 1993) is more revealing still. The symmetric shock coefficient α falls to approximately 0, while the coefficient on down moves is γ = 0.20 (t-statistic 10.4), meaning that in SPY, essentially all of the response of volatility to shocks comes from down days. Rallies barely raise future volatility while selloffs do, a pattern known as the leverage effect (Black, 1976), which directly contradicts the symmetry assumption built into σ, and the asymmetric model is strongly preferred by the data (the BIC improves by about 260).

### 4.3 The 100% floor and skew

A stock cannot lose more than 100% of its value, but it can gain 125%, 300%, or, as Amazon did in 1998, 966%. Over longer horizons, that floor makes returns strongly right-skewed, a shape that a symmetric measure like σ cannot represent.

![The 100% floor](/assets/charts/05_annual_stock_returns.png)

Across 1,364 calendar-year returns of the 26 large-cap stocks in the sample, skewness is +7.0 (compared with 0 for a normal distribution), the mean is 19.8%, the median is 13.5%, and σ is 48%. In 47 stock-years the return exceeded 100%, while only 26 stock-years lost more than 50%, with the worst being a loss of 82.8% (NVDA, 2002). A normal distribution fitted to these returns assigns a 0.63% probability to losing more than 100% in a year, about one stock-year in 160, which is a mathematical impossibility, and "mean minus two sigmas" works out to a loss of 76%.

Bitcoin is the extreme case, with returns of +1,369% in 2017, −74% in 2018, +303% in 2020 and −64% in 2022, a pattern that no single σ can describe in a useful way. The floor also helps explain a well-known result from Bessembinder (2018), who found that most individual U.S. stocks underperform Treasury bills over their lifetimes, while a small minority of extreme winners account for the market's entire net wealth creation. That is what positive skew looks like when aggregated across an entire market.

### 4.4 σ penalizes the upside, and the obvious fix barely helps

Since standard deviation is symmetric, an asset with large upside surprises looks riskier than it is, and the textbook response is the Sortino ratio, which counts only downside deviation. The question worth asking is whether that substitution actually changes conclusions in practice.

Over the last 10 years, for the 48 assets in the panel, the rank correlation between rankings by Sharpe ratio and rankings by Sortino ratio was 0.998, and no asset moved more than three places. The reason is that the ratio of daily downside deviation to standard deviation sits between 0.65 and 0.73 for every asset, close to the 0.71 that a symmetric distribution would produce. At daily frequency, then, the asymmetry problem is real, but swapping σ for downside deviation barely changes anything, because the larger errors lie in the tails and in the variation of risk over time rather than in the split between upside and downside.

### 4.5 The tail events σ did not anticipate

The history of financial crises provides a series of examples. In 1987, portfolio insurance programs built on assumptions of continuous trading and stable volatility sold into a falling market and made the crash worse. In 1998, Long-Term Capital Management, whose partners included Nobel laureates Robert Merton and Myron Scholes, lost about $4.6 billion in less than four months, and the Federal Reserve Bank of New York facilitated a $3.6 billion private recapitalization by 14 banks and securities firms, with no Fed money involved (Lowenstein, 2000; Federal Reserve History, n.d.). Correlations that had been stable in calm periods all moved toward one at the same time.

In 2008, normal VaR models calibrated on the calm period of 2004 to 2006 badly understated risk, and SPY's 99% one-day VaR from a one-year normal model was breached far more often than 1% of the time (Figure 8 below). In 2020, the S&P 500 fell 12% on March 16, an 8σ to 10σ event measured against trailing volatility, only a few weeks after volatility had been near historical lows.

## 5. The toolbox that already exists

None of this is new to quantitative analysts, and a substantial set of alternative measures already exists, each with its own trade-offs.

| Measure | Idea | Strength | Weakness |
|:-|:-|:-|:-|
| Semivariance / downside deviation (Markowitz, 1959) | Count only returns below a target | Matches loss aversion | Discards half the data, and is still a second-moment measure |
| Sortino ratio (Sortino & van der Meer, 1991) | Excess return ÷ downside deviation | Does not punish upside | Rankings barely differ from Sharpe (see 4.4) |
| Value-at-Risk (RiskMetrics, 1996; Basel, 1996) | Loss not exceeded with X% confidence | Intuitive, regulatory standard | Says nothing about losses beyond the threshold, and is not subadditive, so it can penalize diversification (Artzner et al., 1999) |
| CVaR / Expected Shortfall (Rockafellar & Uryasev, 2000; Acerbi & Tasche, 2002) | Average loss in the worst X% | Coherent, tail-focused, optimizable by linear programming | Needs a lot of data, and is noisy |
| Basel FRTB (BCBS, 2016/2019) | Replaced 99% VaR with 97.5% Expected Shortfall for bank market-risk capital | Regulators acknowledging VaR's flaw | Implementation repeatedly delayed |
| Maximum drawdown / Calmar ratio (Young, 1991) | Worst peak-to-trough loss | Path-dependent, matches investor pain | A single observation that depends on sample length |
| Ulcer Index (Martin, 1987; Martin & McCann, 1989) | Root mean square of drawdowns | Captures both depth and duration | Same issues as drawdown, and less widely known |
| Omega ratio (Keating & Shadwick, 2002) | Probability-weighted gains ÷ losses relative to a threshold | Uses the entire distribution | Hard to interpret and to optimize |
| GARCH / EWMA conditional volatility (Engle, 1982; Bollerslev, 1986; RiskMetrics) | Volatility that changes over time | Captures clustering | Still symmetric and Gaussian unless extended |
| Cornish-Fisher "modified VaR" (Zangari, 1996; Favre & Galeano, 2002) | Adjust the normal quantile for skew and kurtosis | Simple higher-moment correction | Sample skew and kurtosis are extremely noisy |
| Extreme Value Theory (Embrechts et al., 1997; McNeil & Frey, 2000) | Model only the tail (for example, with a generalized Pareto distribution) | Built for extremes | Data-hungry, and sensitive to the choice of threshold |
| Tail ratio | 95th percentile ÷ abs(5th percentile) | Quick check on skew | Crude |

The common pattern across this toolbox is that each measure fixes one of σ's assumptions (symmetry, tails, or time variation) and usually leaves the others in place.

## 6. A proposed alternative: Downside Regime-Tail risk (DRT)

The objective of the proposed measure is a single number that addresses the three failures that matter most for actual losses, while remaining simple enough to compute in a spreadsheet. The first is asymmetry, since only downside moves should drive the risk estimate, as the GJR result above suggests. The second is regime dependence, since the measure should reflect current risk rather than a one-year average. The third is fat tails, since the translation from a measure of scale to an estimate of loss should come from the asset's own tail rather than from the bell curve.

![DRT formula](/assets/charts/00_drt_formula.png)

The measure is built in four steps. The first step computes the downside regime scale σ↓, an exponentially weighted average of squared returns on down days only (the factor of 2 makes it equal to ordinary variance for a symmetric, zero-mean distribution). With λ = 0.97, the half-life is about 23 trading days, so the scale reacts within days to a selloff and does not respond to rallies.

The second step standardizes each day's return by dividing it by the previous day's downside scale, which removes the regime and expresses each shock relative to the conditions in which it occurred. The third step computes the tail multiplier κ as the average of the worst 2.5% of these standardized shocks over the last 3 years (756 trading days). This captures the asset's own empirical tail, measured in units of current risk. For a normal distribution κ would be 2.34, and every asset in the analysis is currently above that level, with values of 2.57 for TLT, 3.14 for SPY, 3.58 for GLD and 4.11 for IBM.

The fourth step multiplies the two, DRT = σ↓ × κ, and the result is a one-day 97.5% Expected Shortfall forecast, the same confidence level used in Basel's FRTB. That gives the number a direct interpretation: on a bad day (one in 40), the expected loss is about DRT percent.

![Tail multiplier by asset](/assets/charts/11_kappa_by_asset.png)

The design has three features that are worth spelling out. First, it contains σ as a special case: if returns were normal and i.i.d., DRT would equal 2.34σ exactly, so comparing an asset's κ with 2.34 shows directly how much the bell curve understates its tail. For SPY today, κ/2.34 = 1.34, which means that a normal-based Expected Shortfall understates SPY's tail by about a third, even after adjusting for the current volatility regime. Second, it requires no distributional assumption and no maximum-likelihood fitting, since it consists of two exponentially weighted averages and a sort. Third, it separates risk into two readable components, how turbulent conditions are now (σ↓) and how severe this asset's turbulence tends to be (κ).

The lineage of the measure should be acknowledged. DRT is a downside-only variant of filtered historical simulation (Barone-Adesi et al., 1999; Hull & White, 1998), which combines GARCH-type scaling with empirical residuals, and what is new is the downside-only regime scale and the use of the result as a general-purpose risk score in place of σ, rather than solely as a bank VaR engine. To separate the contribution of each component, the analysis also tests two ablations: EWMA, a symmetric RiskMetrics volatility (λ = 0.94) that captures the regime alone, and FHS, symmetric EWMA multiplied by the empirical tail multiplier, which captures regime and tails without asymmetry.

All parameters were fixed before any results were examined: the RiskMetrics λ = 0.94 for the symmetric version, a slower λ = 0.97 for the downside-only version (because it uses only about half of the days), the Basel 97.5% level, and a 3-year window. Nothing was optimized on the test data.

![SPY DRT vs SD](/assets/charts/10_spy_drt_vs_sd.png)

The chart shows the practical difference for SPY. Trailing one-year σ (red) moves slowly: it was still near its lows in early 2020, and it remained elevated for a full year after both 2008 and 2020, well after the danger had passed. DRT (navy, rescaled to σ units for comparison) moves with the actual level of danger.

## 7. Does it actually work? The statistical tests

"Better" has to be defined before testing, and the analysis uses three questions, each paired with a test of statistical significance. The first concerns prediction: does today's measure predict future losses out of sample, specifically next-3-month tail loss, next-3-month and next-12-month maximum drawdown, and the next month's worst day? The second concerns calibration: when the measure is used as a VaR or ES forecast, is it right as often as it claims, as judged by the Kupiec, Christoffersen and ES ratio tests? The third concerns portfolio construction: do minimum-risk portfolios built with the measure perform better out of sample?

The competing measures are computed at every month-end using only data available at the time. They are SD (trailing 252-day σ), DD (252-day downside deviation), CVaR (252-day historical 95% Expected Shortfall), mVaR (Cornish-Fisher modified VaR), EWMA, FHS and DRT.

### 7a. Predicting future losses

The prediction tests use 48 assets (the S&P 500 index is excluded to avoid duplicating SPY) and 21,648 asset-months from January 1965 to June 2026, with targets always measured strictly in the future. For out-of-sample R², each month the log of the target is regressed on the log of the measure using only target windows that had already ended, the next month is forecast, and the forecast is scored against a historical-mean benchmark, with 10 years of history required before the first forecast. Forecast errors are compared with Diebold-Mariano tests (using Newey-West standard errors), rank correlations are computed both within each asset over time and across assets each month, and confidence intervals come from a block bootstrap (12-month blocks, 500 draws).

![Prediction R2](/assets/charts/07_prediction_r2.png)

The table reports out-of-sample R² for predicting the log of future risk.

| Measure | Next-3m tail loss (ES 5%) | Next-3m max drawdown | Next-12m max drawdown | Next-month worst day |
|:-|:-|:-|:-|:-|
| SD (σ, 1 yr) | 0.476 | 0.306 | 0.247 | 0.389 |
| Downside deviation | 0.455 | 0.292 | 0.232 | 0.376 |
| CVaR 95% (1 yr) | 0.446 | 0.281 | 0.226 | 0.365 |
| Cornish-Fisher mVaR | 0.295 | 0.196 | 0.145 | 0.253 |
| EWMA vol (ablation) | **0.533** | **0.338** | **0.281** | **0.447** |
| FHS (ablation) | 0.507 | 0.313 | 0.269 | 0.421 |
| DRT (proposed) | 0.487 | 0.302 | 0.261 | 0.410 |

Three lessons emerge from these numbers, and they do not all favor the proposed measure. The first is that DRT outperforms the textbook alternatives to σ. Against downside deviation and CVaR, DRT has a higher out-of-sample R² on every target, and the Diebold-Mariano advantage is significant for next-month worst day (p = 0.003 against CVaR and p = 0.025 against downside deviation) and marginal for 3-month tail loss (p = 0.09 against CVaR). The popular fixes for σ actually predict worse than σ itself, because they use less data (downside deviation) or only the noisiest data (CVaR, and Cornish-Fisher in particular).

The second lesson is that DRT and plain σ are statistically tied on pooled prediction. DRT is slightly ahead on three of the four targets (for example, an R² of 0.261 against 0.247 for 12-month drawdown), but the Diebold-Mariano tests are not significant (p values between 0.27 and 0.87), and the bootstrap interval for the difference in rank correlation includes zero (for 3-month tail loss, +0.005 with a 95% confidence interval of [−0.032, +0.044]).

The third lesson is that the best predictor was the simplest regime model. Plain EWMA volatility beat every other measure, including DRT, by a significant margin on the short horizons (DM t = −5.1 for 3-month tail loss and −4.3 for 3-month drawdown, p < 0.001), although the difference at 12 months is not significant. Since the tail multiplier κ is estimated from only about 19 tail observations, its noise cost more, on average, than its information was worth for ranking future risk.

The difference between the measures becomes clearer when you separate prediction over time from prediction across assets.

| Avg. Spearman ρ with next-3m tail loss | Within asset, over time | Across assets, each month |
|:-|:-|:-|
| SD | 0.445 | **0.696** |
| Downside deviation | 0.428 | 0.672 |
| CVaR | 0.426 | 0.667 |
| EWMA | **0.522** | 0.665 |
| DRT | 0.493 | 0.630 |

![Rank correlation](/assets/charts/06_prediction_rank_corr.png)

This split is the most useful finding in the study. When the question is timing (is this asset more dangerous than usual right now?), DRT beats σ for 69% of assets on 3-month tail loss and for 77% of assets on 12-month maximum drawdown (Wilcoxon signed-rank p < 0.001 for both), and for 12-month drawdown the within-asset correlation rises from 0.196 for σ to 0.258 for DRT, about 30% more predictive power.

When the question is comparison across assets (is AAPL riskier than KO?), plain one-year σ was the best of all seven measures, and it beat DRT in a paired monthly test (Newey-West t = −11.1). Over a year, the level of volatility is a stable, low-noise property of an asset, and that is precisely what σ measures well. The implication is that σ is a good ranking device for comparing assets and a poor timing device for tracking changes in risk.

### 7b. Calibration: is the measure right as often as it claims?

Calibration is where the bell curve fails most clearly. Each day, for all 49 assets (482,110 forecasts in total), the backtest forecasts the next day's 99% VaR and 97.5% Expected Shortfall and counts breaches. The Kupiec test asks whether the breach rate is actually 1%, the Christoffersen test asks whether breaches are independent or clustered, and the ES ratio test asks whether, on breach days, the realized loss on average matches the predicted ES (a ratio of 1.0 is perfect, and 1.2 means losses were 20% worse than forecast).

| Method (1-day, 99% VaR) | Breach rate (target 1.00%) | Assets passing Kupiec | Passing Christoffersen (cond. coverage) | ES ratio (target 1.00) | Assets passing ES test |
|:-|:-|:-|:-|:-|:-|
| Normal, 1-yr σ | 1.83% | **0%** | 0% | 1.20 | 0% |
| Historical simulation, 1 yr | 1.52% | 2% | 2% | 1.08 | 6% |
| EWMA-normal (RiskMetrics) | 1.72% | 2% | 2% | 1.17 | 0% |
| Cornish-Fisher | 1.20% | 69% | 12% | n/a | n/a |
| FHS | 1.13% | 92% | 63% | 1.01 | 100% |
| DRT | **1.12%** | **96%** | **67%** | **1.01** | **100%** |

(The breach rate is the average across the 49 assets.)

![SPY VaR backtest](/assets/charts/08_spy_var_backtest.png)

The normal model based on σ failed the Kupiec test on every one of the 49 assets. Pooled across all forecasts, it produced 8,422 breaches where 4,821 were expected, 75% more than it promised, and on the days its threshold was breached, losses were on average 20% larger than its Expected Shortfall forecast. For SPY, normal-σ VaR was breached on 2.40% of days, almost two and a half times the advertised 1%, compared with 1.08% for DRT. For Bitcoin, the corresponding figures were 1.95% for the normal model and 0.96% for DRT, and on the full S&P 500 history since 1928 they were 2.05% and 1.09%.

DRT passed the Kupiec test on 47 of 49 assets and got the size of tail losses almost exactly right (an ES ratio of 1.01). It does not solve every problem, however. More than a third of assets (37%) still fail the Christoffersen independence test, and the 98-year S&P 500 series fails the conditional-coverage test for every method, which indicates that breaches still cluster to some degree during crises and that none of these models fully captures clustering.

### 7c. Portfolio test: does it build better portfolios?

The portfolio test uses 16 ETFs (SPY, IWM, EFA, TLT, IEF, LQD, GLD and the nine sector SPDRs), with long-only positions, a maximum weight of 35% per asset, monthly rebalancing, and a transaction cost of 5 basis points per unit of turnover. The out-of-sample period runs from December 2007 to September 2026, so it includes the 2008 crisis, the COVID crash and the 2022 selloff in both stocks and bonds. Each portfolio minimizes its own risk measure: variance (σ), semivariance, historical CVaR (a linear program, following Rockafellar and Uryasev), EWMA variance, FHS-ES, and DRT (minimum 97.5% CVaR on regime-rescaled downside scenarios).

![Portfolio equity and drawdown](/assets/charts/09_portfolio_equity_drawdown.png)

| Portfolio | CAGR | Vol | Sharpe | Sortino | Max DD | Calmar | Daily CVaR 95% | Ulcer | Turnover/yr |
|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|
| Equal weight | 8.63% | 14.17% | 0.56 | 0.78 | 42.0% | 0.21 | 2.16% | 8.06 | 0.32× |
| Min variance (σ) | 4.72% | 6.37% | 0.54 | 0.75 | 20.0% | 0.24 | 0.94% | 4.96 | 1.09× |
| Min semivariance (DD) | 4.98% | 6.44% | 0.57 | 0.80 | 19.2% | 0.26 | 0.96% | 4.74 | 1.36× |
| Min CVaR 95% (hist.) | 5.20% | 6.50% | 0.60 | 0.84 | 19.0% | 0.27 | 0.96% | 4.51 | 1.83× |
| Min EWMA variance | 5.29% | 6.21% | **0.64** | **0.91** | 18.0% | 0.29 | **0.90%** | **4.14** | 4.40× |
| Min FHS-ES | 5.21% | 6.37% | 0.61 | 0.86 | 20.3% | 0.26 | 0.94% | 5.55 | 3.71× |
| Min DRT | **5.42%** | 6.52% | 0.63 | 0.89 | **17.1%** | **0.32** | 0.97% | 4.38 | 3.41× |

The table below shows total return and maximum drawdown within three crisis windows.

| Window | Min variance (σ): return / max DD | Min DRT: return / max DD |
|:-|:-|:-|
| GFC, Jun 2008 to Jun 2009 | −4.5% / 13.1% | −2.0% / 11.6% |
| COVID, Feb to Apr 2020 | −2.7% / 16.3% | +1.6% / 13.7% |
| 2022 bear market | −12.3% / 18.4% | −10.1% / 16.1% |

The DRT portfolio had the smallest maximum drawdown of any strategy (17.1%, compared with 20.0% for minimum variance), the best Calmar ratio (0.32 against 0.24), and the highest return among the low-risk portfolios, and it did better than minimum variance in all three crisis windows.

These results should be read with caution. A stationary block bootstrap (1,000 resamples, with a mean block length of 21 days) puts the difference in maximum drawdown between DRT and minimum variance at −2.9 percentage points, with a 95% confidence interval of [−8.2, +2.5]; DRT was better in 82% of resamples, but the difference is not statistically significant. The Sharpe ratio difference of +0.09 has a confidence interval of [−0.11, +0.26] and is also not significant, and daily CVaR was slightly worse for DRT (+0.03 percentage points, with an interval of [−0.01, +0.07]), which suggests that its advantage lies in avoiding sustained drawdowns rather than individual bad days.

Two further qualifications apply. DRT trades about three times as much as minimum variance (3.4× against 1.1× turnover per year), and while costs are included at 5 basis points, implementations with higher costs would give back some of the advantage. And once again, simple EWMA variance did about as well (a Sharpe ratio of 0.64 and a maximum drawdown of 18.0%), with the lowest daily CVaR and Ulcer index of any portfolio.

### 7d. Scorecard

| Test | Did DRT beat σ? | Strength of evidence |
|:-|:-|:-|
| Normality tests (motivation) | σ's assumption rejected for 49/49 assets | Overwhelming |
| VaR / ES calibration | Yes, decisively (96% vs 0% of assets pass Kupiec; ES ratio 1.01 vs 1.20) | Overwhelming |
| Timing risk within an asset | Yes (69 to 77% of assets; p < 0.001) | Strong |
| Pooled out-of-sample prediction | Slightly ahead, not significant | Weak |
| Ranking risk across assets | No, σ wins | Strong (against DRT) |
| Portfolio drawdown / Calmar | Yes (17.1% vs 20.0%; 0.32 vs 0.24) | Suggestive, not significant |
| Against plain EWMA volatility | No, EWMA matches or beats DRT on prediction | Strong (against DRT) |

Taken together, the evidence says that DRT is a much better tail-loss and VaR number than σ, and a better timing signal. It is not a better tool for ranking assets against each other, and most of its predictive advantage comes from awareness of the current regime, which plain EWMA volatility already provides. The fat-tail multiplier is essential for getting the size of losses right, but it is too noisy to improve the ranking of risk.

## 8. Practical takeaways

The first implication is that standard deviation should not be quoted as a measure of how much you could lose. Across the 49 assets, normal-σ VaR was breached 75% more often than advertised, and losses on breach days were 20% worse than forecast. If a loss estimate is needed, an empirical tail multiplier is more appropriate: for broad equity, roughly 3× the current daily volatility for a one-in-40 bad day, rather than the 2.34× that the normal distribution implies.

The second implication is that current volatility is more informative than one-year volatility. The simplest improvement tested here, RiskMetrics-style EWMA volatility, was the best single predictor of future losses, and it can be computed in a single line of code. The third, related implication is that σ is better suited to comparisons than to timing, since trailing one-year σ was the best way to rank which assets are riskier but a poor guide to when risk is high.

The fourth implication is that sophisticated fixes estimated on short windows deserve skepticism. Cornish-Fisher VaR and one-year historical CVaR predicted worse than plain σ, because skewness and kurtosis estimated from 252 days of data are mostly noise. Along the same lines, the Sortino ratio does not change much in practice: over 10 years, Sharpe and Sortino rankings had a correlation of 0.998, since the asymmetry that matters lies in how volatility reacts to losses (GJR γ = 0.20, α ≈ 0) rather than in the shape of daily returns.

For long-term investors, drawdowns deserve more attention than daily volatility, since risk for them is the depth and duration of a decline (captured by maximum drawdown and the Ulcer index). The DRT and EWMA portfolios reduced maximum drawdown from 20% to 17–18%, but no measure eliminates drawdowns. For individual stocks, the floor at a 100% loss matters, because long-horizon returns are strongly right-skewed (skew of +7 on annual returns): σ overstates the downside of a diversified basket of winners and losers and understates the chance that a single stock goes to zero, which is an argument for diversification.

Finally, no trailing measure anticipates the first shock. At the end of August 2008, SPY's trailing one-year σ was 19.8% annualized, elevated but not alarming, and over the next three months SPY fell 41% from peak to trough, a loss that none of the measures examined here came close to forecasting. Risk measures are useful for sizing positions and surviving the second and third shocks of a crisis, but the evidence does not suggest they can predict the first.

## 9. Conclusion

Standard deviation became the default measure of risk not because anyone believed markets were normal (Mandelbrot and Fama showed otherwise more than 60 years ago), but because it was tractable, it fit into an elegant body of theory, and it was built into software, textbooks and regulation. Its assumptions fail in every dataset analyzed here: 49 of 49 assets reject normality, the S&P 500 has had 50 "once in 13,800 years" days since 1928, volatility clusters with a half-life of about 150 days, and the floor at a 100% loss makes long-run stock returns strongly skewed.

The more interesting finding is that σ fails in specific ways rather than in every way. It is a poor forecaster of losses and a poor timing tool, but a good tool for ranking assets against one another. The proposed measure, DRT (downside regime × empirical tail), addresses the forecasting failure decisively (96% against 0% of assets passing VaR backtests), improves risk timing for most assets, and produced the minimum-risk portfolio with the smallest drawdown. It did not beat σ at ranking assets, it did not beat simple EWMA volatility at prediction, and its portfolio advantages were not statistically significant over 19 years.

The evidence therefore points less toward replacing σ than toward recognizing what it is good at. The larger errors in treating σ as risk come from assuming that risk is constant and that tails are thin, rather than from penalizing upside volatility. Conditional volatility addresses the first problem and an empirical tail multiplier addresses the second, while σ remains a reasonable tool for comparing assets, which suggests that a sensible risk process uses each measure for the question it answers best.

## Methods and reproducibility

The code consists of `download_data.py` (data download), `analysis.py` (all statistics and charts) and `make_formula.py`, and the results are in `results.csv` (long format, about 1,700 rows), with detailed tables in `results/`. Returns are simple daily returns from Yahoo Finance adjusted closes through 2026-09-30; ^GSPC is a price index (no dividends), and Bitcoin, which trades seven days a week, is annualized with 365 days where relevant.

The analysis avoids look-ahead throughout: every risk measure at date *t* uses only data through *t*, standardized shocks use the previous day's scale, and out-of-sample regressions use only target windows that had fully ended.

The analysis has several limitations. The 26 stocks are today's survivors, which understates single-stock crash risk, and Yahoo adjusted prices can contain occasional data errors, with older data less reliable. Overlapping 3-month and 12-month targets are handled with Newey-West and block-bootstrap methods, but the effective sample sizes for 12-month drawdowns are much smaller than the raw counts suggest. The portfolio test covers one universe and one 19-year period. Finally, DRT's κ uses 3 years of data (about 19 tail observations), and a longer or shrunk estimate may help; that variation was deliberately not tested, to avoid tuning on the results.

## References

Acerbi, C., & Tasche, D. (2002). On the coherence of expected shortfall. *Journal of Banking & Finance*, 26(7), 1487–1503.

Artzner, P., Delbaen, F., Eber, J.-M., & Heath, D. (1999). Coherent measures of risk. *Mathematical Finance*, 9(3), 203–228.

Barone-Adesi, G., Giannopoulos, K., & Vosper, L. (1999). VaR without correlations for portfolios of derivative securities. *Journal of Futures Markets*, 19(5), 583–602.

Basel Committee on Banking Supervision (1996). *Amendment to the Capital Accord to Incorporate Market Risks*; and *Supervisory Framework for the Use of "Backtesting" in Conjunction with the Internal Models Approach*. BIS.

Basel Committee on Banking Supervision (2016; revised 2019). *Minimum capital requirements for market risk* (Fundamental Review of the Trading Book). BIS.

Bessembinder, H. (2018). Do stocks outperform Treasury bills? *Journal of Financial Economics*, 129(3), 440–457.

Black, F. (1976). Studies of stock price volatility changes. *Proceedings of the 1976 Meetings of the American Statistical Association, Business and Economic Statistics Section*, 177–181.

Black, F., & Scholes, M. (1973). The pricing of options and corporate liabilities. *Journal of Political Economy*, 81(3), 637–654.

Bollerslev, T. (1986). Generalized autoregressive conditional heteroskedasticity. *Journal of Econometrics*, 31(3), 307–327.

Chamberlain, G. (1983). A characterization of the distributions that imply mean-variance utility functions. *Journal of Economic Theory*, 29(1), 185–201.

Christoffersen, P. F. (1998). Evaluating interval forecasts. *International Economic Review*, 39(4), 841–862.

Cont, R. (2001). Empirical properties of asset returns: stylized facts and statistical issues. *Quantitative Finance*, 1(2), 223–236.

Diebold, F. X., & Mariano, R. S. (1995). Comparing predictive accuracy. *Journal of Business & Economic Statistics*, 13(3), 253–263.

Dowd, K., Cotter, J., Humphrey, C., & Woods, M. (2008). How unlucky is 25-sigma? *Journal of Portfolio Management*, 34(4), 76–80.

Embrechts, P., Klüppelberg, C., & Mikosch, T. (1997). *Modelling Extremal Events for Insurance and Finance*. Springer.

Engle, R. F. (1982). Autoregressive conditional heteroscedasticity with estimates of the variance of United Kingdom inflation. *Econometrica*, 50(4), 987–1007.

Fama, E. F. (1965). The behavior of stock-market prices. *Journal of Business*, 38(1), 34–105.

Favre, L., & Galeano, J.-A. (2002). Mean-modified value-at-risk optimization with hedge funds. *Journal of Alternative Investments*, 5(2), 21–25.

Federal Reserve History (n.d.). Near failure of Long-Term Capital Management. Federal Reserve Bank essay, federalreservehistory.org.

Financial Times (2007, August 13). Goldman pays the price of being big. (Source of the David Viniar "25-standard deviation moves" quote.)

Glosten, L. R., Jagannathan, R., & Runkle, D. E. (1993). On the relation between the expected value and the volatility of the nominal excess return on stocks. *Journal of Finance*, 48(5), 1779–1801.

Harvey, C. R., & Siddique, A. (2000). Conditional skewness in asset pricing tests. *Journal of Finance*, 55(3), 1263–1295.

Hull, J., & White, A. (1998). Incorporating volatility updating into the historical simulation method for value-at-risk. *Journal of Risk*, 1(1), 5–19.

J.P. Morgan/Reuters (1996, December). *RiskMetrics Technical Document* (4th ed.). Morgan Guaranty Trust Company.

Keating, C., & Shadwick, W. F. (2002). A universal performance measure. *Journal of Performance Measurement*, 6(3), 59–84.

Kraus, A., & Litzenberger, R. H. (1976). Skewness preference and the valuation of risk assets. *Journal of Finance*, 31(4), 1085–1100.

Kupiec, P. H. (1995). Techniques for verifying the accuracy of risk measurement models. *Journal of Derivatives*, 3(2), 73–84.

Levy, H., & Markowitz, H. M. (1979). Approximating expected utility by a function of mean and variance. *American Economic Review*, 69(3), 308–317.

Lintner, J. (1965). The valuation of risk assets and the selection of risky investments in stock portfolios and capital budgets. *Review of Economics and Statistics*, 47(1), 13–37.

Lowenstein, R. (2000). *When Genius Failed: The Rise and Fall of Long-Term Capital Management*. Random House.

Mandelbrot, B. (1963). The variation of certain speculative prices. *Journal of Business*, 36(4), 394–419.

Markowitz, H. (1952). Portfolio selection. *Journal of Finance*, 7(1), 77–91.

Markowitz, H. M. (1959). *Portfolio Selection: Efficient Diversification of Investments*. Wiley (Cowles Foundation Monograph 16).

Markowitz, H. M. (1999). The early history of portfolio theory: 1600–1960. *Financial Analysts Journal*, 55(4), 5–16.

Martin, P. G., & McCann, B. B. (1989). *The Investor's Guide to Fidelity Funds*. Wiley.

McNeil, A. J., & Frey, R. (2000). Estimation of tail-related risk measures for heteroscedastic financial time series: an extreme value approach. *Journal of Empirical Finance*, 7(3–4), 271–300.

Mossin, J. (1966). Equilibrium in a capital asset market. *Econometrica*, 34(4), 768–783.

Rockafellar, R. T., & Uryasev, S. (2000). Optimization of conditional value-at-risk. *Journal of Risk*, 2(3), 21–41.

Roy, A. D. (1952). Safety first and the holding of assets. *Econometrica*, 20(3), 431–449.

Sharpe, W. F. (1963). A simplified model for portfolio analysis. *Management Science*, 9(2), 277–293.

Sharpe, W. F. (1964). Capital asset prices: A theory of market equilibrium under conditions of risk. *Journal of Finance*, 19(3), 425–442.

Sharpe, W. F. (1966). Mutual fund performance. *Journal of Business*, 39(1, Part 2: Supplement on Security Prices), 119–138.

Sharpe, W. F. (1994). The Sharpe ratio. *Journal of Portfolio Management*, 21(1), 49–58.

Sortino, F. A., & van der Meer, R. (1991). Downside risk. *Journal of Portfolio Management*, 17(4), 27–31.

Tobin, J. (1958). Liquidity preference as behavior towards risk. *Review of Economic Studies*, 25(2), 65–86.

Young, T. W. (1991, October). Calmar ratio: A smoother tool. *Futures*, 20(12), 40.

Zangari, P. (1996). A VaR methodology for portfolios that include options. *RiskMetrics Monitor*, First Quarter, 4–12.

*This article is for educational purposes and is not investment advice.*
