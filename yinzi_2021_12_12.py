import akshare as ak
stock_financial_report_sina_df = ak.stock_financial_report_sina(stock="600004", symbol="现金流量表")

stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="600004", start_date="20170301", end_date='20211218', adjust="")

stock_a_indicator_df = ak.stock_a_lg_indicator(stock="600004")

stock_financial_analysis_indicator_df = ak.stock_financial_analysis_indicator(stock="600004")

##算总市值##

ak.stock_zh_a_gdhs()