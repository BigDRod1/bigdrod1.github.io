---
layout: post
title: "Same Screen, Same Numbers: Consensus Estimates and the Problem of Independent Thinking"
summary: "How consensus estimates are built, how they behave in 42,515 quarterly earnings reports and 57 years of forecaster data, what happened when shared views became shared positions in August 2007, and practical ways to form an independent view."
date: 2026-10-27
published: true
permalink: /articles/same-screen-same-numbers/
author: Diego Rodriguez
image: /assets/brand/banner.png
description: >-
  How consensus estimates and shared platforms such as the Bloomberg Terminal
  shape investing: earnings surprises, the walk down, analyst herding, the
  Survey of Professional Forecasters, the August 2007 quant unwind and methods
  for forming an independent view.
---

# Same Screen, Same Numbers: Consensus Estimates and the Problem of Independent Thinking

Most of the people who set prices in public equity markets start their day looking at the same numbers. The consensus earnings estimate for a company, the average of the forecasts published by the analysts who cover it, appears on the Bloomberg Terminal, on FactSet, on LSEG Workspace and on every free quote page. Earnings season is scored against it, guidance is framed around it, and valuation multiples are computed on it.

That shared starting point raises an uncomfortable question. If almost every professional works from the same tool and the same estimates, it is not obvious how anyone forms a view that is genuinely their own, or whether the consensus itself can be trusted. This article looks at how the consensus is built, how it behaves in the data, what happens to markets when everyone holds the same position, the case in favor of the crowd, and the practical tools that make an independent view possible.

## What a consensus estimate is

A consensus estimate is a simple statistic, usually the mean or median of the current forecasts that sell side analysts have submitted for a company's earnings per share, revenue or another line item. Data vendors collect the individual forecasts, check that they are on a comparable accounting basis, drop forecasts that have gone stale, and publish the summary. Bloomberg's version is called BEst, and Bloomberg's own documentation describes the BEst EPS consensus as the mean of sell side analyst estimates [1].

The oldest of these services is I/B/E/S, the Institutional Brokers' Estimate System, now owned by LSEG. Its U.S. history begins in 1976 and its international history in 1987, and LSEG says it now covers more than 22,000 companies with estimates sourced from more than 950 firms and 18,000 analysts [2]. FactSet runs a competing estimates database, and notes in its research that it aggregates and redistributes estimates data and does not conduct independent research of its own [3].

The vendors therefore do not forecast anything. The consensus is a summary of what a few dozen people employed by brokers and investment banks expect, and its quality depends entirely on their incentives and their independence from one another.

## The Bloomberg Terminal

The Terminal is the place where most professionals meet those numbers. Bloomberg describes it as connecting a global network of more than 350,000 decision makers [4]. Bloomberg is private and does not publish its prices, but its notice to clients, reported by NeuGroup, set the annual cost from January 1, 2025 at $31,980 for a client with a single Terminal and $28,320 per Terminal for clients with more than one, an increase of 6.5% that Bloomberg linked to weighted global inflation [5].

Its revenue has to be estimated from outside. The Financial Times, using BCG Expand data, put Bloomberg's 2025 revenue at roughly $14.4 billion, larger than the roughly $12.3 billion combined revenue of the more than 1,800 other market data vendors that BCG Expand tracks [6]. Burton Taylor International Consulting estimates that total global spending on financial market data and analysis reached a record $49.2 billion in 2025, up 6.5% from 2024 [7].

Terminals are the largest product category in that market. BCG Expand estimates that they accounted for 32% of industry revenue in 2025 [8]. FactSet, the closest rival in estimates data, reports more than 9,100 clients and more than 247,000 individual users [3].

The point for this article is concentration rather than price. When a large share of the professional market sees the same consensus figure, the same news headline and the same screen of comparable company multiples at the same moment, the inputs to independent judgment are much less independent than the number of people looking at them suggests.

## The bar that results clear

If analyst forecasts were unbiased, results would land above and below the consensus in roughly equal numbers. They do not. FactSet reports that over the past ten years, 77% of S&P 500 companies have reported EPS above the mean estimate, and with 9% of the index reporting third quarter 2026 results as of October 16, the share was 84% [3].

![Beat rate and surprise size, FactSet](/assets/charts/cons_01_beat_rate_factset.png)

