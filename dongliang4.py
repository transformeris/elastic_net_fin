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
from datetime import datetime
def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

etf_close=load_obj('etf_close')
etf_all=pd.concat(etf_close, axis=1)
etf_all=etf_all.sort_index()





delta_etf_all=etf_all.shift(10)
mtm_20=(etf_all-delta_etf_all)/etf_all
mtm_20['stock_mtm_max']=mtm_20.idxmax(axis=1)

etf_open=load_obj('etf_open')
etf_open_pandas=pd.concat(etf_open, axis=1)


mtm_20['stock_hold']=mtm_20['stock_mtm_max'].shift(1)
mtm_20=mtm_20.dropna(how='all')
# mtm_20=mtm_20.drop(datetime.strptime('2005-03-23', '%Y-%m-%d'),axis=0)
# mtm_20=mtm_20.drop(datetime.strptime('2013-8-30', '%Y-%m-%d'),axis=0)
# mtm_20=mtm_20.drop(datetime.strptime('2005-3-09', '%Y-%m-%d'),axis=0)

for i in mtm_20.iterrows():
    if mtm_20.loc[i[0],'stock_mtm_max']!=mtm_20.loc[i[0],'stock_hold']:
        mtm_20.loc[i[0], 'hold_change']=1
    elif mtm_20.loc[i[0],'stock_mtm_max']==mtm_20.loc[i[0],'stock_hold']:
        mtm_20.loc[i[0], 'hold_change'] = 0
    try:
        mtm_20.loc[i[0],'buy_price']=etf_open[i[1]['stock_hold']][i[0]]
        mtm_20.loc[i[0], 'sell_price'] = etf_close[i[1]['stock_hold']][i[0]]
    except:
        pass

flag=0
for i,j in zip(mtm_20.index,mtm_20['stock_hold']):
    if j!=flag:
        mtm_20.loc[i,'buy_sign']=1
    elif j==flag:
        mtm_20.loc[i,'buy_sign']=0
    flag=j





res={}
money=1
for i in mtm_20.iterrows():
    if i[1]['buy_sign']==1:
        mtm_20.loc[i[0],'fenne']=money/i[1]['buy_price']
        fene=money/i[1]['buy_price']
    if i[1]['hold_change']==1:
        mtm_20.loc[i[0],'money']=i[1]['sell_price']*money/i[1]['buy_price']
        money=i[1]['sell_price']*money/i[1]['buy_price']
    fene