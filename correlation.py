import pandas as pd
import yfinance as yf
import requests

def get_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    html = requests.get(url).content
    df = pd.read_html(html, header=0)[0]
    tickers = df['Symbol'].tolist()
    return tickers

def get_stock_correlations(symbol):
    # Retrieve S&P500 company tickers
    sp500_tickers = get_sp500_tickers()

    # Get historical data for the given stock
    stock_data = yf.Ticker(symbol).history(period="1y")

    # Get correlation coefficients for the given stock with each S&P500 company
    correlations = []
    for ticker in sp500_tickers:
        sp500_data = yf.Ticker(ticker).history(period="1y")
        corr = stock_data['Close'].corr(sp500_data['Close'])
        correlations.append((ticker, corr))

    # Create a data frame with the correlations
    df = pd.DataFrame(correlations, columns=['Ticker', 'Correlation'])

    # Rank the correlations in descending order
    df = df.sort_values(by=['Correlation'], ascending=False)

    return df

# Example usage
df = get_stock_correlations("TSLA")
print(df.head())
