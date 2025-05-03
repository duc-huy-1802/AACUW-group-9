# Remember to update your current version of yfinance
# for the code to work properly:
# pip install --upgrade yfinance

# import numpy as np
# import pandas as pd
# import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf
# from yahoofinancials import YahooFinancials

"""
Compute the Relative Strength Index for the current stock ticker
within the two periods
"""
def compute_rsi(series, period):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def stock_analysis(ticker):
    df_2 = yf.download(ticker,
                          start='2025-01-05',
                          end='2025-05-01',
                          progress=False,
    )
    df_1= yf.download(ticker,
                          start='2024-09-05',
                          end='2024-11-12',
                          progress=False,
    )
    df_1['RSI'] = compute_rsi(df_1['Close'], 20)
    df_2['RSI'] = compute_rsi(df_2['Close'], 20)
    plt = sma_analysis(ticker, df_1, df_2)
    plt = ema_analysis(ticker, plt, df_1, df_2)
    plt = rsi_analysis(ticker, plt, df_1, df_2)

"""
Compute and graph the Simple Moving Average for the current stock ticker
within the two periods
"""
def sma_analysis(ticker, df_1, df_2):
    sma_period_1 = 20  # You can change this to any period you want
    sma_period_2 = 20  # You can change this to any period you want

    df_1['SMA'] = df_1['Close'].rolling(window=sma_period_1).mean()
    df_2['SMA'] = df_2['Close'].rolling(window=sma_period_2).mean()

    # Plotting
    plt.figure(figsize=(14, 7))

    # Plot for the first time period
    plt.subplot(2, 1, 1)
    plt.plot(df_1['Close'], label=f'{ticker} Close Price', color='blue')
    plt.plot(df_1['SMA'], label=f'SMA {sma_period_1} Days', color='orange')
    plt.title(f'{ticker} Close Price and SMA (2024-09-05 to 2024-11-12)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()

    # Plot for the second time period
    plt.subplot(2, 1, 2)
    plt.plot(df_2['Close'], label=f'{ticker} Close Price', color='blue')
    plt.plot(df_2['SMA'], label=f'SMA {sma_period_2} Days', color='orange')
    plt.title(f'{ticker} Close Price and SMA (2025-01-05 to 2025-05-01)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()

    plt.tight_layout()

    plt.savefig(f"{ticker}_sma_analysis.png")
    return plt

"""
Compute and graph the Exponential Moving Average for the current stock ticker
within the two periods
"""
def ema_analysis(ticker, plt, df_1, df_2):
    ema_period_1 = 20  # You can change this to any period you want
    ema_period_2 = 20  # You can change this to any period you want

    df_1['EMA'] = df_1['Close'].ewm(span=ema_period_1, adjust=False).mean()
    df_2['EMA'] = df_2['Close'].ewm(span=ema_period_2, adjust=False).mean()

    # Plotting
    plt.figure(figsize=(14, 7))

    # Plot for the first time period
    plt.subplot(2, 1, 1)
    plt.plot(df_1['Close'], label=f'{ticker} Close Price', color='blue')
    plt.plot(df_1['EMA'], label=f'EMA {ema_period_1} Days', color='orange')
    plt.title(f'{ticker} Close Price and EMA (2024-09-05 to 2024-11-12)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()

    # Plot for the second time period
    plt.subplot(2, 1, 2)
    plt.plot(df_2['Close'], label=f'{ticker} Close Price', color='blue')
    plt.plot(df_2['EMA'], label=f'EMA {ema_period_2} Days', color='orange')
    plt.title(f'{ticker} Close Price and EMA (2025-01-05 to 2025-05-01)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()

    plt.tight_layout()

    plt.savefig(f"{ticker}_ema_analysis.png")
    plt.show()
    return plt

"""
Graph the Relative Strength Index for the current stock ticker
within the two periods
"""
def rsi_analysis(ticker, plt, df1, df2):

    plt.figure(figsize=(14, 7))
    plt.subplot(2, 1, 1)
    plt.plot(df1.index, df1['RSI'], label='RSI')
    plt.axhline(70, color='red', linestyle='--', label='Overbought (70)')
    plt.axhline(30, color='green', linestyle='--', label='Oversold (30)')
    plt.title(f"{ticker} - 20 - Day RSI")
    plt.xlabel('Date')
    plt.ylabel('RSI')
    min_rsi = df1['RSI'].min()
    plt.fill_between(df1.index, min_rsi, df1['RSI'], alpha = 0.7)
    plt.legend()
    plt.grid()

    plt.subplot(2, 1, 1)
    plt.figure(figsize=(14, 7))
    plt.plot(df2.index, df2['RSI'], label='RSI')
    plt.axhline(70, color='red', linestyle='--', label='Overbought (70)')
    plt.axhline(30, color='green', linestyle='--', label='Oversold (30)')
    plt.title(f"{ticker} - 20-Day RSI")
    plt.xlabel('Date')
    plt.ylabel('RSI')
    min_rsi = df2['RSI'].min()
    plt.fill_between(df2.index, min_rsi, df2['RSI'], alpha=0.7)
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.savefig(f"{ticker}_rsi_analysis.png")
    plt.show()

    return plt



