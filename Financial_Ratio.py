import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# from scraping import Scraper
from Financial_Data_From_SEC import Data
from Stock_data import Stock

class Ratio:
	def  __init__(self, comp_list, label_lst, quarters):
		self.quarters = quarters
		self.label_lst = label_lst
		dat = Data(comp_list, label_lst, quarters)
		self.df = dat.create_dataframe()
		cik_dict = dat.get_cik_code()
		dat.get_financial_data(cik_dict, self.df)
		# stock = Stock([])

	'''
	Give back the current dataframe
	'''
	def get_df(self):
		return self.df

	'''
	Give back the current list of quarters and companies
	'''
	def get_quarters(self):
		return self.quarters

	'''
	Do explanatory data analysis for our current dataframe
	'''
	def data_eda(self):
		pd.options.display.max_columns = None
		print('Our current financial data tags are:', self.df.columns)
		indexes = self.df.index.tolist()
		print(f"Our current companies and quarters are: {indexes}")
		print(self.df.isna().sum())

	'''
	Calculate the required ratio for the current company in the current quarter
	'''
	# Need to work on the stock prices again
	def calculate_ratio(self, ratio, comp, quarter):
		if ratio == 'ROA' or ratio == 'ROE':
			num = self.df.loc[(comp, quarter), 'Assets'] if ratio == 'ROA' else self.df.loc[(comp, quarter), 'StockholdersEquity']
			income = self.df.loc[(comp, quarter), 'NetIncomeLoss']
			return income / num * 100
		elif ratio == 'Current Ratio':
			return (self.df.loc[(comp, quarter), 'AssetsCurrent'] /
					self.df.loc[(comp, quarter), 'LiabilitiesCurrent'])
		elif ratio == 'Debt-to-Equity Ratio':
			return self.df.loc[(comp, quarter), 'Liabilities'] / self.df.loc[(comp, quarter), 'StockholdersEquity']
		elif ratio == 'Asset Turnover Ratio':
			return (self.df.loc[(comp, quarter), 'Revenues'] / self.df.loc[(comp, quarter), 'Assets']) * 100
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
	Graph the required ratios for relevant list of companies
	'''
	def graph_ratios(self, ratio_list, comp_list, name):
		row = 0
		col = 0
		df = pd.DataFrame(columns=['Ratio', 'Comp', 'Quarter', 'Value'])
		for ratio in ratio_list:
			for comp in comp_list:
				for quarter in self.quarters:
					x_val = quarter[-4::]
					df = pd.concat([df, pd.DataFrame.from_dict([{'Ratio' : ratio, 'Comp' : comp, 'Quarter' : x_val,
							 'Value' : self.calculate_ratio(ratio, comp, quarter)}])], ignore_index=True)
		ax = sns.relplot(data = df, kind = 'line', facet_kws={"sharey": False},
					x = 'Quarter', y = 'Value', hue = 'Comp', col = 'Ratio', col_wrap = 3, height = 5, aspect = 1.5)
		# sns.move_legend(ax, "center right")
		sns.move_legend(
			ax,
			loc = 'center right',
			bbox_to_anchor = (1, 0.5),
			frameon = True,
			title = 'Company'
		)
		ax.fig.subplots_adjust(top=0.9, right=0.85)
		plt.savefig(name)
		plt.close()
		plt.show()

### Feel free to adjust this to match your company and required quarters
instance = Ratio(['NVIDIA CORP', 'MICROSOFT CORP', 'Tesla, Inc.'],
				 ['Assets', 'AssetsCurrent', 'Revenues', 'LiabilitiesAndStockholdersEquity', 'Liabilities',
				 'LiabilitiesCurrent', 'StockholdersEquity', 'NetIncomeLoss'],
		 		 ['CY2023Q1', 'CY2023Q2', 'CY2023Q3', 'CY2023Q4', 'CY2024Q1', 'CY2024Q2', 'CY2024Q3', 'CY2024Q4']
				)
instance.data_eda()
instance.graph_ratios(['ROA', 'ROE', 'Asset Turnover Ratio'],
		 ['NVIDIA CORP', 'MICROSOFT CORP', 'Tesla, Inc.'], "plot1.png")
instance.graph_ratios(['Current Ratio', 'Debt-to-Equity Ratio'],
		 ['NVIDIA CORP', 'MICROSOFT CORP', 'Tesla, Inc.'], "plot2.png")

