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


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

etf_all=load_obj('etf_danweijinzi')
etf_all=pd.concat(etf_all, axis=1)
etf_all=etf_all.sort_index()

delta_etf_all=etf_all.shift(20)
mtm_20=(etf_all-delta_etf_all)/etf_all
mtm_20['max']=mtm_20.idxmax(axis=1)
mtm_20['max_shift_1']=mtm_20['max'].shift(1)
mtm_20_dropna=mtm_20.dropna(how='all')
mtm_20_dropna=mtm_20_dropna.drop('2005-03-09')
mtm_20_dropna=mtm_20_dropna.drop('2010-09-19')
mtm_20_dropna=mtm_20_dropna.drop('2010-09-20')
mtm_20_dropna=mtm_20_dropna.drop('2010-10-27')
mtm_20_dropna=mtm_20_dropna.drop('2010-10-28')
mtm_20_dropna=mtm_20_dropna.drop('2011-01-30')
mtm_20_dropna=mtm_20_dropna.drop('2011-01-31')
mtm_20_dropna=mtm_20_dropna.drop('2020-01-19')
mtm_20_dropna=mtm_20_dropna.drop('2020-01-20')

for i in mtm_20_dropna.iterrows():
    mtm_20_dropna.loc[i[0],'test']=etf_all.loc[i[0],mtm_20_dropna.loc[i[0],'max']]

money=1
flag=0
res={}
for i in zip(mtm_20_dropna.index,mtm_20_dropna['max_shift_1'],mtm_20_dropna['test']):
    leiji=etf_all.loc[i[0],i[1]]
    if i[1]!=flag:
       fene=money/leiji
    elif i[1]==flag:
        fene=fene
        money=leiji*fene
    flag=i[1]
    res[i]=money

