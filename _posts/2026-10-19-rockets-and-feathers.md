---
layout: post
title: "Rockets and Feathers: Why Gas Prices Rise Fast and Fall Slowly"
summary: "Why pump prices rise quickly when costs go up and drift down slowly when costs fall, tested on 34 years of weekly EIA price data, with the seasons, psychology and law behind it."
date: 2026-10-19
published: true
permalink: /articles/rockets-and-feathers/
author: Diego Rodriguez
image: /assets/brand/banner.png
description: >-
  Why gas prices rise fast and fall slowly: the price stack, seasonality,
  consumer search, tacit coordination, price gouging law and the 2026 shocks,
  tested on weekly EIA data from 1992 to 2026.
---

# Rockets and Feathers: Why Gas Prices Rise Fast and Fall Slowly

Every driver has a version of the same complaint. When oil spikes, the sign at the corner station seems to change before the evening news finishes the story, and when oil falls, the relief arrives in pennies over weeks. Economists have a name for this pattern, "rockets and feathers," and they have been arguing about its causes for three decades.

This article takes the complaint seriously. It breaks down what goes into a gallon of gasoline, looks at the seasonal forces that move prices every year, reviews the psychology and the law, and tests the asymmetry directly on 34 years of weekly U.S. price data. It closes with the forces pushing pump prices higher in the fall of 2026.

## What goes into a gallon

The price on the sign is a stack of four layers. The U.S. Energy Information Administration (EIA) splits it into crude oil, refining costs and margins, distribution and marketing costs and margins, and taxes. In its May 2026 breakdown, with regular gasoline at $4.48 a gallon, crude accounted for 52%, refining for 22%, distribution and marketing for 15%, and taxes for 12% [1].

Crude is the largest and most volatile layer. A barrel holds 42 gallons, so every $10 move in a barrel of crude translates to roughly 24 cents a gallon before anything else changes. That arithmetic is why the headline price of Brent or WTI dominates coverage of gas prices, even though it is only half the story.

Refining is measured by the crack spread, the gap between the wholesale price of gasoline and the price of the crude it is made from. It is the layer that swings most with refinery outages, inventories and seasonal demand. The analysis below estimates that the gasoline crack spread over Brent averaged 19 cents a gallon in 2019, 61 cents in 2022 and 76 cents so far in 2026.

Distribution and marketing covers pipelines, terminals, trucking, the station's costs and the retailer's margin. Taxes are a mix of a fixed federal excise of 18.4 cents a gallon, unchanged since 1993, and state excise taxes and fees that vary widely by state [2]. Because most of these taxes are charged per gallon rather than as a percentage, the tax share of the price falls as prices rise.

Two regulatory costs sit inside the refining layer. The first is fuel volatility rules: from June 1 to September 15, the Environmental Protection Agency limits the Reid vapor pressure (RVP) of gasoline sold at retail to reduce smog, which requires a costlier summer blend [3]. The second is the Renewable Fuel Standard, under which refiners and importers must blend biofuels or buy credits called Renewable Identification Numbers (RINs), whose cost is passed through to wholesale prices [4].

## Seasonality

Gasoline prices have a calendar. Demand rises into the summer driving season, refiners take units offline for maintenance in late winter and early spring, and the switch to the summer blend raises production costs at the same time. The analysis averaged the crack spread by calendar month from 2000 to 2025 and found it at about 15 to 21 cents a gallon from November through February, rising to 33 to 36 cents in April through June.

The fall reverses the pattern. Once the summer volatility season ends in mid September, cheaper winter blends are allowed and driving demand eases, so the refining margin tends to drift down through December. Hurricane season is the main exception, because it peaks in August and September, and the Gulf Coast holds a large share of U.S. refining capacity.

The fall of 2026 shows how quickly that exception can matter. On October 8, operators had shut in roughly 1.28 million barrels a day of Gulf of Mexico oil production, about 63% of the region's output, as Hurricane Isaias approached [5].

![Seasonality of refining and retail margins](/assets/charts/gas_06_seasonality.png)

## Testing the asymmetry

The analysis used EIA's weekly U.S. average retail price for regular gasoline, weekly spot prices for conventional gasoline in New York Harbor and on the Gulf Coast, and weekly Brent and WTI spot prices, from January 1992 to October 5, 2026 [6]. The wholesale price is the average of the two spot markets, and spot prices for each week are matched to the following Monday's retail survey. All prices are in cents per gallon.

