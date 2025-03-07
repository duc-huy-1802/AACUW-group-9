import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from scraping import Scraper

class Ratio:

	def  __init__(self, comp_list, generate_csv):
		scraper = Scraper(comp_list)
		self.df = scraper.load_data(generate_csv)
		self.quarters_list = self.df.index.tolist()
		self.color_dict = {'TESLA, INC.' : 'r',
						   'NVIDIA CORP' : 'g'}

	'''
	Give back the current dataframe
	'''
	def get_df(self):
		return self.df

	'''
	Give back the current list of quarters and companies
	'''
	def get_quarters(self):
		return self.quarters_list

	'''
	Do explanatory data analysis for our current dataframe
	'''
	def data_eda(self):
		pd.options.display.max_columns = None
		print('Our current financial data tags are:', self.df.columns)
		indexes = self.df.index.tolist()
		print(f"Our current companies and quarters are: {indexes}")
		print(self.df.isna().sum())

	# Need to work on the stock prices again
	def calculate_ratio(self, ratio, quarter):
		if ratio == 'ROA' or ratio == 'ROE':
			average = (pd.to_numeric(self.df['Assets'][quarter]) if ratio == 'ROA' \
				else (pd.to_numeric(self.df['LiabilitiesAndStockholdersEquity'][quarter])
					  - pd.to_numeric(self.df['Liabilities'][quarter])))
			income = pd.to_numeric(self.df['NetIncomeLoss'][quarter])
			return income / average * 100
		elif ratio == 'Current Ratio':
			return (pd.to_numeric(self.df['AssetsCurrent'][quarter]) /
					pd.to_numeric(self.df['LiabilitiesCurrent'][quarter]))
		elif ratio == 'Debt-to-Equity Ratio':
			return (pd.to_numeric(self.df['Liabilities'][quarter]) \
					/ (pd.to_numeric(self.df['LiabilitiesAndStockholdersEquity'][quarter])
					  - pd.to_numeric(self.df['Liabilities'][quarter])))
		elif ratio == 'Asset Turnover Ratio':
			return (pd.to_numeric(self.df['Revenues'][quarter]) \
				/ pd.to_numeric(self.df['Assets'][quarter]) * 100)
		elif ratio == 'P/E':
			'''
			at the end of the reporting day
			stock_price =
			return stock_price / pd.to_numeric(self.df['EarningsPerShareBasic'][quarter])
			'''
			pass
		else:
			return -1

	'''
	Graph the ratio that has been calculated
	'''
	def plot_single_ratio(self, ratio, comp_list):
		color_list = []
		for comp in comp_list:
			data = []
			curr_quarters_list = []
			for quarter in self.quarters_list:
				if quarter[0] == comp:
					curr_quarters_list.append(quarter[1][-4:len(quarter[1]):1])
					data.append(self.calculate_ratio(ratio, quarter))
			y = np.array(data)
			plt.plot(curr_quarters_list, y, self.color_dict[comp], linewidth=2)
			color_list.append(self.color_dict[comp])
		plt.legend(comp_list, color_list)

	def graph_ratios(self, ratio_list, comp_list):
		count = 1
		plt.figure(figsize=(15, 10))
		for ratio in ratio_list:
			plt.subplot(2, 3, count)
			self.plot_single_ratio(ratio, comp_list)
			plt.title(f"{ratio} for 2 years")
			plt.xlabel('Year and Quarter')
			plt.ylabel(ratio)
			count += 1
		plt.tight_layout()
		plt.show()

instance = Ratio(['TESLA, INC.', 'NVIDIA CORP'], True)
instance.graph_ratios(['ROA', 'ROE', 'Asset Turnover Ratio', 'Current Ratio', 'Debt-to-Equity Ratio'],
					  ['TESLA, INC.', 'NVIDIA CORP'])
