import requests
import pandas as pd
import re

### Getting our financial data from the SEC EDGAR API, please consult the following link for reference
### https://www.sec.gov/search-filings/edgar-application-programming-interfaces

### using your email within the header
headers = {'User-Agent': "duchuynguyen1802@gmail.com"}

### Load Financial Data into your program for later usage (plotting and analysis)
### Caution: the Data class is still in development and few columns are empty. Feel free to load relevant real world data
### into NaN values if required
class Data:
	def __init__(self, comp_lst, label_lst, quarters):
		self.comp_lst = comp_lst
		self.label_lst = label_lst
		self.quarters = quarters
		self.years = set()
		for quarter in self.quarters:
			self.years.add(quarter[:-2:])

	# Generate a cik code references for companies
	def get_cik_code(self) -> dict():
		company_ticker = requests.get(
			"https://www.sec.gov/files/company_tickers.json",
			headers=headers
		)
		company_code = pd.DataFrame.from_dict(company_ticker.json(), orient='index')
		company_code['cik_str'] = company_code['cik_str'].astype(str).str.zfill(10)
		cik_dict = {}
		for index, row in company_code.iterrows():
			comp = row['title']
			if comp in self.comp_lst:
				cik_dict[comp] = row['cik_str']
		return cik_dict

	# Create an empty dataframe to add data into
	def create_dataframe(self) -> pd.DataFrame():
		tup_lst = list()
		for comp in self.comp_lst:
			for quarter in self.quarters:
				tup_lst.append((comp, quarter))
		indexes = pd.MultiIndex.from_tuples(tup_lst, names = ['Company', 'Quarter'])
		df = pd.DataFrame(index = indexes, columns = self.label_lst)
		return df

	# Get all the financial data labels related to the code
	def get_financial_data_labels(self, code) -> None:
		company_fact = requests.get(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{code}.json',
									headers = headers)
		print(company_fact.json()['facts']['us-gaap'].keys())

	# Load the financial data from SEC fillings into the Dataframe
	# Make sure that your code is up-to-date with the new taxonomy that companies are using within their fillings to the SEC
	def get_financial_data(self, cik_dict, df):
		for comp in self.comp_lst:
			company_fact_requests = requests.get(
				f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_dict[comp]}.json",
				headers=headers
			)
			for label in self.label_lst:
				data = pd.DataFrame.from_dict(company_fact_requests.json()['facts']['us-gaap'][label])
				# Account for different taxonomy tax within the period
				if label == 'Revenues' and comp == 'MICROSOFT CORP':
					data = pd.DataFrame.from_dict(company_fact_requests.json()['facts']['us-gaap']['RevenueFromContractWithCustomerExcludingAssessedTax'])
				data = pd.DataFrame.from_dict(data['units']['USD'])
				data = data.dropna(axis = 0, subset = ['frame'])
				for index, row in data.iterrows():
					num = row['val']
					if label == 'Revenues' or label == 'NetIncomeLoss':
						quarter = row['frame']
						if quarter in self.quarters or quarter in self.years:
							df.loc[(comp, quarter), label] = num
					else:
						quarter = row['frame'][:-1:]
						if quarter in self.quarters:
							df.loc[(comp, quarter), label] = num
