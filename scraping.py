import os
import pandas as pd

'''
The data is retrived from: 
https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets
(for the last 8 quarters: from 2023 Q1 to 2024 Q4)
'''

class Scraper:

	def __init__(self, comp_list):
		self.comp_list = comp_list

	'''
	Getting the company code for each company using the txt file
	'''
	def load_code_into_dict(self, quarter, comp_list, filepath, code_dict):
		code_dict[quarter] = {}
		with open(filepath, 'r') as f:
			next(f)
			lines = f.readlines()
			for line in lines:
				line_to_list = line.split('	')
				if line_to_list[2] in comp_list:
					code_dict[quarter][line_to_list[0]] = line_to_list[2]
	'''
	Map the related adsh, tag and version into each quarter code
	'''
	def load_tag_into_dict(self, tag_dict, quarter, filepath):
		tag_dict[quarter] = {}
		with open(filepath, 'r') as f:
			next(f)
			lines = f.readlines()
			for line in lines:
				line_to_list = line.split('	')
				# adsh is the EDGAR accession number
				adsh = line_to_list[1]
				if adsh not in tag_dict[quarter]:
					tag_dict[adsh] = {}
				tag_dict[line_to_list[-4]] = line_to_list[-2]

	'''
	Loading relevant financial data from the txt file into our program
	'''
	def load_financial_data(self, curr_quarter, filepath, code_dict, \
							tag_dict, financial_dict):
		for comp in code_dict.values():
			financial_dict[comp][curr_quarter] = {}
		with open(filepath, 'r') as f:
			next(f)
			lines = f.readlines()
			for line in lines:
				line_to_list = line.split('	')
				adsh = line_to_list[0]
				if adsh in code_dict.keys():
					current_comp = code_dict[adsh]
					tag_name = line_to_list[1]
					# if the adsh and the tag_name match our tag conversion dictionary,
					# convert the tag in tax code to preferred name
					if adsh in tag_dict.keys():
						if tag_name in tag_dict[adsh].keys():
							tag_name = tag_dict[adsh][tag_name]
					financial_dict[current_comp][curr_quarter][tag_name] = line_to_list[-2]

	'''
	Flatten the dictionary before converting it to pandas dataframe
	'''
	def flatten_dict(self, nested_dict) -> {}:
		res = {}
		# Flatten recursively through the dictionary to flatten it
		if isinstance(nested_dict, dict):
			for k in nested_dict:
				flattened_dict = self.flatten_dict(nested_dict[k])
				for key, val in flattened_dict.items():
					key = list(key)
					key.insert(0, k)
					res[tuple(key)] = val
		else:
			res[()] = nested_dict
		return res

	'''
	Converting the nested dictionary into a pandas dataframe
	'''
	def nested_dict_to_dataframe(self, nested_dict) -> pd.DataFrame:
		flat_dict = self.flatten_dict(nested_dict)
		df = pd.DataFrame.from_dict(flat_dict, orient = 'index')
		df.index = pd.MultiIndex.from_tuples(df.index)
		df = df.unstack()
		df.columns = df.columns.map(lambda x: x[1])
		return df

	'''
	Loading our data from the txt files into our program
	'''
	def load_data(self, load_csv) -> pd.DataFrame:
		# setting up the directory
		current_dir = os.path.join(os.getcwd(), 'data') # depend on where you store your file
		company_code_dict = {}
		financial_dict = {}
		quarter_dir = {}
		tag_dict = {}
		# Getting the code for each company and adding the financial file for each quarter
		# to the list
		for quarter in os.listdir(current_dir):
			if quarter != '.DS_Store':
				directory = os.path.join(current_dir, quarter)
				for file in os.listdir(directory):
					# Path to the current file
					file_dir = os.path.join(directory, file)
					if file_dir.endswith('num.txt'):
						quarter_dir[quarter] = file_dir
					elif file_dir.endswith('sub.txt'):
						self.load_code_into_dict(quarter, self.comp_list, file_dir, company_code_dict)
					elif file_dir.endswith('pre.txt'):
						self.load_tag_into_dict(tag_dict, quarter, file_dir)
		for comp in self.comp_list:
			financial_dict[comp] = {}
		for quarter in quarter_dir.keys():
			self.load_financial_data(quarter, quarter_dir[quarter], company_code_dict[quarter], \
									 tag_dict[quarter], financial_dict)
		# Convert the loaded nested dictionary into dataframe
		df = self.nested_dict_to_dataframe(financial_dict)
		df = df.fillna(0)
		if load_csv:
			df.to_csv('Financial_Statement_Data.csv')
		return df