The test is an asymmetric error correction model, the standard approach in this literature since Borenstein, Cameron and Gilbert [7]. Weekly changes in the retail price are regressed on current and lagged increases and decreases in the wholesale price, entered separately, along with lagged retail changes and the gap between retail and its long run relationship with wholesale. Simulating the model then shows how much of a 10 cent wholesale move reaches the pump week by week.

![Cumulative pass-through](/assets/charts/gas_02_asymmetric_passthrough.png)

The results confirm the pattern. In the first week after a wholesale increase, about 56% of the long run change shows up at the pump, while after a decrease of the same size only 26% does. By week two the figures are 70% and 48%, and the hypothesis that increases and decreases pass through equally in the first two weeks is rejected with a p value of 0.0005.

The asymmetry has not faded with time. On data from 2010 onward, first week pass-through is 65% for increases and 24% for decreases, and the two week gap is wider than in the full sample. Decreases do eventually catch up, reaching roughly 90% after six to eight weeks, so the feathers land, but slowly.

One detail matters for the question of blame. When the same model is run on wholesale gasoline against Brent, the difference between increases and decreases is not statistically significant (p value 0.20). In these data the asymmetry lives mainly between the wholesale rack and the pump, which matches what Borenstein, Cameron and Gilbert reported for the 1980s and early 1990s [7].

## Margins when prices fall

A second way to see the effect is to look at the gap between the pump price and the wholesale price, which includes taxes, distribution and the retail margin. The analysis grouped every week by how much the wholesale price had moved over the previous four weeks.

![Retail margin by wholesale move](/assets/charts/gas_03_margin_by_wholesale_move.png)

When wholesale prices had been flat, the pump price averaged 69 cents above wholesale. When wholesale prices had fallen by more than 20 cents, the gap averaged 94 cents. When they had risen by more than 20 cents, the gap averaged 76 cents, only slightly above the flat case.

The interpretation is straightforward. Retailers absorb some of the cost when wholesale prices rise quickly and recover it, with interest, when wholesale prices fall. Over a full cycle the margin does not look unusual, but its timing is lopsided, and consumers pay the most when the news tells them prices should be falling.

## The psychology behind the pattern

Economic theory offers several explanations, and the evidence suggests more than one is at work. The most cited is consumer search. When prices are rising, drivers notice, shop around and punish stations that are out of line, which forces retailers to keep up with costs. When prices are falling, drivers are relieved by any decline, search less, and stations face little pressure to cut quickly.

Matthew Lewis found support for this "reference price" search model in San Diego station data, showing that margins stay elevated after cost declines in ways that match reduced consumer search [8]. Michael Tappata developed a related theory in which consumers' uncertainty about costs alone can generate rockets and feathers even in competitive markets [9].

Retailers also coordinate without talking. Stations watch each other's signs and tend to settle on focal prices, and a falling cost removes the urgency to be the first to cut. Sam Peltzman documented that asymmetric price adjustment is common across many products, not just gasoline, which suggests that the mechanism is a general feature of how markets with frequent cost changes behave [10].

The most direct evidence of tacit collusion comes from outside the United States. Byrne and de Roos studied retail gasoline in Perth, Australia, and found that the dominant firm used price leadership to teach rivals a coordinated pricing pattern over several years, raising margins without any explicit agreement [11]. Tacit coordination of that kind is generally not illegal, which is part of why it is hard to address.

## The legal side

There is no federal price gouging law for gasoline. The Federal Trade Commission enforces antitrust law and a rule against fraud and manipulation in petroleum markets, but sellers acting independently can legally raise prices as high as the market will bear [12].

States fill part of that gap. According to the National Conference of State Legislatures, 39 states, the District of Columbia and several territories have statutes or regulations that define price gouging during a declared disaster or emergency [13]. Most are triggered only by an emergency declaration, some cap increases at a percentage above pre emergency prices, and most allow sellers to defend higher prices by showing higher costs.

The FTC has investigated gasoline prices repeatedly and has generally found competitive markets rather than conspiracies. After Hurricanes Katrina and Rita, its 2006 report to Congress found no illegal market manipulation, identified 15 firms whose September 2005 prices fit the statutory definition of price gouging, and concluded that regional or local market conditions explained the pricing in nearly all of those cases [14].

