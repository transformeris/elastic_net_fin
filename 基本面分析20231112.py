import akshare as ak
import matplotlib.pyplot as plt
import pandas as pd

def calculate_eps(pe_ratio_data, stock_price_data):
    """
    Calculate Earnings Per Share (EPS) based on PE Ratio and Stock Price data.

    Parameters:
    pe_ratio_filepath (str): File path for the PE Ratio data.
    stock_price_filepath (str): File path for the Stock Price data.

    Returns:
    pandas.DataFrame: A DataFrame containing the dates and calculated EPS.
    """

    pe_ratio_data.loc[:, 'date']=pd.to_datetime(pe_ratio_data.loc[:, 'date'])
    stock_price_data.loc[:, 'date'] = pd.to_datetime(stock_price_data.loc[:, 'date'])
    # Merge the datasets on the 'date' column
    merged_data = pd.merge(pe_ratio_data, stock_price_data, on='date')

    # Calculate the EPS (Earnings Per Share)
    # EPS = Stock Price / PE Ratio
    # Using 'close' as the stock price for calculation
    merged_data['EPS'] = merged_data['close'] / merged_data['value']

    # Select only the date and EPS for the final output
    eps_data = merged_data[['date', 'EPS']]

    return eps_data

if __name__=='__main__':
    资产负债表 = ak.stock_financial_report_sina(stock="sh600600", symbol="资产负债表")
    利润表 = ak.stock_financial_report_sina(stock="sh600600", symbol="利润表")
    现金流量表=ak.stock_financial_report_sina(stock="sh600600", symbol="现金流量表")
    股价=ak. stock_zh_a_daily(symbol="sh600600")
    市盈率=ak.stock_zh_valuation_baidu(symbol="600600", indicator="市盈率(TTM)", period="全部")


    # 股价.set_index(pd.to_datetime(股价.loc[:, 'date']), inplace=True)
    # 市盈率.set_index(pd.to_datetime(市盈率.loc[:, 'date']), inplace=True)

    eps=calculate_eps(市盈率,股价)
    merged_data_full = pd.merge(股价, eps, on='date', how='left')
    merged_data_full['eps'] = merged_data_full['EPS'].ffill()
    merged_data_full['pe_ttm']=merged_data_full['close']/merged_data_full['eps']
    # merged_data_full.to_excel('混合数据.xlsx')

    window_size=252*3
    pe_band = merged_data_full[['date', 'pe_ttm']].copy()
    pe_band['min'] = pe_band['pe_ttm'].rolling(window=window_size).min()
    pe_band['max'] = pe_band['pe_ttm'].rolling(window=window_size).max()

    # 将最大最小值之间分为五等份
    for i in range(1, 5):
        pe_band[f'pct_{i * 20}'] = pe_band['min'] + i * (pe_band['max'] - pe_band['min']) / 5


    #
    # # 绘制PE Band图表
    # plt.figure(figsize=(15, 8))
    # plt.fill_between(pe_band['date'], pe_band['min'], pe_band['max'], color='grey', alpha=0.3)
    # for i in range(1, 5):
    #     plt.plot(pe_band['date'], pe_band[f'pct_{i * 20}'], linestyle='--', label=f'{i * 20}% Level')
    #
    # plt.title('PE Band Divided into Five Equal Parts')
    # plt.xlabel('Date')
    # plt.ylabel('PE Ratio')
    # plt.legend()
    # plt.grid(True)
    # plt.show()