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


def single_stock_tradeback(stock_code,etf_kline,money,trade_pay_rate,start_date,end_date):

    '''

    :param stock_code:  str  股票代码，例：'sz159966'
    :param etf_kline:  dict  全部etf基金k线，
    :param money: float  初始买入成本，包含手续费
    :param trade_pay_rate: float，手续费费率，【0-1】
    :param start_date: date   回测开始日期，
    :param end_date: date   回测结束日期，
    :return: pandas.Dataframe  包含净值等信息的
    '''
    if etf_kline==None:
        etf_kline = ak.fund_etf_hist_sina(stock_code)
        etf_kline.set_index(etf_kline['date'], inplace=True)
    etf_hold = etf_kline[start_date:end_date]
    etf_close = etf_hold['close']
    etf_close_shift = etf_close.shift(1)
    etf_delta = (etf_close - etf_close_shift) / etf_close_shift
    etf_delta = etf_delta.drop(start_date)
    etf_hold['incresing_rate'] = etf_delta
    etf_hold.loc[start_date, 'incresing_rate'] = (etf_hold.loc[start_date, 'close'] - etf_hold.loc[
        start_date, 'open']) / etf_hold.loc[start_date, 'open']
    etf_hold['日增长倍数'] = etf_hold['incresing_rate'] + 1
    etf_hold['净值倍数'] = etf_hold['日增长倍数'].cumprod()
    etf_hold['金额'] = etf_hold['净值倍数'] * money_after_trade
    etf_hold.loc[start_date, '手续费'] = money * trade_pay_rate
    etf_hold.loc[end_date, '手续费'] = etf_hold.loc[end_date, '金额'] * trade_pay_rate

    etf_hold.loc[end_date, '卖出金额_手续费后'] = etf_hold.loc[end_date, '金额'] * (1 - trade_pay_rate)
    return etf_hold,etf_hold.loc[end_date, '金额'] * (1 - trade_pay_rate)


def etf_get():
    etf_list = ak.fund_etf_category_sina(symbol="ETF基金")
    res={}
    res1 = {}
    res2 = {}
    res3 = {}
    res4 = {}
    res5 = {}
    n = 1
    for i in etf_list['symbol']:
        if i == 'sh513200' or i == 'sh513150':
            continue
        print(i)
        print(n)
        fund_etf_hist_sina_df = ak.fund_etf_hist_sina(symbol=i)

        fund_etf_hist_sina_df.set_index(['date'], inplace=True)
        # ma12 = fund_em_etf_fund_info_df['单位净值'].rolling(window=5).mean()
        close = fund_etf_hist_sina_df['close']
        open_etf = fund_etf_hist_sina_df['open']
        high = fund_etf_hist_sina_df['high']
        low = fund_etf_hist_sina_df['low']
        volume = fund_etf_hist_sina_df['volume']
        fund_etf_hist_sina_df=pd.to_numeric(fund_etf_hist_sina_df).sort_index()
        close = pd.to_numeric(close).sort_index()
        open_etf = pd.to_numeric(open_etf).sort_index()
        high = pd.to_numeric(high).sort_index()
        low = pd.to_numeric(low).sort_index()
        volume = pd.to_numeric(volume).sort_index()
        fund_etf_hist_sina_df=fund_etf_hist_sina_df.sort_index()

        close = close.sort_index()
        open_etf = open_etf.sort_index()
        high = high.sort_index()
        low = low.sort_index()
        volume = volume.sort_index()
        # jinzi_delta=jinzi.shift(20)
        # mtm_20=(jinzi-jinzi_delta)/jinzi
        res[i]=fund_etf_hist_sina_df
        res1[i] = close
        res2[i] = open_etf
        res3[i] = high
        res4[i] = low
        res5[i] = volume
        n = n + 1
    save_obj(res, 'etf_all')
    # save_obj(res1, 'etf_close')
    # save_obj(res2, 'etf_open')
    # save_obj(res3, 'etf_high')
    # save_obj(res4, 'etf_low')
    # save_obj(res5, 'etf_volume')


if __name__=='__main__':

    money=1

    trade_pay_rate=0.1#0.00015

    money_after_trade=money*(1-trade_pay_rate)

    etf_kline=ak.fund_etf_hist_sina('sz159966')
    etf_kline.set_index(etf_kline['date'],inplace=True)
    start_date=date(2019,12,27)
    end_date=date(2020,1,6)

    etf_close = load_obj('etf_close')
    etf_all = pd.concat(etf_close, axis=1)
    etf_all = etf_all.sort_index()

    delta_etf_all = etf_all.shift(10)
    mtm_20 = (etf_all - delta_etf_all) / etf_all
    mtm_20['stock_mtm_max'] = mtm_20.idxmax(axis=1)

    mtm_20['stock_hold'] = mtm_20['stock_mtm_max'].shift(1)
    mtm_20 = mtm_20.dropna(how='all')
    mtm_20['test']=mtm_20.loc[mtm_20['stock_hold']=='sz159902','sz159902']


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
    for i in zip(mtm_20.index,mtm_20['stock_mtm_max'],mtm_20['stock_hold']):
        if i[1]==i[2]:
            res.append(i[0])
        elif i[1]!=i[2]:
            res.append(i[0])
            res2.append(res)
            res=[]



