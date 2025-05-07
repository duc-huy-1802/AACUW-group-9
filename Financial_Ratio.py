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
		self.dat = Data(comp_list, label_lst, quarters)
		self.df = self.dat.create_dataframe()
		cik_dict = self.dat.get_cik_code()
		self.dat.get_financial_data(cik_dict, self.df)

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
		print("The number of missing entries per labels are:")
		print(self.df.isna().sum())

	'''
	Calculate the required ratio for the current company in the current quarter
	'''
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
			return (self.df.loc[(comp, quarter), 'Revenues'] / self.df.loc[(comp, quarter), 'Assets'])
		else:
			return -1

	"""
	Load ratio values into dataframe based on the ratio list and companies list
	"""

	def load_ratio(self, ratio_list, comp_list):
		df = pd.DataFrame(columns=['Ratio', 'Comp', 'Quarter', 'Value'])
		for ratio in ratio_list:
			for comp in comp_list:
				for quarter in self.quarters:
					x_val = quarter[-4::]
					df = pd.concat([df, pd.DataFrame.from_dict([{'Ratio': ratio, 'Comp': comp, 'Quarter': x_val,
																 'Value': self.calculate_ratio(ratio, comp, quarter)}])],
								   							   ignore_index=True)
		return df

	'''
	Graph the required ratios for relevant list of companies
	'''
	def graph_ratios(self, ratio_list, comp_list, name):
		df = self.load_ratio(ratio_list, comp_list)
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

	"""
	Accommodate for the gaps in 2015-2016 fillings that the program can not
	parse from SEC fillings. Load from additional csv files instead
	"""
	def add_data(self, label_lst, quarters_lst):
		for label in label_lst:
			curr_df = pd.read_csv(f"additional_data/magnificent7_2015_2016_quarterly_{label}.csv")
			for index, row in curr_df.iterrows():
				for quarter in quarters_lst:
					self.df.loc[(row['Company'], quarter), label] = row[quarter]
		aapl_df = pd.read_csv("additional_data/alphabet_2015Q12_additional.csv")
		for index, row in aapl_df.iterrows():
			for quarter in ['CY2015Q1', 'CY2015Q2']:
				self.df.loc[('Alphabet Inc.', quarter), row['Metric']] = row[quarter]
		if 'CY2023' in self.dat.get_years():
			nvidia_df = pd.read_csv("additional_data/nvidia_2023_2024_quarterly_revenue.csv", index_col=0)
			for quarter in nvidia_df.columns:
				self.df.loc[('NVIDIA CORP', quarter), 'Revenues'] = nvidia_df.loc['Revenues', quarter]