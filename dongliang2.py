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