The size of those beats is often modest. In the same report, aggregate earnings were 2.6% above estimates, against a ten year average of 8.0% [3]. A high share of companies clearing the bar by small amounts is what a bar set slightly below expected results looks like.

To see the pattern over a longer period, the analysis collected the consensus EPS estimate and reported EPS for every quarterly report that Yahoo Finance lists for the current members of the S&P 500. That produced 42,515 quarterly reports from 500 companies between January 2002 and October 2026. The beat rate in these data averaged 77.4% from 2021 to 2025, close to FactSet's five year average of 78%, which suggests the free data track the professional series reasonably well.

![Beat, meet and miss rates by year](/assets/charts/cons_05_beat_meet_miss_by_year.png)

The long run trend is striking. In 2002, 55% of reports beat the consensus, 28% matched it exactly and 17% missed. By 2025, 79% beat, only 4% matched exactly, and the miss rate was still 17%. The rise in beats roughly mirrors the fall in exact meets, which suggests that results that once landed on the estimate now tend to land a cent or more above it.

The distribution of surprises in cents shows how close to the line many of those beats are. In the sample, 4,739 reports beat the consensus by exactly one cent while 1,732 missed it by exactly one cent, a ratio of 2.7 to 1. A smooth distribution of forecast errors would put roughly similar numbers on either side of zero.

![Distribution of earnings surprises in cents](/assets/charts/cons_04_surprise_distribution_cents.png)

Academic work has documented this discontinuity for decades. Degeorge, Patel and Zeckhauser showed that reported earnings bunch just above three thresholds, positive profits, the prior year's result and analyst expectations [9]. Brown and Caylor found that from the mid 1990s onward, avoiding a negative surprise relative to analyst estimates became the threshold managers prioritized most [10].

Managers say as much themselves. In a survey of 401 financial executives, Graham, Harvey and Rajgopal found that 78% would give up economic value in exchange for smooth earnings, and that a majority would avoid a project with positive net present value if it meant missing the current quarter's consensus [11].

## The walk down

The consensus also moves in a predictable direction as results approach. FactSet tracks the bottom up EPS estimate for the S&P 500, an aggregation of the median estimates for every company in the index, from the first to the last day of each quarter. Over the past 20 years it has fallen by an average of 4.2% during the quarter, over 15 years by 3.2%, over ten years by 2.5% and over five years by 2.2% [12].

![Change in quarterly estimates during the quarter, FactSet](/assets/charts/cons_02_walkdown_factset.png)

Richardson, Teoh and Wysocki describe the same pattern at the company level as a walk down to beatable forecasts, in which analysts start optimistic and lower their estimates to levels that firms can beat at the announcement. They found the walk down was most pronounced when the firm or its insiders were net sellers of stock after the earnings announcement [13].

The third quarter of 2026 has been an exception. FactSet reports that the bottom up EPS estimate rose 1.4%, from $88.64 to $89.84, between June 30 and September 30, the second straight quarter of increases, driven mainly by the Energy and Information Technology sectors [12]. The walk down is a strong tendency in the data, not a rule.

## Optimism in ratings and price targets

Recommendations lean even more heavily in one direction. FactSet counts 13,234 analyst ratings on S&P 500 stocks, of which 60.1% are Buy, 35.3% are Hold and 4.7% are Sell [3]. The analysis of Yahoo Finance recommendation counts, fetched on October 21, 2026, gives a similar split, with 61.1% Buy or Strong Buy and 4.0% Sell or Strong Sell across 11,766 ratings, and 51% of S&P 500 companies had no Sell rating at all.

![Analyst ratings on S&P 500 stocks, FactSet](/assets/charts/cons_03_ratings_mix_factset.png)

Price targets show the same tilt. FactSet's bottom up target for the S&P 500 was 20.3% above the index level in its October 16 report [3]. Across the 499 index members with Yahoo Finance target data, the median stock had a mean price target 14.6% above its current price, and only 10% had a mean target below the price.

![Distribution of implied upside in price targets](/assets/charts/cons_06_price_target_upside.png)

