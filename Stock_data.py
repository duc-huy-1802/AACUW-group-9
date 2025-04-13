#install the latest version of yahoo finance within your terminal for better usage:
#pip install yfinance --upgrade --no-cache-dir

# Yahoo Finance documentations: https://yfinance-python.org/reference/yfinance.analysis.html#
import yfinance as yf
import pandas as pd

# Getting the stock data from yfinance API for a single stock over a specific period
class Stock:
	def __init__(self, comp, range, df):
		self.comp = comp
		self.range = range

	def get_stock_data(self, df):
		tick = yf.Ticker(self.comp)
		income_data = tick.history(start = self.range[0], end = self.range[1], interval = '3mo')
		stock_price = income_data['Open']
		df['Stock'] = stock_price