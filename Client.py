from Financial_Ratio import Ratio
from Stock_Analysis import stock_analysis

if __name__ == '__main__':
    comp_list = ['Apple Inc.', 'MICROSOFT CORP', 'NVIDIA CORP', 'Meta Platforms, Inc.',
                 'Tesla, Inc.', 'Alphabet Inc.', 'AMAZON COM INC']
    quote_dict = {'Apple Inc.' : 'AAPL', 'MICROSOFT CORP' : 'MSFT', 'NVIDIA CORP' : 'NVDA',
                'Meta Platforms, Inc.' : 'META', 'Tesla, Inc.' : 'TSLA', 'Alphabet Inc.' : 'GOOG', 'AMAZON COM INC' : 'AMZN'}
    quarters_lst1 = ['CY2023Q1', 'CY2023Q2', 'CY2023Q3', 'CY2023Q4', 'CY2024Q1', 'CY2024Q2', 'CY2024Q3', 'CY2024Q4']
    quarters_lst2 = ['CY2015Q1', 'CY2015Q2', 'CY2015Q3', 'CY2015Q4', 'CY2016Q1', 'CY2016Q2', 'CY2016Q3', 'CY2016Q4']
    instance1 = Ratio(comp_list,
                      ['Assets', 'AssetsCurrent', 'Revenues', 'LiabilitiesAndStockholdersEquity', 'Liabilities',
                       'LiabilitiesCurrent', 'StockholdersEquity', 'NetIncomeLoss'],
                      quarters_lst1)
    instance1.add_data([], None)
    instance1.data_eda()
    instance1.graph_ratios(['ROA', 'ROE', 'Asset Turnover Ratio'], comp_list, "financial_ratios_1_2324.png")
    instance1.graph_ratios(['Current Ratio', 'Debt-to-Equity Ratio'], comp_list, "financial_ratios_2_2324.png")
    # instance2 = Ratio(comp_list,
    #                   ['Assets', 'AssetsCurrent', 'Revenues', 'LiabilitiesAndStockholdersEquity', 'Liabilities',
    #                    'LiabilitiesCurrent', 'StockholdersEquity', 'NetIncomeLoss'],
    #                   quarters_lst2)
    #
    # instance2.add_data(['Revenues', 'Liabilities'], quarters_lst2)
    #
    # instance2.graph_ratios(['ROA', 'ROE', 'Asset Turnover Ratio'], comp_list, "financial_ratios_1_1516.png")
    # instance2.graph_ratios(['Current Ratio', 'Debt-to-Equity Ratio'], comp_list, "financial_ratios_2_1516.png")
    # for comp in comp_list:
    #     stock_analysis(quote_dict[comp])
