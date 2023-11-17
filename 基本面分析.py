import akshare as ak
import matplotlib.pyplot as plt
资产负债表 = ak.stock_financial_report_sina(stock="sh600600", symbol="资产负债表")
利润表 = ak.stock_financial_report_sina(stock="sh600600", symbol="利润表")
现金流量表=ak.stock_financial_report_sina(stock="sh600600", symbol="现金流量表")
股价=ak. stock_zh_a_daily(symbol="sh600600")

资产负债表.to_excel('资产负债表.xlsx')
利润表.to_excel('利润表.xlsx')
现金流量表.to_excel('现金流量表.xlsx')
股价.to_excel('股价.xlsx')
# stock_balance_sheet_by_report_em_df = ak.stock_balance_sheet_by_report_em(symbol="SH600600")
z = ak.stock_zh_valuation_baidu(symbol="600600", indicator="市盈率(静)", period="全部")

import pandas as pd




z = ak.stock_zh_valuation_baidu(symbol="600600", indicator="市盈率(TTM)", period="全部")
z.to_excel('市盈率(静).xlsx')


def calculate_eps(pe_ratio_filepath, stock_price_filepath):
    """
    Calculate Earnings Per Share (EPS) based on PE Ratio and Stock Price data.

    Parameters:
    pe_ratio_filepath (str): File path for the PE Ratio data.
    stock_price_filepath (str): File path for the Stock Price data.

    Returns:
    pandas.DataFrame: A DataFrame containing the dates and calculated EPS.
    """
    # Read the PE Ratio and Stock Price data
    pe_ratio_data = pd.read_excel(pe_ratio_filepath)
    stock_price_data = pd.read_excel(stock_price_filepath)

    # Merge the datasets on the 'date' column
    merged_data = pd.merge(pe_ratio_data, stock_price_data, on='date')

    # Calculate the EPS (Earnings Per Share)
    # EPS = Stock Price / PE Ratio
    # Using 'close' as the stock price for calculation
    merged_data['EPS'] = merged_data['close'] / merged_data['value']

    # Select only the date and EPS for the final output
    eps_data = merged_data[['date', 'EPS']]

    return eps_data


# File paths
pe_ratio_filepath = '市盈率(静).xlsx'
stock_price_filepath = '股价.xlsx'

# Calculate EPS and display the results
eps_data = calculate_eps(pe_ratio_filepath, stock_price_filepath)
eps_data.head()  # Display the first few rows of the calculated EPS data
pe_ratio_data = pd.read_excel(pe_ratio_filepath)
stock_price_data = pd.read_excel(stock_price_filepath)
# Merge the datasets on the 'date' column with an outer join to include all dates
merged_data_full = pd.merge(stock_price_data, pe_ratio_data, on='date', how='left')

# Forward fill the PE ratio data
# This will propagate the last valid PE ratio observation forward until a new PE ratio is encountered
merged_data_full['value'] = merged_data_full['value'].ffill()


# 1. 加载数据
# 替换这里的文件路径为您的实际文件路径
pe_ratio_filepath = '市盈率(静).xlsx'
stock_price_filepath = '股价.xlsx'

pe_ratio_data = pd.read_excel(pe_ratio_filepath)
stock_price_data = pd.read_excel(stock_price_filepath)

# 2. 合并数据集
# 假设两个数据集都有一个名为 'date' 的日期列
merged_data = pd.merge(stock_price_data, pe_ratio_data, on='date', how='left')

# 3. 前向填充市盈率数据
# 这会将最近有效的市盈率应用到下一个有效值出现之前的所有日期
merged_data['value'] = merged_data['value'].ffill()
merged_data['EPS'] = merged_data['close'] / merged_data['value']
# 4. 计算PE Band
# 使用252个交易日的窗口来计算滚动的最小值、最大值、平均值和中位数
window_size = 252*3  # 使用252个交易日表示一年
pe_band = merged_data[['date', 'value']].copy()
pe_band['min'] = pe_band['value'].rolling(window=window_size).min()
pe_band['max'] = pe_band['value'].rolling(window=window_size).max()

# 将最大最小值之间分为五等份
for i in range(1, 5):
    pe_band[f'pct_{i*20}'] = pe_band['min'] + i * (pe_band['max'] - pe_band['min']) / 5

# 绘制PE Band图表
plt.figure(figsize=(15, 8))
plt.fill_between(pe_band['date'], pe_band['min'], pe_band['max'], color='grey', alpha=0.3)
for i in range(1, 5):
    plt.plot(pe_band['date'], pe_band[f'pct_{i*20}'], linestyle='--', label=f'{i*20}% Level')

plt.title('PE Band Divided into Five Equal Parts')
plt.xlabel('Date')
plt.ylabel('PE Ratio')
plt.legend()
plt.grid(True)
# plt.show()
merged_data=merged_data.merge(merged_data,eps_data,on='date', how='left')