Incentives explain part of this. Many sell side analysts work at banks that earn underwriting and advisory fees from the companies they cover, and depend on access to those companies' management. Michaely and Womack found that stocks recommended by analysts at the bank that underwrote them performed worse than Buy recommendations from unaffiliated brokers [14]. In 2003, the SEC and other regulators announced a settlement with ten investment firms over research conflicts totaling about $1.4 billion, along with structural reforms separating research from investment banking [15].

## Herding, cascades and anchoring

Analysts also have reasons to stay close to each other. Hong, Kubik and Solomon found that inexperienced analysts were more likely to lose their jobs for bold forecasts that departed from the consensus, even controlling for accuracy, and that they herded more as a result [16]. Being wrong together carries a smaller career cost than being wrong alone.

Herding has a price in accuracy. Clement and Tse classified forecasts as bold when they moved away from both the analyst's own prior forecast and the consensus, and found that bold forecasts were more accurate than herding forecasts [17]. Welch found that an analyst's recommendation is positively influenced by the prevailing consensus and by the most recent revisions of other analysts [18].

Information cascades offer a theory of why this can happen even without career concerns. Bikhchandani, Hirshleifer and Welch showed that when people act in sequence and can observe earlier choices, it can become rational to ignore private information and follow the crowd, so that a cascade forms on the basis of very little real information and can break on a small shock [19].

Anchoring adds a cognitive layer. Cen, Hilary and Wei found that analysts anchor on the industry median forecast EPS, producing optimistic forecasts when a firm's forecast EPS is below the industry median and pessimistic ones when it is above, with predictable effects on subsequent returns [20]. The consensus itself is the most visible anchor of all, since every analyst sees it before publishing.

## How much do analysts disagree?

The spread of estimates is narrow. In Yahoo Finance data fetched on October 21, 2026, the median S&P 500 company had 19 analysts estimating its current fiscal year EPS, and the gap between the highest and lowest estimate was 5.8% of the mean. For the next fiscal year, the same gap was 14.6% of the mean.

Those ranges are small relative to how much earnings actually change. A narrow range can reflect genuine certainty, but it is also what herding toward a shared figure would produce, and the two are hard to tell apart in advance.

When analysts do disagree, the disagreement carries information. Diether, Malloy and Scherbina found that stocks with higher dispersion in analyst earnings forecasts earned lower subsequent returns than otherwise similar stocks, and interpreted dispersion as a measure of differences of opinion that prices did not fully reflect [21].

## When everyone holds the same view

A consensus that is right on average can still fail badly when it is wrong, because the errors are shared. The analysis tested this on the Federal Reserve Bank of Philadelphia's Survey of Professional Forecasters, which publishes every individual forecast since 1968 [22]. It compared 8,257 individual forecasts of the unemployment rate four quarters ahead, from 222 quarterly surveys between 1968 and 2025, with the realized quarterly average unemployment rate.

![Median SPF unemployment forecast versus actual](/assets/charts/cons_07_spf_unemployment_forecasts.png)

The errors are strongly correlated. In 51% of the surveys, at least 90% of forecasters erred in the same direction, and in the 40 surveys where the median forecast missed by a full percentage point or more, an average of 99% of forecasters were on the same side of the outcome, and the actual rate fell outside the range between the 10th and 90th percentile forecasts every time. In the second quarter of 2008, all 45 forecasters expected unemployment a year later to be below 6.3%, with a median of 5.5%, and the actual rate in the second quarter of 2009 averaged 9.3%.

Markets face the same problem when positions, not just forecasts, converge. In the week of August 6, 2007, a number of quantitative long/short equity funds suffered large losses at the same time. Khandani and Lo simulated a simple contrarian strategy that lost 6.85% over August 7 to 9, about 12 daily standard deviations, and then gained 5.92% on August 10, and attributed the episode to the rapid unwinding of one or more large portfolios in a strategy space that had become crowded [23].

![Factor returns in August 2007](/assets/charts/cons_09_quant_quake_aug2007.png)

The episode is visible in public factor data. Using the daily value (HML) and momentum factors from the Kenneth French Data Library, an equal mix of the two lost 2.9% from August 6 to 9, about 10.6 times its 2006 daily standard deviation, while the market factor rose 1.4% over the same days, and the mix recovered 1.3% on August 10 [24]. The losses came from many funds holding similar positions, not from any change in the companies they owned.

Stein described the general mechanism in his 2009 presidential address to the American Finance Association. When many sophisticated investors pursue the same strategy without knowing how many others are in it, and finance it with leverage, their trading can push prices away from fundamentals rather than toward them [25].

