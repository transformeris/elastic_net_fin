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

etf_close=load_obj('etf_close')
etf_all=pd.concat(etf_close, axis=1)
etf_all=etf_all.sort_index()




delta_etf_all=etf_all.shift(20)
mtm_20=(etf_all-delta_etf_all)/etf_all
mtm_20['stock_mtm_max']=mtm_20.idxmax(axis=1)

etf_open=load_obj('etf_open')
etf_open_pandas=pd.concat(etf_open, axis=1)


mtm_20['stock_hold']=mtm_20['stock_mtm_max'].shift(1)

for i in mtm_20.iterrows():