The clearest recent case of proven misconduct is narrower. California sued the traders Vitol and SK Energy in 2020, alleging that they manipulated California spot gasoline prices after the 2015 explosion at the Torrance refinery. The companies settled for $50 million without admitting wrongdoing, with final approval in February 2025, and a separate federal class action settled for $13.9 million [15][16]. California has since created a Division of Petroleum Market Oversight under its 2023 law SBX1 2 to monitor refiner margins [15].

## Exploitation, or something else?

The question of whether crises are used as cover for higher margins has to be answered separately for each layer of the stack. At the refining layer, margins clearly expand in a crisis. In 2022, after Russia invaded Ukraine, the analysis finds the gasoline crack spread averaged about 61 cents a gallon, roughly three times its 2019 level.

![The 2022 episode](/assets/charts/gas_04_episode_2022.png)

Wide crack spreads during a supply shock are not by themselves evidence of manipulation. When refining capacity is lost and inventories are low, the price of fuel has to rise relative to crude to ration supply and pull in imports, and refiners that are still running collect that spread. The FTC's 2006 findings and the Dallas Fed's October 2026 analysis both read crisis margins mainly as scarcity rather than markup [14][17].

The retail layer tells a different story, and it is the one consumers feel. The asymmetry in the data sits at the station, and the widest retail margins appear after prices peak, not during the spike. That pattern fits the search and coordination explanations better than outright gouging, and it is legal almost everywhere because it happens outside declared emergencies and does not involve an agreement.

## Why gas is rising in October 2026

The current spike combines an oil shock and a refining shock. A war involving Iran began in February 2026, and the Strait of Hormuz was closed in March, temporarily cutting off about 5 million barrels a day of Persian Gulf refined product exports [17]. Weekly Brent spot prices, which averaged about $71 in February, passed $120 in early April, and the U.S. retail price rose from $3.02 on March 2 to $4.50 by mid May [6].

![The 2026 episode](/assets/charts/gas_05_episode_2026.png)

Prices eased in June and early July and then climbed again with renewed attacks on energy infrastructure. EIA reported that front month Brent futures peaked at $109 on September 15, while spot prices reached as high as $132 around the same time [18]. In the week ending October 2, the Brent spot price averaged about $120, and the October 5 retail price was $4.35 a gallon [6].

The refining side may matter even more for gasoline. The Federal Reserve Bank of Dallas estimates that 6 to 8 million barrels a day of global refining capacity, up to 10% of the world total, has been offline since late spring because of damaged Middle East refineries, Ukrainian drone strikes that cut Russian refining capacity by as much as 60% over the summer, shipping constraints and Chinese export curbs [17]. It notes that crack spreads have exceeded their 2022 levels and that the Strategic Petroleum Reserve held 284 million barrels in September, its lowest since 1982 [17].

The news flow remains two sided. On October 12, Reuters reported Brent near $106 a barrel on attacks on Saudi Arabia and on tankers near Hormuz, partly offset by announced Russian diesel exports, and Goldman Sachs raised its December Brent forecast to $90 [19]. Markets were also weighing possible U.S. and Iran negotiations and a possible suspension of the federal gasoline tax, which the President said he was considering [5].

The data add one observation to that picture. In 2026 the gap between the pump price and wholesale has averaged about 86 cents, below the 108 cents of 2025, while the crack spread has averaged about 76 cents, its highest of any recent year. So far this cycle the squeeze has come through refining rather than retail, which is consistent with the Dallas Fed's reading [17].

![Annual crack spread](/assets/charts/gas_07_crack_by_year.png)

That history also suggests what to watch when prices turn. If crude and wholesale prices fall, the evidence from three decades of data is that retail prices will follow with a lag of several weeks, and retail margins will widen on the way down. Damaged refineries may also keep crack spreads elevated after crude normalizes, as the Dallas Fed expects [17].

![Pump, wholesale and crude prices since 1992](/assets/charts/gas_01_pump_wholesale_crude_history.png)

## Methodology and data

Data are EIA weekly series EMM_EPMR_PTE_NUS_DPG (retail regular, all formulations), EER_EPMRU_PF4_Y35NY_DPG and EER_EPMRU_PF4_RGC_DPG (conventional regular spot, New York Harbor and Gulf Coast), RBRTE (Brent spot) and RWTC (WTI spot), January 1992 to October 5, 2026, 1,705 weekly observations in the models [6]. Prices are nominal. The error correction model uses four lags of positive and negative changes, HAC standard errors, and separate adjustment speeds for positive and negative deviations from the long run relationship. The retail minus wholesale gap includes federal and state taxes, so it overstates the station's margin by a roughly constant amount per gallon.

