import akshare as ak

stock_zh_index_spot_df = ak.stock_zh_index_spot()

for i in stock_zh_index_spot_df['代码']:
    stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol=i)