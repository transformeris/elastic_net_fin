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

# def k_line_huiche():


if __name__=='__main__':

    etf_kline_all=load_obj('etf_all')

    zhengquan_kline=etf_kline_all['sh512880']

    zhengquan_kline.loc[:, 'mairushoushu'] = 0
    zhengquan_kline.loc[:, 'maichushoushu'] = 0

    buy_signal=[datetime.date(2016, 8, 10),datetime.date(2016, 8, 30)]
    buy_time='即时'
    zhengquan_kline.loc[buy_signal, 'mairu'] = 1
    zhengquan_kline.loc[buy_signal, 'mairushoushu'] = 2


    sell_signal=[datetime.date(2016, 8, 15),datetime.date(2016, 9, 9)]
    sell_time='即时'
    zhengquan_kline.loc[sell_signal, 'maichu'] = 1
    zhengquan_kline.loc[sell_signal, 'maichushoushu'] = 1



    zhengquan_kline.loc[:, 'chiyoushoushu_after_shoupan'] = zhengquan_kline['mairushoushu'].cumsum()-zhengquan_kline['maichushoushu'].cumsum()

    zhengquan_kline.loc[:, 'chiyoujine_after_shoupan'] = zhengquan_kline.loc[:, 'chiyoushoushu_after_shoupan']*100*zhengquan_kline.loc[:, 'close']

    zhengquan_kline.loc[:, 'mairushouxufei'] = 0
    zhengquan_kline.loc[buy_signal, 'mairushouxufei']=0.001*zhengquan_kline.loc[buy_signal, 'mairushoushu']*100*zhengquan_kline.loc[buy_signal, 'close']
    zhengquan_kline.loc[:, 'mairuchengben_without_shouxufei'] =0
    zhengquan_kline.loc[buy_signal, 'mairuchengben_without_shouxufei']=zhengquan_kline.loc[buy_signal, 'mairushoushu']*100*zhengquan_kline.loc[buy_signal, 'close']

    zhengquan_kline.loc[:, 'maichuxianjin']=0
    zhengquan_kline.loc[sell_signal, 'maichuxianjin']=zhengquan_kline.loc[sell_signal, 'maichushoushu']*100*zhengquan_kline.loc[sell_signal, 'close']




    zhengquan_kline.loc[:, 'yu_e']=500+zhengquan_kline.loc[:, 'maichuxianjin'].cumsum()-zhengquan_kline.loc[:, 'mairuchengben_without_shouxufei'].cumsum()

    zhengquan_kline.loc[:, 'zhongzhi']=zhengquan_kline.loc[:, 'maichuxianjin'].cumsum()+zhengquan_kline.loc[:, 'chiyoujine_after_shoupan']

    zhengquan_kline.loc[:, 'zhengzhi']=zhengquan_kline.loc[:, 'zhongzhi']-zhengquan_kline.loc[:, 'mairuchengben_without_shouxufei'].cumsum()
    zhengquan_kline.loc[:, 'chichangchengben_per_shou']=(zhengquan_kline.loc[:, 'mairuchengben_without_shouxufei'].cumsum()-zhengquan_kline.loc[:, 'maichuxianjin'].cumsum())/zhengquan_kline.loc[:, 'chiyoushoushu_after_shoupan']
    # zhengquan_kline.loc[buy_signal, 'chichangchengben_per_shou']=zhengquan_kline.loc[buy_signal, 'chiyoujine_after_shoupan']/zhengquan_kline.loc[buy_signal, 'chiyoushoushu_after_shoupan']
    # zhengquan_kline.loc[:, 'xianjinlirun']=zhengquan_kline.loc[:, 'yu_e']+zhengquan_kline.loc[:, 'chiyoujine_after_shoupan']-500
    # zhengquan_kline['jizhunxian']=1
    # zhengquan_kline.loc[datetime.date(2016, 8, 10), 'mairu'] = 1
    # zhengquan_kline.loc[datetime.date(2016, 8, 10), 'mairushoushu'] = 1
    # zhengquan_kline.loc[datetime.date(2016, 8, 10), 'mairujia'] = zhengquan_kline.loc[datetime.date(2016, 8, 10), 'close']
    # zhengquan_kline.loc[datetime.date(2016, 8, 10), 'shouxufeilv'] = 0.001
    # zhengquan_kline.loc[datetime.date(2016, 8, 10), 'mairuchengben'] = (1+zhengquan_kline.loc[datetime.date(2016, 8, 10), 'shouxufeilv'])*zhengquan_kline.loc[datetime.date(2016, 8, 10), 'close']*zhengquan_kline.loc[datetime.date(2016, 8, 10), 'mairushoushu']*100
    # zhengquan_kline.loc[datetime.date(2016, 8, 10), 'shouxufei'] = zhengquan_kline.loc[datetime.date(2016, 8, 10), 'shouxufeilv']*zhengquan_kline.loc[datetime.date(2016, 8, 10), 'mairushoushu']*100*zhengquan_kline.loc[datetime.date(2016, 8, 10), 'mairujia']
    #
    #
    #
    #
    # zhengquan_kline.loc[datetime.date(2016,8,11),'chichang'] = 1
    # zhengquan_kline.loc[datetime.date(2016, 8, 12), 'chichang'] = 1
    # zhengquan_kline.loc[datetime.date(2016, 8, 15), 'chichang'] = 1
    # zhengquan_kline.loc[datetime.date(2016, 8, 17), 'chichang'] = 1
    # zhengquan_kline.loc[datetime.date(2016, 8, 18), 'chichang'] = 1
    # zhengquan_kline['chichang'][zhengquan_kline['chichang']!=1]=0
    #
    #
    #
    # zhengquan_kline.loc[datetime.date(2016, 8, 15), 'maichu'] = 1
    # zhengquan_kline.loc[datetime.date(2016, 8, 15), 'maichujia'] =zhengquan_kline.loc[datetime.date(2016, 8, 15), 'close']
    #
    # zhengquan_kline.loc[datetime.date(2016, 8, 15), 'maichushoushu'] = 1
    #
    # zhengquan_kline['zhangdie']=zhengquan_kline['close'].diff(1)
    # zhengquan_kline['rijian_zhangdiefu_close'] = zhengquan_kline['close'].diff(1)/zhengquan_kline['close']
    #
    # zhengquan_kline['ciyoujine'] = zhengquan_kline['close']*zhengquan_kline['chichang']







