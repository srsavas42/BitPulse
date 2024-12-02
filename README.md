# BitPulse

### Project Description
Using bitcoin pricing and sentiment to predict the price movements of other major crypto currencies.

### Datasets
CoinGecko API for pricing and TokenMetrics API for sentiment analysis

### Project Goals
We plan to create a regression model with the goal of predicting price movements of crypto-curriencies by using Bitcoin as a baseline. This builds off of a hypothesis that crypto currencies are driven primarily by sentiment, with Bitcoin being a major driver of sentiment in alternative major crypto currencies. We plan on using a covariance metric in our initial analysis to help identify if the expected relationships hold, with Mean-Squared Error and PnL to evaluate the efficacy of our final model.

### Data modeling and validation

The data modeling and visualization notebook is best viewed on [Colab](https://colab.research.google.com/drive/1kZKUH2CfUCLwDjMI3K9cJaK5ZgRt-xtB?usp=sharing). Here's the backtesting TL;DR:

- 2019-05-03 to 2019-08-16: Total return of 18.45% and Sharpe ratio of 8.36
- 2019-09-04 to 2023-08-10: Total return of 4357.47% and Sharpe ratio of 5.09
- 2024-03-07 to 2024-11-14: Total return of 69.32% and Sharpe ratio of 4.99

These numbers look pretty great. People can have two reactions: (i) wow, these undergrads hammering out a project a day before the presentation sure are smart, and (ii) these undergrads have a bug in their code. (I know that in practice everyone has(/should have) the latter reaction.) The explanation is simpler: we're trading straddles on an asset class we chose partly _because_ of its volatility. Were cryptocurrencies not famously unstable, we wouldn't _think_ to train a volatility predictor on them. We didn't break the efficient markets hypothesis. 

The other headline result is that incorporating Reddit sentiment doesn't affect prediction [root mean squared error](https://en.wikipedia.org/wiki/Root_mean_square_deviation) _at all_. This isn't surprising considering that during data exploration, we found Reddit sentiment to be overwhelmingly positive, so the noise drowns out whatever signal there is. 
