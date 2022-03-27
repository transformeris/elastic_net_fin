import akshare as ak
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
from datetime import date


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def date_mtm():
    money=1

    trade_pay_rate=0.1#0.00015

    money_after_trade=money*(1-trade_pay_rate)

    etf_kline=ak.fund_etf_hist_sina('sz159966')
    etf_kline.set_index(etf_kline['date'],inplace=True)
    start_date=date(2019,12,27)
    end_date=date(2020,1,6)
    etf_close={}
    stock_index = load_obj('stock_index')
    for i,j in stock_index.items():
        etf_close[i]=j['close']


    # etf_close = load_obj('etf_close')
    # res= {}
    # for i,j in etf_close.items():
    #     if i=='sh510300' or i=='sz159999':
    #         print('fuck')
    #         #or i=='sh510300' or i=='sh510500' or i=='sz159903' or i=='sz159915':
    #         res[i]=j
    #
    # etf_close=res
    etf_all = pd.concat(etf_close, axis=1)
    etf_all = etf_all.sort_index()

    delta_etf_all = etf_all.shift(20)
    mtm_20 = (etf_all - delta_etf_all) / etf_all
    mtm_20['stock_mtm_max'] = mtm_20.idxmax(axis=1)

    mtm_20['stock_hold'] = mtm_20['stock_mtm_max'].shift(1)
    mtm_20 = mtm_20.dropna(how='all')
    # mtm_20['test']=mtm_20.loc[mtm_20['stock_hold']=='sz159902','sz159902']


    for i in mtm_20.iterrows():
        if mtm_20.loc[i[0], 'stock_mtm_max'] != mtm_20.loc[i[0], 'stock_hold']:
            mtm_20.loc[i[0], 'hold_change'] = 1
        elif mtm_20.loc[i[0], 'stock_mtm_max'] == mtm_20.loc[i[0], 'stock_hold']:
            mtm_20.loc[i[0], 'hold_change'] = 0
        try:

            mtm_20.loc[i[0], 'sell_price'] = etf_close[i[1]['stock_hold']][i[0]]
        except:
            pass

    mtm_20=mtm_20[mtm_20['sell_price'].notnull()]

    res=[]
    res2=[]
    res3={}
    for i in zip(mtm_20.index,mtm_20['stock_mtm_max'],mtm_20['stock_hold']):
        if i[1]==i[2]:

            res.append(i[0])
        elif i[1]!=i[2]:
            res.append(i[0])
            res2.append(res)
            res.append(i[2])
            # res3[i[2]]=res
            res=[]
    return res2

def single_stock_tradeback(stock_code,etf_kline,money,trade_pay_rate,start_date,end_date):

    '''
    以start_date的开盘价买入，以end_date的收盘价卖出
    :param stock_code:  str  股票代码，例：'sz159966'
    :param etf_kline:  dict  全部etf基金k线，
    :param money: float  初始买入成本，包含手续费
    :param trade_pay_rate: float，手续费费率，【0-1】
    :param start_date: date   回测开始日期，
    :param end_date: date   回测结束日期，
    :return: pandas.Dataframe  包含净值等信息的
    '''
    etf_kline_stock=etf_kline[stock_code]
    etf_hold = etf_kline_stock[start_date:end_date]
    etf_close = etf_hold['close']
    etf_close_shift = etf_close.shift(1)
    etf_delta = (etf_close - etf_close_shift) / etf_close_shift
    etf_delta = etf_delta.drop(start_date)
    etf_hold['incresing_rate'] = etf_delta
    etf_hold.loc[start_date, 'incresing_rate'] = (etf_hold.loc[start_date, 'close'] - etf_hold.loc[
        start_date, 'open']) / etf_hold.loc[start_date, 'open']
    etf_hold['日增长倍数'] = etf_hold['incresing_rate'] + 1
    etf_hold['净值倍数'] = etf_hold['日增长倍数'].cumprod()
    money_after_trade=money* (1 - trade_pay_rate)
    etf_hold['金额'] = etf_hold['净值倍数'] * money_after_trade
    etf_hold.loc[start_date, '手续费'] = money * trade_pay_rate
    etf_hold.loc[end_date, '手续费'] = etf_hold.loc[end_date, '金额'] * trade_pay_rate

    etf_hold.loc[end_date, '卖出金额_手续费后'] = etf_hold.loc[end_date, '金额'] * (1 - trade_pay_rate)
    return etf_hold,etf_hold.loc[end_date, '金额'] * (1 - trade_pay_rate)



