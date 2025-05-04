import requests
import pandas as pd

### Getting our financial data from the SEC EDGAR API, please consult the following link for reference
### https://www.sec.gov/search-filings/edgar-application-programming-interfaces
### Get the company name from the link: https://www.sec.gov/files/company_tickers.json

### using your email within the header
headers = {'User-Agent': youremailhere@gmail.com}

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

	"""
	Generate a cik code references for companies
	"""
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

	"""
	Create an empty dataframe to add data into
	"""
	def create_dataframe(self) -> pd.DataFrame():
		tup_lst = list()
		for comp in self.comp_lst:
			for quarter in self.quarters:
				tup_lst.append((comp, quarter))
		indexes = pd.MultiIndex.from_tuples(tup_lst, names = ['Company', 'Quarter'])
		df = pd.DataFrame(index = indexes, columns = self.label_lst)
		return df

	"""
	Get all the financial data labels related to the code
	"""
	def get_financial_data_labels(self, code) -> None:
		company_fact = requests.get(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{code}.json',
									headers = headers)
		print(company_fact.json()['facts']['us-gaap'].keys())

	"""
	Load the financial data from SEC fillings into the Dataframe
	and make that the label is up-to-date with the new taxonomy that companies are using within their fillings to the SEC
	"""
	def get_financial_data(self, cik_dict, df):
		for comp in self.comp_lst:
			company_data = requests.get(
				f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_dict[comp]}.json",
				headers=headers
			).json()

			facts = company_data['facts']['us-gaap']

			# Define label fallbacks to account for different taxonomy label
			fallback_labels = {
				'Revenues': [
					'RevenueFromContractWithCustomerExcludingAssessedTax',
					'SalesRevenueNet',
					'SalesRevenueGoodsNet',
					'Revenues',
					'Revenue',
					'RevenueNet',
					'OperatingRevenue',
					'SalesRevenueNet'
				],
				'Assets': [
					'Assets', 'AssetsNet', 'TotalAssets'
				],
				'AssetsCurrent': [
					'AssetsCurrent'
				],
				'Liabilities': [
					'Liabilities', 'TotalLiabilities',
					'LiabilitiesAssumed', 'LiabilitiesAssumed1'
				],
				'LiabilitiesCurrent': [
					'LiabilitiesCurrent'
				],
				'StockholdersEquity': [
					'StockholdersEquity',
					'StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest'
				],
				'NetIncomeLoss': [
					'NetIncomeLoss',
					'ProfitLoss', 'NetIncome',
					'NetIncomeAvailableToCommonStockholdersBasic'
				],
				'LiabilitiesAndStockholdersEquity': [
					'LiabilitiesAndStockholdersEquity'
				]
			}

			for label in self.label_lst:
				fallback_keys = fallback_labels[label]

				# Find the first matching fallback label in facts
				data = None
				for fb_label in fallback_keys:
					if fb_label in facts:
						data = facts[fb_label]['units']['USD']
						break

				if not data:
					print(f"[Warning] No data found for label '{label}' for company {comp}. Tried: {fallback_keys}")
					continue

				for entry in data:
					quarter = entry.get('frame')
					quarter = self.normalize_quarter(quarter)
					if not quarter:
						continue

					# Accept both exact quarter match or match by year prefix
					if quarter in self.quarters:
						try:
							df.loc[(comp, quarter), label] = entry['val']
						except Exception as e:
							print(f"[Error] Could not set value for {comp}, {quarter}, {label}: {e}")
					if quarter in self.years:
						df.loc[(comp, f"{quarter}Q4"), label] = self.calculate_last_quarter(data, entry, quarter)

	# Account for the "I": interim notation in the SEC data
	def normalize_quarter(self, quarter):
		if quarter and quarter.endswith("I"):
			return quarter[:-1]
		return quarter

	"""
	Calculate the data for the last quarter in the fiscal year if company's 
	fillings don't have information for the last quarter
	"""
	def calculate_last_quarter(self, data, entry, year):
		total = entry['val']
		q123_sum = 0
		q_frames = {f"{year}Q1", f"{year}Q2", f"{year}Q3"}
		for other_entry in data:
			quarter = other_entry.get('frame')
			quarter = self.normalize_quarter(quarter)
			if not quarter:
				continue
			if quarter in q_frames:
				q123_sum += other_entry['val']
		return (total - q123_sum)
