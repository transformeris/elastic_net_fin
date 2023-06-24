import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels import regression
import matplotlib.pyplot as plt
import requests
import re
import bs4
import akshare as ak

def cal_rsrs(data2, data1, N=16):
    """
    计算data2中标的所在日期的RSRS斜率指标和拟合优度
    """
    data11 = data1[data1['sec_code'].isin(data2['sec_code'])].reset_index()
    loc = data11[data11['tradeday'].isin(data2['tradeday'])].index.tolist()
    if loc[0] >= N:
        x = sm.add_constant(data11['low_slice'][(loc[0] - N):loc[0]]).astype('float64')
        y = data11['high_slice'][(loc[0] - N):loc[0]].astype('float64')
        est = sm.OLS(y, x)
        res = est.fit()
        params = res.params.low_slice
        r_squared = res.rsquared
    else:
        params = None
        r_squared = None
    data2['rsrs'] = params
    data2['r_squared'] = r_squared
    return data2


def rsrs(data, N=16):
    """
    由日频数据计算RSRS斜率指标和拟合优度
    """
    data = data.dropna()
    data['tradeday'] = pd.to_datetime(data['tradeday'], format='%Y/%m/%d %H:%M:%S')
    data.sort_values(by=['sec_code', 'tradeday'], inplace=True)
    data1 = data.copy()
    data1 = data1.groupby(['sec_code', 'tradeday']).apply(lambda x, data1=data1, N=N: cal_rsrs(x, data1, N))
    print("RSRS斜率指标和拟合优度已计算")

    return data1


def cal_rsrs_std(data2, data1, M=300, N=16):
    """
    计算data2中标的所在日期的RSRS标准分
    """
    data11 = data1[data1['sec_code'].isin(data2['sec_code'])].reset_index()
    loc = data11[data11['tradeday'].isin(data2['tradeday'])].index.tolist()
    # print(loc[0])
    rsrs = data2['rsrs']
    if loc[0] < M + N:
        rsrs_std = None
    else:
        rsrs_mean = np.mean(data11['rsrs'][(loc[0] - M):loc[0]])
        rsrs_s = np.std(data11['rsrs'][(loc[0] - M):loc[0]])
        rsrs_std = (rsrs - rsrs_mean) / rsrs_s
    data2['rsrs_std'] = rsrs_std
    return data2


def rsrs_std(data1, M=300, N=16):
    """
    由RSRS斜率计算RSRS标准分
    """
    data2 = data1.groupby(['sec_code', 'tradeday']).apply(lambda x, data1=data1, M=M, N=N: cal_rsrs_std(x, data1, M, N))
    print("RSRS标准分已计算")
    return data2


def rsrs_std_cor(data2):
    """
    由RSRS标准分计算RSRS修正标准分
    """
    data2['rsrs_std_cor'] = data2['r_squared'] * data2['rsrs_std']
    print('RSRS修正标准分已计算')
    return data2


def rsrs_std_cor_right(data2):
    """
    由RSRS修正标准分计算RSRS右偏修正标准分
    """
    data2['rsrs_std_cor_right'] = data2['rsrs_std_cor'] * data2['rsrs']
    print('RSRS右偏修正标准分已计算')
    return data2


def rsrs_std_cor_right_mean(data2, ndays=5):
    """
    计算RSRS右偏修正标准分的ndays均线
    """
    data2['rsrs_std_cor_right_mean']=data2.groupby('sec_code')['rsrs_std_cor_right'].rolling(window=ndays).mean()

    # data2['rsrs_std_cor_right_mean'] = data2.groupby('sec_code')['rsrs_std_cor_right'].apply(pd.rolling_mean, ndays)
    print('RSRS右偏修正标准分均线已计算')
    return data2


def get_rsrs(data, N=16, M=300, ndays=5):
    """
    根据日频数据计算RSRS相关指标
    data 数据，包括：标的代码sec_code,交易日tradeday,最高价high_slice、最低价low_slice、收盘价close_slice
    N，回归时间窗口，默认取16，不足16赋值为None
    M，标准分计算窗口，默认取300，不足300赋值为None
    """
    data1 = rsrs(data, N)
    data2 = rsrs_std(data1, M, N)
    data2 = rsrs_std_cor(data2)
    data2 = rsrs_std_cor_right(data2)
    data2 = rsrs_std_cor_right_mean(data2, ndays)
    return data2


def get_signal(data2, S):
    """
    根据RSRS指标和阈值S判断是否有交易信号（最简单的情况）,trade_dir为0代表买入，为1代表卖出，为-1代表无信号
    """
    data3 = data2.copy()
    data3.loc[:,'trade_dir']=-1
    data3.loc[(data3['rsrs_std_cor_right'] > S) & (data3['trade_dir'] == -1), 'trade_dir'] = 0
    data3.loc[(data3['rsrs_std_cor_right'] > S) & (data3['trade_dir'] == 1), 'trade_dir'] = -1

    data3.loc[(data3['rsrs_std_cor_right'] < -S) & (data3['trade_dir'] == -1), 'trade_dir'] = 1
    data3.loc[(data3['rsrs_std_cor_right'] < -S) & (data3['trade_dir'] == 0), 'trade_dir'] = -1
    # data3.drop(['rsrs','r_squared','rsrs_std','rsrs_std_cor','rsrs_std_cor_right'], axis = 1, inplace = True)
    return data3


def RSRS(data, N=16, M=300, S=0.7, ndays=5):
    """
    根据日频数据计算RSRS相关指标，并判断交易信号，更新trade_dir,删除中间变量
    """
    data2 = get_rsrs(data, N, M, ndays)
    data3 = get_signal(data2, S)
    return data3


if __name__=='__main__':
    stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol="sh000300")
    stock_zh_index_daily_df['tradeday']=stock_zh_index_daily_df.index
    stock_zh_index_daily_df['high_slice']=stock_zh_index_daily_df['high']
    stock_zh_index_daily_df['low_slice'] = stock_zh_index_daily_df['low']
    stock_zh_index_daily_df['close_slice'] = stock_zh_index_daily_df['close']
    stock_zh_index_daily_df['sec_code'] = 'sz399552'
    rsrs_=RSRS(stock_zh_index_daily_df, N=16, M=300, S=0.7, ndays=5)
    data2 = get_rsrs(stock_zh_index_daily_df, N=16, M=300,  ndays=5)
    data2.loc[:,'trade_dir']=-1
    S=0.7
    data2.loc[(data2['rsrs_std_cor_right'] > S) & (data2['trade_dir'] == -1), 'trade_dir'] = 0

    data = ak.stock_zh_a_daily(symbol='sh000001', start_date='20100101', end_date='20201231')

    ak.stock_us_daily()



