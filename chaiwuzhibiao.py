import akshare as ak

stock_balance_sheet_by_report_em_df = ak.stock_balance_sheet_by_report_em(symbol="SH600519")
print(stock_balance_sheet_by_report_em_df)
zz=stock_balance_sheet_by_report_em_df[1:3]
zz_json=zz.to_json()

stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="600519", period="daily", start_date="20170301", end_date='20230907', adjust="")
print(stock_zh_a_hist_df)
zzzzz=stock_balance_sheet_by_report_em_df.columns()