## The case for the consensus

None of this means the consensus is useless, and the counterargument is strong. In 1907, Francis Galton analyzed 787 guesses of the weight of an ox at a livestock fair and found that the median guess of 1,207 pounds was within 1% of the actual dressed weight of 1,198 pounds [26]. Averaging many estimates cancels out individual errors as long as those errors are not all in the same direction.

The same Survey of Professional Forecasters data that show correlated failures also show the value of aggregation. Over the full sample, the median forecast had an average absolute error of 0.70 percentage points, against 0.80 for the average individual forecast. Of the 141 forecasters who submitted at least 20 forecasts, only 26% were more accurate than the median over the same surveys.

![Individual forecasters versus the median](/assets/charts/cons_08_spf_forecaster_vs_median.png)

The conditions for that result matter. Surowiecki argued that crowds are wise when their members are diverse and independent [27], and Lorenz, Rauhut, Schweitzer and Helbing showed experimentally that even mild exposure to other people's estimates reduces the diversity of a group's answers without improving its collective accuracy, while making individuals more confident [28]. A consensus built from analysts who all see each other's numbers sits somewhere between an independent crowd and a single opinion repeated many times.

Alternative data are often presented as the way out, since satellite images, card transactions and web traffic offer information that is not in the consensus. The evidence shows they can carry real information. Katona, Painter, Patatoukas and Zeng found that sophisticated investors used satellite images of retailer parking lots to anticipate bad quarterly news, but also that unequal access to these data increased information asymmetry without immediately improving price discovery [29]. As more funds buy the same datasets, alternative data risk becoming another shared input.

## Forming an independent view

An independent view does not require rejecting the consensus, only arriving at a number before looking at it. The most direct method is to build a model from the company's own filings, starting from revenue drivers, margins and reinvestment, and to compare the result with the consensus only at the end. A forecast built this way can still be wrong, but its errors are its own rather than a copy of the crowd's.

Base rates are the second tool. Kahneman and Lovallo distinguished between the inside view, which builds a forecast from the details of the case at hand, and the outside view, which asks how similar cases have turned out [30]. Mauboussin, Callahan and Majd applied the idea to corporate performance, publishing distributions of sales growth and other measures across large samples of companies [31], so that a forecast of 25% annual growth for a decade can be checked against how rarely companies of a given size have achieved it.

The third is to make the story explicit. Damodaran argues that every valuation is a narrative expressed in numbers, and that each input, growth, margins, reinvestment and risk, should be traceable to a specific claim about the business that can be tested and revised [32]. Writing down the story before opening the estimates screen makes it harder for the consensus to become the narrative by default.

The fourth is to run the problem in reverse. Mauboussin and Rappaport's expectations investing approach starts from the current price and solves for the growth and margins it implies, then asks whether those expectations are reasonable [33]. Damodaran applies the same logic at the market level each month, backing out the equity risk premium implied by the level of the S&P 500 [34]. A reverse valuation does not rely on anyone's forecast, so it is a useful check on both the consensus and one's own model.

The last tool is a record. Writing down forecasts and the reasons for them, and comparing them later with both the outcome and the consensus, shows whether departures from the crowd have added information or only noise. The Survey of Professional Forecasters data suggest that most forecasters do not beat the median over time, which is a reason to treat a disagreement with the consensus as a claim that needs evidence.

## Methodology and data

Earnings data are the EPS estimate and reported EPS fields that Yahoo Finance displays for each quarterly report, collected with the yfinance library on October 21, 2026 for the 503 share classes listed as S&P 500 constituents on Wikipedia that day, giving 42,515 reports from 500 companies between January 2002 and October 21, 2026 [35]. The sample includes only companies in the index today, so it is subject to survivorship bias, and Yahoo does not document the vintage or provider of its historical consensus figures, so these results should be read as indicative and were checked against FactSet's published averages. Free data do not include the history of individual analyst estimates, so the walk down analysis relies on FactSet's published statistics.

Ratings, price targets and the high and low estimates come from the same Yahoo Finance fetch. Implied upside is the mean price target divided by the current price, and the estimate range is the highest minus the lowest estimate divided by the absolute mean, for companies with at least five estimates and a mean above 10 cents.

