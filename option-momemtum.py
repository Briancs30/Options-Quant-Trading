import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def optionMomemtumMACD(sym):
    # Set the ticker symbol, expiration date, and option symbol
    option_symbol = sym

    # Get the historical data for the specific option
    option_history = yf.Ticker(option_symbol).history(period="max")
    print(option_symbol)
    print(option_history)
    # Define the short-term and long-term moving averages
    short_ma = 12
    long_ma = 26

    # Calculate the MACD and signal lines
    option_history['ma_short'] = option_history['Close'].rolling(window=short_ma).mean()
    option_history['ma_long'] = option_history['Close'].rolling(window=long_ma).mean()
    option_history['macd'] = option_history['ma_short'] - option_history['ma_long']
    option_history['signal'] = option_history['macd'].rolling(window=9).mean()

    # Define the buy and sell signals
    option_history['buy_signal'] = option_history['macd'] > option_history['signal']
    option_history['sell_signal'] = option_history['macd'] < option_history['signal']

    # Initialize the position and P&L variables
    position = 0
    pnl = [0] * len(option_history)
    num = 1
    count = 0

    # Loop through the trading period
    for i in range(len(option_history)):
        date = option_history.index[i]
        # Check for buy signal
        if option_history.loc[date, 'buy_signal'] and position == 0:
            position = num
            count += 1
            buy_price = option_history.loc[date, 'Close']
            print(f"Buying at {buy_price}")
        # Check for sell signal
        elif option_history.loc[date, 'sell_signal'] and position == num:
            position = 0
            count += 1
            sell_price = option_history.loc[date, 'Close']
            pnl[i] = (sell_price - buy_price) * num
            print(f"Selling at {sell_price}")
        # No signal
        else:
            pnl[i] = 0
    

    # Calculate the cumulative P&L
    cum_pnl = pd.Series(pnl).cumsum()


    # Calculate the daily P&L
    daily_pnl = cum_pnl.diff()

    # Calculate the Sharpe ratio
    sharpe_ratio = (daily_pnl.mean() / daily_pnl.std()) * np.sqrt(252)

    # Plot the price chart with buy and sell signals
    plt.plot(option_history['Close'])
    plt.scatter(option_history.index[option_history['buy_signal']], option_history['Close'][option_history['buy_signal']], color='green', marker='^')
    plt.scatter(option_history.index[option_history['sell_signal']], option_history['Close'][option_history['sell_signal']], color='red', marker='v')
    plt.show()

    # Plot the P&L chart
    plt.plot(option_history.index, cum_pnl)
    plt.xlabel('Trading Date')
    plt.ylabel('Cumulative P&L')
    plt.title('Cumulative Profit and Loss (P&L) Chart')
    plt.show()

    print(f"End Position: {position}")
    print(f"Numbers of Trades: {count}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")



def optionBollinger(sym):
    # Set the option symbol
    option_symbol = sym

    # Get the historical data for the specific option
    option_history = yf.Ticker(option_symbol).history(period="max")

    # Define the period and standard deviation for Bollinger Bands
    period = 20
    std_dev = 2

    # Calculate the Bollinger Bands
    option_history['MA'] = option_history['Close'].rolling(window=period).mean()
    option_history['upper_band'] = option_history['MA'] + std_dev * option_history['Close'].rolling(window=period).std()
    option_history['lower_band'] = option_history['MA'] - std_dev * option_history['Close'].rolling(window=period).std()

    # Define the buy and sell signals
    option_history['buy_signal'] = (option_history['Close'] < option_history['lower_band']).astype(int)
    option_history['sell_signal'] = (option_history['Close'] > option_history['upper_band']).astype(int)

    # Initialize the position and P&L variables
    position = 0
    pnl = [0] * len(option_history)
    num = 1
    count = 0
    # Loop through the trading period
    for i in range(len(option_history)):
        date = option_history.index[i]
        # Check for buy signal
        if option_history.loc[date, 'buy_signal'] and position == 0:
            position = num
            count += 1
            buy_price = option_history.loc[date, 'Close']
            print(f"Buying at {buy_price}")
        # Check for sell signal
        elif option_history.loc[date, 'sell_signal'] and position == num:
            position = 0
            count += 1
            sell_price = option_history.loc[date, 'Close']
            pnl[i] = (sell_price - buy_price) * num
            print(f"Selling at {sell_price}")
        # No signal
        else:
            pnl[i] = 0

    # Calculate the cumulative P&L
    cum_pnl = pd.Series(pnl).cumsum()

    # Calculate the daily P&L
    daily_pnl = cum_pnl.diff()

    # Calculate the Sharpe ratio
    sharpe_ratio = (daily_pnl.mean() / daily_pnl.std()) * np.sqrt(252)
    print(f"End Position: {position}")
    print(f"Number of Trades: {count}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Cumulative P&L: {cum_pnl.iloc[-1]:.2f}")
    


    '''
    # Plot the Bollinger Bands chart
    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(option_history.index, option_history['Close'], label='Option Close Price')
    ax.plot(option_history.index, option_history['MA'], label='Moving Average')
    ax.plot(option_history.index, option_history['upper_band'], label='Upper Band')
    ax.plot(option_history.index, option_history['lower_band'], label='Lower Band')
    ax.fill_between(option_history.index, option_history['upper_band'], option_history['lower_band'], alpha=0.1)
    ax.set_xlabel('Trading Date')
    ax.set_ylabel('Option Price ($)')
    ax.set_title('Bollinger Bands')
    ax.legend()
    plt.show()
    '''

    # Plot the Bollinger Bands and P&L charts separately
    fig, axs = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

    # Plot the Bollinger Bands chart
    axs[0].plot(option_history.index, option_history['Close'], label='Option Close Price')
    axs[0].plot(option_history.index, option_history['MA'], label='Moving Average')
    axs[0].plot(option_history.index, option_history['upper_band'], label='Upper Band')
    axs[0].plot(option_history.index, option_history['lower_band'], label='Lower Band')
    axs[0].fill_between(option_history.index, option_history['upper_band'], option_history['lower_band'], alpha=0.1)
    axs[0].set_ylabel('Option Price ($)')
    axs[0].set_title('Bollinger Bands')

    # Plot the P&L chart
    axs[1].plot(option_history.index, cum_pnl, label='Cumulative P&L')
    axs[1].set_xlabel('Trading Date')
    axs[1].set_ylabel('P&L ($)')
    
    # Format the axes
    for ax in axs:
        ax.legend()
        ax.grid(True)

    plt.show()

#optionBollinger("AAPL230616C00160000") #Sharpe Ratio: 0.06; Cumulative P&L: 0.71
optionBollinger("AAPL230616P00160000")  #Sharpe Ratio: 0.61; Cumulative P&L: 10.12

#optionMomemtumMACD("AAPL", "2023-03-17", "AAPL230317C00125000", "call")
#optionMomemtumMACD( "AAPL", "2023-03-17", "AAPL230317C00185000", "call")
#optionMomemtumMACD( "SPY", "2023-06-30", "SPY230630C00350000", "call")
#optionMomemtumMACD( "TSLA", "2023-06-16", "SPY230616P00400000", "put") #SR = 0.92, Trades: 21, Profits


#optionMomemtumMACD( "AAPL230317C00300000") #in the market call 1 year; SR = -0.47; profit = -71.3

#optionMomemtumMACD( "AAPL", "2023-03-17", "TSLA230317P00300000", "put") #in the market call 1 year; SR = -0.47; profit = -71.3