# stock_zh_index_spot_df = ak.stock_zh_index_spot()
# res={}
# for i in stock_zh_index_spot_df['代码']:
#     try:
#         stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol=i)
#         res[i]=stock_zh_index_daily_df
#     except:
#         pass
# save_obj(res,'stock_index')

def huiche():
    res = date_mtm()

    etf_all = load_obj('stock_index')

    qian = []
    quxian = 1

    for i in res:
        stock = i[-1]
        date_range = i[0:-1]
        start = min(date_range)
        end = max(date_range)

        # etf_kline=etf_all[stock]
        jinzi, quxian = single_stock_tradeback(stock, etf_all, quxian, 0.0001, start, end)
        aa = jinzi['金额']
        qian.append(aa)


    aaa = pd.concat(qian)
    plt.plot(aaa)

    plt.show()


if __name__=='__main__':

    etf_close={}
    stock_index = load_obj('stock_index')
    for i,j in stock_index.items():
        etf_close[i]=j['close']

    etf_all = pd.concat(etf_close, axis=1)
    etf_all = etf_all.sort_index()

    delta_etf_all = etf_all.shift(16)
    mtm_20 = (etf_all - delta_etf_all) / etf_all
    mtm_20['mtm_max'] = mtm_20.max(axis=1)



    mtm_20['percent_90']=mtm_20.quantile(q=0.9,axis=1)
    mtm_20['stock_mtm_max'] = mtm_20.idxmax(axis=1)



    mtm_20['stock_hold'] = mtm_20['stock_mtm_max'].shift(1)
    mtm_20['date']=mtm_20.index
    mtm_20['date_shift']=mtm_20['date'].shift(-1)
    mtm_20 = mtm_20.dropna(how='all')
    # mtm_20['test']=mtm_20.loc[mtm_20['stock_hold']=='sz159902','sz159902']

    for i in mtm_20.iterrows():
        if mtm_20.loc[i[0], 'stock_mtm_max'] != mtm_20.loc[i[0], 'stock_hold']:
            mtm_20.loc[i[0], 'hold_change'] = 1
        elif mtm_20.loc[i[0], 'stock_mtm_max'] == mtm_20.loc[i[0], 'stock_hold']:
            mtm_20.loc[i[0], 'hold_change'] = 0
        try:

            mtm_20.loc[i[0], 'sell_price'] = etf_close[i[1]['stock_hold']][i[0]]
        except:
            pass

    mtm_20=mtm_20[mtm_20['sell_price'].notnull()]

    # res=[]
    # res2=[]
    # res3={}
    # for i in zip(mtm_20.index,mtm_20['stock_mtm_max'],mtm_20['stock_hold']):
    #     if i[1]==i[2]:
    #
    #         res.append(i[0])
    #     elif i[1]!=i[2]:
    #         res.append(i[0])
    #         res2.append(res)
    #         res.append(i[2])
    #         # res3[i[2]]=res
    #         res=[]



    res=[]
    res2=[]
    res3={}
    for i in zip(mtm_20.index,mtm_20['stock_mtm_max'],mtm_20['stock_hold']):
        if i[1]==i[2]:

            res.append(i[0])
        elif i[1]!=i[2]:
            res.append(i[0])
            res2.append(res)
            res.append(i[2])
            # res3[i[2]]=res
            res=[]


    res = res2
    mtm_20_proto=mtm_20
    mtm_20=mtm_20[mtm_20['percent_90']>=0]

    useful_date=list(mtm_20.index)
    # res=[res[0]]
    test=[]
    test1=[]
    flag = 1
    for i in res:
        for ii in i:
            if ii in useful_date:
                flag=1
                test.append(ii)
            elif ii not in useful_date and flag==1:
                test.append(i[-1])
                test1.append(test)
                test = []
                flag=0
                # if flag == 0:
                #     continue
            elif type(ii)==str:
                continue


    res=test1[1:]

    etf_all = load_obj('stock_index')

    qian = []
    quxian = 1

    for i in res:
        stock = i[-1]
        date_range = i[0:-1]
        start = min(date_range)
        end = max(date_range)

        # etf_kline=etf_all[stock]
        jinzi, quxian = single_stock_tradeback(stock, etf_all, quxian, 0, start, end)
        aa = jinzi['金额']
        qian.append(aa)


    aaa = pd.concat(qian)
    plt.plot(aaa)
    plt.plot()
    plt.show()

