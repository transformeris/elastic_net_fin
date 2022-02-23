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

def single_stock_tradeback(stock_code,money,trade_pay_rate,start_date,end_date):

    '''

    :param stock_code:  str  股票代码，例：'sz159966'
    :param money: float  初始买入成本，包含手续费
    :param trade_pay_rate: float，手续费费率，【0-1】
    :param start_date: date   回测开始日期，
    :param end_date: date   回测结束日期，
    :return: pandas.Dataframe  包含净值等信息的
    '''
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

if __name__=='__main__':
    money=1

    trade_pay_rate=0.1#0.00015

    money_after_trade=money*(1-trade_pay_rate)

    etf_kline=ak.fund_etf_hist_sina('sz159966')
    etf_kline.set_index(etf_kline['date'],inplace=True)
    start_date=date(2019,12,27)
    end_date=date(2020,1,6)

    zzzz=single_stock_tradeback('sz159966',100,0.3,start_date,end_date)



    etf_hold=etf_kline[start_date:end_date]


    etf_close=etf_hold['close']
    etf_close_shift=etf_close.shift(1)
    etf_delta=(etf_close-etf_close_shift)/etf_close_shift
    etf_delta=etf_delta.drop(start_date)
    etf_hold['incresing_rate']=etf_delta
    etf_hold.loc[start_date, 'incresing_rate'] = (etf_hold.loc[start_date, 'close'] - etf_hold.loc[
        start_date, 'open']) / etf_hold.loc[start_date, 'open']
    etf_hold['日增长倍数']=etf_hold['incresing_rate']+1
    etf_hold['净值倍数']=etf_hold['日增长倍数'].cumprod()
    etf_hold['金额']=etf_hold['净值倍数']*money_after_trade
    etf_hold.loc[start_date,'手续费']=money*trade_pay_rate
    etf_hold.loc[end_date, '手续费'] = etf_hold.loc[end_date,'金额']*trade_pay_rate

    etf_hold.loc[end_date,'卖出金额_手续费后']=etf_hold.loc[end_date,'金额']*(1-trade_pay_rate)





