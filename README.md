TITLE: Statistical Arbitrage & Cointegration Terminal

A Python-based quantitative trading engine that identifies, mathematically verifies, and signals market-neutral pair trading opportunities.

Instead of relying on basic price ratios or black-box machine learning libraries, this terminal builds Ordinary Least Squares (OLS) Linear Regression from scratch to calculate dynamic hedge ratios, and utilizes the Augmented Dickey-Fuller (ADF) Test to rigorously prove mean-reversion.

THE CORE PHILOSOPHY: Correlation vs. Cointegration
Many retail traders confuse correlation with cointegration. To understand the difference, imagine a drunk man walking down the street with his dog on a leash.

Correlation (The Two Drunk Men): Imagine two drunk men walking down the same street, heading toward the same bar. They are moving in the same general direction (high correlation). But because they are wandering randomly, one might walk faster or stumble down a side street. Eventually, they can drift miles apart. If you bet your money that they will stay exactly 5 feet apart forever, you will lose.

Cointegration (The Man and the Dog): Now imagine the drunk man and his dog. They are both wandering erratically all over the sidewalk. But because the dog is tied to the man by a physical leash, the distance between them is mathematically capped. The dog might chase a squirrel and stretch the leash out, but eventually, the leash will always yank the dog back toward the man.

This engine is designed to find that leash, measure its exact length, and signal exactly when it is stretched to its absolute limit so we can trade the "snap-back".

THE 4-STAGE ARCHITECTURE

Engine 1: The Correlation Terminal (Vector Space)
Before finding the leash, we must find stocks moving in the same general direction.

Transforms raw daily prices into percentage returns (geometric vectors).

Mean-centers the data to strip away broad market drift.

Calculates the Pearson Correlation Coefficient using the Dot Product and L2 Norms (Euclidean distance) to prove structural directional similarity.

Engine 2: The Cointegration Terminal (OLS Regression)
Proves the distance between the assets is capped and calculates the exact Hedge Ratio.

Built from Scratch: Calculates raw Covariance and Variance to find the slope of the regression line (Beta) without relying on libraries like scikit-learn.

The Hedge Ratio: Calculates the exact "exchange rate" of volatility to ensure the portfolio remains perfectly market-neutral.

The Spread Vector: Adjusts for the structural price gap (Alpha) and generates a synthetic, tradeable asset: The Spread.

Engine 3: The Gatekeeper (Stationarity Testing)
A financial polygraph test that physically blocks trades if the math is weak.

Uses the Augmented Dickey-Fuller (ADF) Test on the Spread vector.

Strict 5% Rule: Rejects any pair with a P-Value of 0.05 or higher. It demands 95% mathematical certainty that the spread is stationary (not a random walk).

Compares the ADF Statistic to critical thresholds to measure the actual tensile strength of the "Bungee Cord."

Engine 4: The Trigger (Execution Signals)
Converts raw Rupee spread data into actionable trading triggers.

Calculates a rolling 21-day average and volatility window to adapt to recent market regimes.

Generates a Z-Score to measure standard deviations from the mean.

If the Gatekeeper approves the pair, it flashes OVERBOUGHT or OVERSOLD when the Z-score breaches algorithmic thresholds.

VISUAL OUTPUTS
The terminal automatically generates three distinct matplotlib visualizations to verify the math:

Normalized Growth Chart: Re-scales both assets to a baseline of 100 to visualize pure percentage growth over 10 years.

The Spread Chart: Plots the historical Rupee divergence, adjusted for Alpha, with the ADF test results embedded directly into the UI.

Z-Score Action Zones: Maps the current spread against standard deviation bands for precision trade entries.

DEPENDENCIES
To run this engine locally, you will need the following Python libraries:

yfinance (Data ingestion)

pandas (Dataframe manipulation)

numpy (Linear algebra & vector math)

matplotlib (Data visualization)

statsmodels (ADF Stationarity testing)