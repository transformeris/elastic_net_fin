import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels import regression
import matplotlib.pyplot as plt
import requests
import re
import bs4
import akshare as ak
import pickle
import numpy as np


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        f.close()


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)



import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
etf_fund_daily = ak.fund_em_etf_fund_daily()
code=[]
for i in etf_fund_daily.iterrows():
    if '指数型' in i[1]['类型']:
        code.append(i[1]['基金代码'])

n=0
res={}
for i in code[0:3]:
    print(i)
    print(n)
    fund_em_etf_fund_info_df = ak.fund_em_etf_fund_info(fund=i)
    fund_em_etf_fund_info_df.set_index(['净值日期'], inplace=True)
    # ma12 = fund_em_etf_fund_info_df['单位净值'].rolling(window=5).mean()
    jinzi=fund_em_etf_fund_info_df['累计净值']
    jinzi = pd.to_numeric(jinzi)
    jinzi=jinzi.sort_index()
    # jinzi_delta=jinzi.shift(20)
    # mtm_20=(jinzi-jinzi_delta)/jinzi
    res[i]=jinzi
    n=n+1
save_obj(res,'etf_leijijinzi')




