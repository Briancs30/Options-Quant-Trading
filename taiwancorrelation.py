import yfinance as yf
import pandas as pd

stock = yf.Ticker("2330.TW")#Enter stock ticker
twii = yf.Ticker("^TWII")#Enter Comparison ticker
stock_data = stock.history(period="1y")#1y, 1m, max
twii_data = twii.history(period="1y")

merged_data = pd.merge(stock_data["Close"], twii_data["Close"], left_index=True, right_index=True)
correlation = merged_data.corr().iloc[0,1]
print("Correlation is: {:.2f}".format(correlation))
