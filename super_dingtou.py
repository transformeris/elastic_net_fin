import backtrader as bt
import datetime
import datetime  #
import scipy.stats
import os.path  # 路径管理
import sys  # 获取当前运行脚本的路径 (in argv[0])
import pickle
import numpy as np
import pandas as pd
import matplotlib as plt
import math
def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
def get_values(x):
    return x

if __name__=='__main__':
    etf_kline_all = load_obj('etf_all')
    zhengquan_kline = etf_kline_all['sh512880']
    zhengquan_kline.loc[:, 'trade_date'] = zhengquan_kline.index
    pd.to_datetime(zhengquan_kline.loc[:, 'trade_date'])
    zhengquan_kline.set_index(pd.to_datetime(zhengquan_kline.loc[:, 'trade_date']), inplace=True)

    zhengquan_kline['ma_20']=zhengquan_kline['close'].rolling(60).mean()
    zhengquan_kline['delta_close']=(zhengquan_kline['close']-zhengquan_kline['ma_20'])/zhengquan_kline['ma_20']
    zhengquan_kline['trade_date_shift']=pd.to_datetime(zhengquan_kline['trade_date'].shift(periods=60))
    for i in zhengquan_kline.iterrows():
        delta_close_window=zhengquan_kline.loc[i[1]['trade_date_shift']:i[0],'delta_close']
        zz=scipy.stats.percentileofscore(delta_close_window, zhengquan_kline.loc[i[0],'delta_close'])
        zhengquan_kline.loc[i[0], 'delta_percent']=zz