## References

1. U.S. Energy Information Administration, "Gasoline and Diesel Fuel Update," accessed October 12, 2026. https://www.eia.gov/petroleum/gasdiesel/
2. U.S. Energy Information Administration, "Factors affecting gasoline prices," Energy Explained. https://www.eia.gov/energyexplained/gasoline/factors-affecting-gasoline-prices.php
3. U.S. Environmental Protection Agency, "Gasoline Reid Vapor Pressure." https://www.epa.gov/gasoline-standards/gasoline-reid-vapor-pressure
4. U.S. Environmental Protection Agency, "Renewable Identification Numbers (RINs) under the Renewable Fuel Standard Program." https://www.epa.gov/renewable-fuel-standard-program/renewable-identification-numbers-rins-under-renewable-fuel-standard
5. PFL Petroleum, "The PFL Petroleum Markets Report for October 9, 2026." https://pflpetroleum.com/reports/petroleum-daily-report-10-9-2026/
6. U.S. Energy Information Administration, Petroleum and Other Liquids, weekly price series (downloaded October 12, 2026). https://www.eia.gov/dnav/pet/pet_pri_gnd_dcus_nus_w.htm and https://www.eia.gov/dnav/pet/pet_pri_spt_s1_w.htm
7. Borenstein, S., A. C. Cameron and R. Gilbert (1997), "Do Gasoline Prices Respond Asymmetrically to Crude Oil Price Changes?" Quarterly Journal of Economics 112(1), 305 to 339. https://ideas.repec.org/a/oup/qjecon/v112y1997i1p305-339..html
8. Lewis, M. S. (2011), "Asymmetric Price Adjustment and Consumer Search: An Examination of the Retail Gasoline Market," Journal of Economics and Management Strategy 20(2), 409 to 449.
9. Tappata, M. (2009), "Rockets and Feathers: Understanding Asymmetric Pricing," RAND Journal of Economics 40(4), 673 to 687.
10. Peltzman, S. (2000), "Prices Rise Faster than They Fall," Journal of Political Economy 108(3), 466 to 502.
11. Byrne, D. P. and N. de Roos (2019), "Learning to Coordinate: A Study in Retail Gasoline," American Economic Review 109(2), 591 to 619.
12. Congressional Research Service, "Gasoline Price Increases: Federal and State Authority to Limit 'Price Gouging'," R47072. https://www.congress.gov/crs-product/R47072
13. National Conference of State Legislatures, "Price Gouging State Statutes." https://www.ncsl.org/financial-services/price-gouging-state-statutes
14. Federal Trade Commission, "Investigation of Gasoline Price Manipulation and Post-Katrina Gasoline Price Increases," May 2006. https://www.ftc.gov/news-events/news/press-releases/2006/05/ftc-releases-report-its-investigation-gasoline-price-manipulation-post-katrina-gasoline-price
15. California Department of Justice, "Attorney General Bonta Announces $50 Million Settlement with Vitol and SK," 2024. https://oag.ca.gov/news/press-releases/attorney-general-bonta-announces-50-million-settlement-vitol-and-sk-part-ongoing
16. Courthouse News Service, "California gasoline firms settle price manipulation claims for nearly $14 million," 2025. https://www.courthousenews.com/california-gasoline-firms-settle-price-manipulation-claims-for-nearly-14-million/
17. Thompson, J. and G. Golding, "Refinery outages pumping up fuel prices more than cost of crude oil," Federal Reserve Bank of Dallas, October 8, 2026. https://www.dallasfed.org/research/economics/2026/1008
18. Big Energy News, "Crude Oil Prices and Refinery Margins Rise Through Third Quarter," October 6, 2026 (summarizing EIA). https://bigenergynews.com/2026/10/crude-oil-prices-and-refinery-margins-rise-through-third-quarter/
19. Reuters via Global Banking and Finance Review, "Oil climbs as Mideast conflict and tanker attacks persist," October 12, 2026. https://www.globalbankingandfinance.com/oil-climbs-mideast-conflict-tanker-attacks-persist/
