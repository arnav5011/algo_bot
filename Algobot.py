import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
import pandas as pd
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame

"""API_key = ""
API_secret = ""
base_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(API_key, API_secret, base_URL, api_version= 'v2')

print(api.get_account())
"""

"""Define a trading strategy: If short term average is larger than long term average buy else sell """

"""Test data with yfinance and compare with historical results"""

#Download Data from yfinance for Apple Stocks from 2014 to 2023
data = yf.download("AAPL", start='2014-01-01', end='2023-01-01')\

#Plot Closing Prices
data["Close"].plot(figsize=(10, 6))
plt.title("Apple Stock Price", fontsize=17)
plt.ylabel('Price', fontsize=14)
plt.xlabel('Time', fontsize=14)
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
plt.show()

#Apply Simple Moving Averages
data["SMA_50"] = data['Close'].rolling(window = 50).mean()
data["SMA_200"] = data['Close'].rolling(window = 200).mean()
#Remove empty
data.dropna(subset=['SMA_50', 'SMA_200'], inplace=True)

#Create appropriate signals 1 = buy, -1 = sell
data["Signal"] = 0
data['Signal'] = np.where(data['SMA_50'] > data['SMA_200'], 1, -1)

#Shift position by 1 as you can only buy/sell the next day
data['Position'] = data['Signal'].shift(1)

# Initial capital
initial_capital = 10000.0
shares = 0
cash = initial_capital
portfolio_values = []

# Simulate trading
for i in range(len(data)):
    if data['Position'][i] == 1 and shares == 0:  # Buy signal, not holding stock
        shares = cash / data['Close'][i]  # Buy as many shares as possible
        cash = 0  # All money is used for buying
    elif data['Position'][i] == -1 and shares > 0:  # Sell signal, holding stock
        cash = shares * data['Close'][i]  # Sell all shares
        shares = 0  # No shares left

    # Portfolio value at each time step (cash + value of shares held)
    portfolio_value = cash + shares * data['Close'][i]
    portfolio_values.append(portfolio_value)

# Add portfolio value to the dataframe
data['Portfolio Value'] = portfolio_values

# Print final portfolio value
final_value = data['Portfolio Value'].iloc[-1]
print(f"Final portfolio value: ${final_value:.2f}")

# Performance metrics
total_return = (final_value - initial_capital) / initial_capital * 100
print(f"Total Return: {total_return:.2f}%")

# Plot the closing prices and the SMA signals
plt.figure(figsize=(12, 8))
plt.plot(data['Close'], label='Close Price')
plt.plot(data['SMA_50'], label='50-day SMA', alpha=0.6)
plt.plot(data['SMA_200'], label='200-day SMA', alpha=0.6)
plt.fill_between(data.index, data['SMA_50'], data['SMA_200'], where=data['SMA_50'] > data['SMA_200'], color='green', alpha=0.3, label='Buy Zone')
plt.fill_between(data.index, data['SMA_50'], data['SMA_200'], where=data['SMA_50'] < data['SMA_200'], color='red', alpha=0.3, label='Sell Zone')
plt.legend()
plt.show()



