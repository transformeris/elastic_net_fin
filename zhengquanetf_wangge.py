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

    zhengquan_kline=etf_kline_all['sh510050']
    aa=zhengquan_kline['volume']
    zhengquan_kline.loc[:,'volume_ma10']=aa.rolling(10,center=False).mean().shift()
    zhengquan_kline.loc[:, 'c/o']=(zhengquan_kline['close']/zhengquan_kline['open']).shift()
    zhengquan_kline.loc[:,'hold_signal']=1
    zhengquan_kline.loc[:, 'hold_signal'][zhengquan_kline.loc[:, 'c/o']>1.03] = 0
    zhengquan_kline.loc[:, 'hold_signal'][zhengquan_kline.loc[:, 'c/o'] < 0.98] = 0
    zhengquan_kline.loc[:, 'hold_signal'][zhengquan_kline.loc[:, 'volume_ma10'].shift() > 3*zhengquan_kline.loc[:,'volume_ma10']] = 0

    zhengquan_kline.loc[:,'shouyi']=((zhengquan_kline['close']/zhengquan_kline['open'])-1)*zhengquan_kline.loc[:, 'hold_signal']
    zhengquan_kline.loc[:, 'zhongshouyi']=zhengquan_kline.loc[:,'shouyi'].cumsum()