The forecaster analysis uses the UNEMP6 variable of the Survey of Professional Forecasters microdata, the forecast of the quarterly average unemployment rate four quarters after the survey quarter, scored against the quarterly average of the BLS unemployment rate (FRED series UNRATE, current vintage) for surveys from 1968Q4 to 2025Q3 [22][36]. Forecaster comparisons use only the surveys in which each forecaster participated. Factor returns are the daily HML and momentum factors from the Kenneth French Data Library, built from the August 2026 CRSP file, with cumulative returns computed arithmetically [24]. Code and data are in the code and data folders.

## References

1. Bloomberg L.P., "Forecasts" (Bloomberg Terminal guide, via WU Vienna University Library). https://library.wu.ac.at/bib/fit4research/wp-content/uploads/2024/02/Forecasts_manuals_Bloomberg.pdf
2. LSEG, "Broker Estimates (I/B/E/S)," data catalogue, accessed October 21, 2026. https://www.lseg.com/en/data-catalogue/company-data/ibes-estimates/broker-estimates
3. FactSet, "Earnings Insight," October 16, 2026. https://advantage.factset.com/hubfs/Website/Resources%20Section/Research%20Desk/Earnings%20Insight/EarningsInsight_101626.pdf
4. Bloomberg Professional Services, "Bloomberg Terminal," accessed October 21, 2026. https://professional.bloomberg.com/products/bloomberg-terminal/
5. NeuGroup, "Bloomberg Terminals: How Much More You'll Pay Next Year," October 9, 2024. https://connect.neugroup.com/public/blogs/bloomberg-terminals-how-much-more-youll-pay-next-year
6. MDC News, "After Bloomberg: Market Data Is Becoming a War of Interfaces, Not Platforms" (citing Financial Times analysis of BCG Expand data). https://www.mdc.news/post/after-bloomberg-market-data-is-becoming-a-war-of-interfaces-not-platforms
7. Burton Taylor International Consulting (TP ICAP), "Real Time Analytics Drive Record Growth Across the Financial Market Data Landscape," via Mondo Visione, March 26, 2026. https://mondovisione.com/media-and-resources/news/realtime-analytics-drive-record-growth-across-the-financial-market-data-landsca-2026326/
8. A-Team Insight, "BCG Expand: Market Data Industry Tops $50bn as Growth Normalises and Cost Discipline Tightens," 2026. https://a-teaminsight.com/blog/bcg-expand-market-data-industry-tops-50bn-as-growth-normalises-and-cost-discipline-tightens/
9. Degeorge, F., J. Patel and R. Zeckhauser (1999), "Earnings Management to Exceed Thresholds," Journal of Business 72(1), 1 to 33.
10. Brown, L. D. and M. L. Caylor (2005), "A Temporal Analysis of Quarterly Earnings Thresholds: Propensities and Valuation Consequences," The Accounting Review 80(2), 423 to 440. https://doi.org/10.2308/accr.2005.80.2.423
11. Graham, J. R., C. R. Harvey and S. Rajgopal (2005), "The Economic Implications of Corporate Financial Reporting," Journal of Accounting and Economics 40, 3 to 73. NBER Working Paper 10550. https://www.nber.org/papers/w10550
12. FactSet, "Earnings Insight," October 2, 2026. https://advantage.factset.com/hubfs/Website/Resources%20Section/Research%20Desk/Earnings%20Insight/EarningsInsight_100226.pdf
13. Richardson, S., S. H. Teoh and P. D. Wysocki (2004), "The Walk Down to Beatable Analyst Forecasts: The Role of Equity Issuance and Insider Trading Incentives," Contemporary Accounting Research 21(4), 885 to 924. https://ideas.repec.org/a/wly/coacre/v21y2004i4p885-924.html
14. Michaely, R. and K. L. Womack (1999), "Conflict of Interest and the Credibility of Underwriter Analyst Recommendations," Review of Financial Studies 12(4), 653 to 686.
15. U.S. Securities and Exchange Commission, "Ten of Nation's Top Investment Firms Settle Enforcement Actions Involving Conflicts of Interest Between Research and Investment Banking," press release 2003 54, April 28, 2003. https://www.sec.gov/news/press/2003-54.htm
16. Hong, H., J. D. Kubik and A. Solomon (2000), "Security Analysts' Career Concerns and Herding of Earnings Forecasts," RAND Journal of Economics 31(1), 121 to 144. https://ideas.repec.org/a/rje/randje/v31y2000ispringp121-144.html
17. Clement, M. B. and S. Y. Tse (2005), "Financial Analyst Characteristics and Herding Behavior in Forecasting," Journal of Finance 60(1), 307 to 341. https://doi.org/10.1111/j.1540-6261.2005.00731.x
18. Welch, I. (2000), "Herding Among Security Analysts," Journal of Financial Economics 58(3), 369 to 396.
19. Bikhchandani, S., D. Hirshleifer and I. Welch (1992), "A Theory of Fads, Fashion, Custom, and Cultural Change as Informational Cascades," Journal of Political Economy 100(5), 992 to 1026.
20. Cen, L., G. Hilary and K. C. J. Wei (2013), "The Role of Anchoring Bias in the Equity Market: Evidence from Analysts' Earnings Forecasts and Stock Returns," Journal of Financial and Quantitative Analysis 48(1), 47 to 76. https://ideas.repec.org/a/cup/jfinqa/v48y2013i01p47-76_00.html
21. Diether, K. B., C. J. Malloy and A. Scherbina (2002), "Differences of Opinion and the Cross Section of Stock Returns," Journal of Finance 57(5), 2113 to 2141. https://doi.org/10.1111/0022-1082.00490
22. Federal Reserve Bank of Philadelphia, Survey of Professional Forecasters, individual forecasts microdata (SPFmicrodata.xlsx), downloaded October 21, 2026. https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/individual-forecasts
23. Khandani, A. E. and A. W. Lo (2007), "What Happened to the Quants in August 2007?" MIT working paper, September 20, 2007; published in Journal of Investment Management 5(4). https://web.mit.edu/Alo/www/Papers/august07.pdf
24. Kenneth R. French Data Library, "Fama/French 3 Factors [Daily]" and "Momentum Factor (Mom) [Daily]," CRSP August 2026 vintage, downloaded October 21, 2026. https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
25. Stein, J. C. (2009), "Presidential Address: Sophisticated Investors and Market Efficiency," Journal of Finance 64(4), 1517 to 1548.
26. Galton, F. (1907), "Vox Populi," Nature 75, 450 to 451. https://doi.org/10.1038/075450a0
27. Surowiecki, J. (2004), The Wisdom of Crowds, Doubleday.
28. Lorenz, J., H. Rauhut, F. Schweitzer and D. Helbing (2011), "How Social Influence Can Undermine the Wisdom of Crowd Effect," Proceedings of the National Academy of Sciences 108(22), 9020 to 9025. https://doi.org/10.1073/pnas.1008636108
29. Katona, Z., M. Painter, P. N. Patatoukas and J. Zeng (2025), "On the Capital Market Consequences of Big Data: Evidence from Outer Space," Journal of Financial and Quantitative Analysis 60(2), 551 to 579. https://doi.org/10.1017/s0022109023001448
30. Kahneman, D. and D. Lovallo (1993), "Timid Choices and Bold Forecasts: A Cognitive Perspective on Risk Taking," Management Science 39(1), 17 to 31.
31. Mauboussin, M. J., D. Callahan and D. Majd (2016), "The Base Rate Book: Integrating the Past to Better Anticipate the Future," Credit Suisse.
32. Damodaran, A. (2017), Narrative and Numbers: The Value of Stories in Business, Columbia Business School Publishing.
33. Mauboussin, M. J. and A. Rappaport (2021), Expectations Investing: Reading Stock Prices for Better Returns, revised edition, Columbia Business School Publishing.
34. Damodaran, A., "Implied Equity Risk Premiums for the US," Damodaran Online. https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/implpr.html
35. Yahoo Finance via the yfinance Python library, earnings dates, analyst recommendations, price targets and earnings estimates, fetched October 21, 2026; S&P 500 constituents from Wikipedia, "List of S&P 500 companies," accessed October 21, 2026.
36. U.S. Bureau of Labor Statistics, Unemployment Rate (UNRATE), retrieved from FRED, Federal Reserve Bank of St. Louis, October 21, 2026. https://fred.stlouisfed.org/series/UNRATE
