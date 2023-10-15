import akshare as ak

stock_financial_report_sina_df = ak.stock_financial_report_sina(stock="sh600600", symbol="资产负债表")
stock_balance_sheet_by_report_em_df = ak.stock_balance_sheet_by_report_em(symbol="SH600600")
print(stock_financial_report_sina_df)
a=list(stock_balance_sheet_by_report_em_df.columns)
b=list(stock_financial_report_sina_df.columns)