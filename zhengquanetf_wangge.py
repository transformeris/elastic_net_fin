import datetime
import seaborn as sns
import tqdm
from hmmlearn import hmm
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import akshare as ak
import statsmodels.api as sm
from copy import deepcopy
import itertools
import seaborn as sns
data_proto=ak.stock_zh_index_daily(symbol="sh000300")
data = ak.stock_zh_index_daily(symbol="sh000300")
close=data['close']
from statsmodels.tsa.stattools import adfuller
import numpy as np
import pandas as pd
import pickle
def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

if __name__=='__main__':

    etf_kline_all=load_obj('etf_all')

    zhengquan_kline=etf_kline_all['sh512880']

    zhengquan_kline['jizhunxian']=1


