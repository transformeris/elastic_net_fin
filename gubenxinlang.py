import requests
import re
import bs4
import pandas as pd
import time
import pandas as pd



url = f"https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructure/stockid/600004.phtml"
r = requests.get(url)
temp_df = pd.read_html(r.text)[13].iloc[:, :5]

temp_df.columns = [*range(5)]
big_df = pd.DataFrame()
need_range = temp_df[temp_df.iloc[:, 0].str.find("截至日期") == 0].index.tolist() + [len(temp_df)]
for i in range(len(need_range) - 1):
    truncated_df = temp_df.iloc[need_range[i]: need_range[i + 1], :]
    truncated_df = truncated_df.dropna(how="all")
    temp_truncated = truncated_df.iloc[5:, :]
    temp_truncated.reset_index(inplace=True, drop=True)
    concat_df = pd.concat([temp_truncated, truncated_df.iloc[0, :], truncated_df.iloc[1, :], truncated_df.iloc[2, :],
                           truncated_df.iloc[3, :], truncated_df.iloc[4, :]], axis=1)
    concat_df.columns = concat_df.iloc[0, :]
    concat_df = concat_df.iloc[1:, :]