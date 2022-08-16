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
    zhengquan_kline.loc[datetime.date(2016, 8, 10), 'mairu'] = 1
    zhengquan_kline.loc[datetime.date(2016, 8, 10), 'mairushoushu'] = 1
    zhengquan_kline.loc[datetime.date(2016, 8, 10), 'mairujia'] = zhengquan_kline.loc[datetime.date(2016, 8, 10), 'close']
    zhengquan_kline.loc[datetime.date(2016, 8, 10), 'shouxufeilv'] = 0.001
    zhengquan_kline.loc[datetime.date(2016, 8, 10), 'mairuchengben'] = (1+zhengquan_kline.loc[datetime.date(2016, 8, 10), 'shouxufeilv'])*zhengquan_kline.loc[datetime.date(2016, 8, 10), 'close']*zhengquan_kline.loc[datetime.date(2016, 8, 10), 'mairushoushu']*100
    zhengquan_kline.loc[datetime.date(2016, 8, 10), 'shouxufei'] = zhengquan_kline.loc[datetime.date(2016, 8, 10), 'shouxufeilv']*zhengquan_kline.loc[datetime.date(2016, 8, 10), 'mairushoushu']*100*zhengquan_kline.loc[datetime.date(2016, 8, 10), 'mairujia']



    zhengquan_kline.loc[datetime.date(2016,8,11),'chichang'] = 1
    zhengquan_kline.loc[datetime.date(2016, 8, 12), 'chichang'] = 1
    zhengquan_kline.loc[datetime.date(2016, 8, 15), 'chichang'] = 1
    zhengquan_kline.loc[datetime.date(2016, 8, 17), 'chichang'] = 1
    zhengquan_kline.loc[datetime.date(2016, 8, 18), 'chichang'] = 1
    zhengquan_kline['chichang'][zhengquan_kline['chichang']!=1]=0

    zhengquan_kline.loc[datetime.date(2016, 8, 15), 'maichu'] = 1


    zhengquan_kline['zhangdie']=zhengquan_kline['close'].diff(1)
    zhengquan_kline['rijian_zhangdiefu_close'] = zhengquan_kline['close'].diff(1)/zhengquan_kline['close']



