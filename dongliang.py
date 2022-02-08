import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels import regression
import matplotlib.pyplot as plt
import requests
import re
import bs4
import akshare as ak




import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
etf_fund_daily = ak.fund_em_etf_fund_daily()
code=[]
for i in etf_fund_daily.iterrows():
    if '指数型' in i[1]['类型']:
        code.append(i[1]['基金代码'])

for i in code[0:1]:
    fund_em_etf_fund_info_df = ak.fund_em_etf_fund_info(fund='510050')
    fund_em_etf_fund_info_df.set_index(['净值日期'], inplace=True)
    ma12 = fund_em_etf_fund_info_df['累计净值'].rolling(window=5).mean()
    jinzi=fund_em_etf_fund_info_df['累计净值']
    buy_date=[]
    index=list(fund_em_etf_fund_info_df.index)
    for i in range(1,len(index)):
        try:
            if float(jinzi.loc[index[i]])<ma12.loc[index[i]] and float(jinzi.loc[index[i+1]])>ma12.loc[index[i+1]]:
                buy_date.append(index[i])
        except:
            pass