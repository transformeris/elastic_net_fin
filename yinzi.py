import akshare as ak
stock_financial_report_sina_df = ak.stock_financial_report_sina(stock="600004", symbol="现金流量表")
print(stock_financial_report_sina_df)
zz=stock_financial_report_sina_df

import akshare as ak
stock_financial_abstract_df = ak.stock_financial_abstract(stock="600004")
print(stock_financial_abstract_df)

import akshare as ak
stock_financial_analysis_indicator_df = ak.stock_financial_analysis_indicator(stock="600004")
print(stock_financial_analysis_indicator_df)
zzz=stock_financial_analysis_indicator_df

import akshare as ak
stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="600004", start_date="20170301", end_date='20210907', adjust="")
print(stock_zh_a_hist_df)

import akshare as ak
stock_a_indicator_df = ak.stock_a_lg_indicator(stock="600004")
print(stock_a_indicator_df)


# for i in range(0,stock_financial_analysis_indicator_df):
#     stock_financial_analysis_indicator_df.loc[i]['BP']=stock_financial_analysis_indicator_df.loc[i]['日期']

# for i in stock_zh_a_hist_df.index:
#     print(i)
#     zzz[zzz.index<i]
stock_zh_a_hist_df.set_index(['日期'],inplace=True)

for i in range(0,len(stock_financial_analysis_indicator_df)-1):
    stock_zh_a_hist_df.loc[stock_financial_analysis_indicator_df.index[i+1]:stock_financial_analysis_indicator_df.index[i],'BP']=stock_zh_a_hist_df[stock_financial_analysis_indicator_df.index[i+1]:stock_financial_analysis_indicator_df.index[i]]['收盘']/float(stock_financial_analysis_indicator_df.loc[stock_financial_analysis_indicator_df.index[i+1],'每股净资产_调整后(元)'])
zzzzzz=stock_a_indicator_df = ak.stock_a_lg_indicator(stock="600004")

# for i in range(0,len(stock_financial_analysis_indicator_df)-1):
#     date_change=stock_zh_a_hist_df[stock_financial_analysis_indicator_df.index[i+1]:stock_financial_analysis_indicator_df.index[i]]
#     print(date_change)
#     stock_zh_a_hist_df[date_change]['BP']=stock_zh_a_hist_df[date_change]['收盘']/stock_financial_analysis_indicator_df.loc[i+1]['每股净资产_调整后（元）']