import yfinance as yf
import numpy as np
from scipy.stats import norm
import pandas as pd

# Define the option parameters
symbol = "AAPL"
expiry = "2023-03-17"
strike_price = 130

# Define the date range for the analysis
start_date = "2021-01-01"
end_date = "2023-03-16"

# Download the historical data for the underlying asset
underlying = yf.download(symbol, start=start_date, end=end_date)

# Calculate the daily returns of the underlying asset
returns = underlying["Adj Close"].pct_change()

# Calculate the implied volatility of the option
option = yf.Ticker(symbol)
option_chain = option.option_chain(expiry)
calls = option_chain.calls
implied_volatility = calls.impliedVolatility[calls.strike == strike_price].values[0]

# Calculate the option price using the Black-Scholes formula
r = 0.01  # risk-free interest rate
t = (pd.Timestamp(expiry) - pd.Timestamp(start_date)).days / 365  # time to expiry in years
d1 = (np.log(underlying["Adj Close"][-1] / strike_price) + (r + implied_volatility**2 / 2) * t) / (implied_volatility * np.sqrt(t))
d2 = d1 - implied_volatility * np.sqrt(t)
option_price = underlying["Adj Close"][-1] * norm.cdf(d1) - strike_price * np.exp(-r * t) * norm.cdf(d2)

# Calculate the option delta using the Black-Scholes formula
delta = norm.cdf(d1)

# Calculate the number of options needed to create a delta-neutral portfolio
option_qty = -delta * len(underlying) / option_price

# Construct the delta-neutral portfolio
portfolio = underlying["Adj Close"] + option_qty * option_price

# Calculate the daily returns of the portfolio
portfolio_returns = portfolio.pct_change()

# Plot the portfolio returns
portfolio_returns.plot()


