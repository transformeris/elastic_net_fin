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
import demjson
from py_mini_racer import py_mini_racer
import pandas as pd
import requests
from akshare.stock.cons import hk_js_decode


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        f.close()


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

etf_list=ak.fund_etf_category_sina(symbol="ETF基金")
res1={}
res2={}
res3={}
res4={}
res5={}
n=1
for i in etf_list['symbol']:
    if i=='sh513200' or i=='sh513150':
        continue
    print(i)
    print(n)
    fund_etf_hist_sina_df = ak.fund_etf_hist_sina(symbol=i)

    fund_etf_hist_sina_df.set_index(['date'], inplace=True)
    # ma12 = fund_em_etf_fund_info_df['单位净值'].rolling(window=5).mean()
    close=fund_etf_hist_sina_df['close']
    open_etf=fund_etf_hist_sina_df['open']
    high=fund_etf_hist_sina_df['high']
    low = fund_etf_hist_sina_df['low']
    volume=fund_etf_hist_sina_df['volume']
    close = pd.to_numeric(close).sort_index()
    open_etf = pd.to_numeric(open_etf).sort_index()
    high = pd.to_numeric(high).sort_index()
    low = pd.to_numeric(low).sort_index()
    volume=pd.to_numeric(volume).sort_index()
    close = close.sort_index()
    open_etf = open_etf.sort_index()
    high = high.sort_index()
    low = low.sort_index()
    volume=volume.sort_index()
    # jinzi_delta=jinzi.shift(20)
    # mtm_20=(jinzi-jinzi_delta)/jinzi
    res1[i]=close
    res2[i]=open_etf
    res3[i]=high
    res4[i]=low
    res5[i]=volume
    n=n+1
save_obj(res1,'etf_close')
save_obj(res2,'etf_open')
save_obj(res3,'etf_high')
save_obj(res4,'etf_low')
save_obj(res5,'etf_volume')
