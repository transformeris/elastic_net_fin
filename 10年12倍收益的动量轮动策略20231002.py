import backtrader as bt
import akshare as ak
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt


import collections

import backtrader as bt
from backtrader import Order, Position
import json
import warnings
import docx
import backtrader as bt
import backtrader.analyzers as btanalyzers
import backtrader.feeds as btfeeds
import backtrader.strategies as btstrats


import math

def annualized_return(total_return, years):
    """
    计算年化收益率

    :param total_return: 投资的总收益率
    :param years: 投资的年数
    :return: 年化收益率
    """
    return math.pow(1 + total_return, 1 / years) - 1







def rename_columns(datas):
    res= {}
    for j,i in datas.items():

        i.rename(columns={
            '日期': 'date', '收盘': 'close', '开盘': 'open', '最高': 'high',
            '最低': 'low', '成交量': 'volume', '成交额': 'amount',
            '振幅': 'amplitude', '涨跌幅': 'pct_change'
        }, inplace=True)
        i.set_index(pd.to_datetime(i.loc[:, 'date']), inplace=True)
        res[j]=i
    return res



def process_data(etfs: dict):
    # ... 省略前面的部分 ...

    # 仓位调节
    stock_percent = holding_df.iloc[:, :len(etfs)].clip(lower=0, inplace=False).div(holding_df.iloc[:, :len(etfs)].clip(lower=0, inplace=False).sum(axis=1), axis=0).shift(1)

    # 删除包含 NaN 的行
    etf_open = etf_open.dropna()
    etf_close = etf_close.dropna()
    stock_percent = stock_percent.dropna()

    # 根据日期索引进行对齐
    data_frames = [etf_open, etf_close, stock_percent]
    for i, df in enumerate(data_frames):
        for j, other_df in enumerate(data_frames):
            if i != j:
                df, _ = df.align(other_df, axis=0)
                df = df.dropna()
        data_frames[i] = df

    return data_frames

def process_data(etf_open,etf_close,stock_percent):
    # ... 省略前面的部分 ...

    # 仓位调节

    # 删除包含 NaN 的行
    etf_open = etf_open.dropna()
    etf_close = etf_close.dropna()
    stock_percent = stock_percent.dropna()

    # 根据日期索引进行对齐
    df_merged = pd.concat([etf_open, etf_close, stock_percent], join='inner', axis=1)

    # 删除 NaN 值
    df_merged = df_merged.dropna()

    # 分离数据给 etf_open, etf_close 和 stock_percent
    etf_open = df_merged[etf_open.columns]
    etf_close = df_merged[etf_close.columns]
    stock_percent = df_merged[stock_percent.columns]

    return etf_open, etf_close, stock_percent


if __name__ == '__main__':

    cyb_etf = ak.fund_etf_hist_em(symbol='159915', adjust='qfq')
    hs300_etf= ak.fund_etf_hist_em(symbol='510300', adjust='qfq')
    ndaq_etf= ak.fund_etf_hist_em(symbol='513100', adjust='qfq')
    gold_etf= ak.fund_etf_hist_em(symbol='518880', adjust='qfq')

    stock_collection={1:cyb_etf,2:hs300_etf,3:ndaq_etf,4:gold_etf}
    stock_name={1:'cyb_etf',2:'hs300_etf',3:'ndaq_etf',4:'gold_etf'}
    stock_list=list(stock_collection.values())
    etfs=rename_columns(stock_collection)


    # 假设cyb_etf、hs300_etf、ndaq_etf、gold_etf是四个pandas dataframe表格


    # 计算二十日收益率
    for etf in etfs.values():
        etf['return_20'] = etf['close'].pct_change(periods=21)

    # 合并四个表格
    holding_df = pd.concat(etfs, axis=1, join='inner')
    holding_df=holding_df.filter(regex='return_20')
    holding_df.columns=stock_name.values()
    etf_number=[0,1,2,3]
    holding_df['max_return_20_etf_name']=holding_df.idxmax(axis=1)
    holding_df['max_return_20_etf_number']=holding_df['max_return_20_etf_name'].replace(['cyb_etf','hs300_etf','ndaq_etf','gold_etf'],etf_number)
    etf_open = pd.concat(etfs, axis=1, join='inner').filter(regex='open')
    etf_open.columns=stock_name.values()
    etf_close = pd.concat(etfs, axis=1, join='inner').filter(regex='close')
    etf_close.columns = stock_name.values()
    # 仓位调节

    stock_percent=holding_df.iloc[:,0:4].clip(lower=0,inplace=False).dropna().div(holding_df.iloc[:,0:4].clip(lower=0,inplace=False).dropna().sum(axis=1),axis=0).shift(1).fillna(0)

    stock_percent






    start_date = max(hs300_etf.index[0], cyb_etf.index[0], ndaq_etf.index[0], gold_etf.index[0])
    end_date = datetime.datetime(2023, 12, 31)

    import pandas as pd
    import numpy as np

    # 读取数据
    # weights = pd.read_csv('weights.csv')
    # weights['date'] = pd.to_datetime(weights['date'])
    # weights.set_index('date', inplace=True)
    #
    # open_prices = pd.read_csv('open_prices.csv')
    # open_prices['date'] = pd.to_datetime(open_prices['date'])
    # open_prices.set_index('date', inplace=True)
    #
    # close_prices = pd.read_csv('close_prices.csv')
    # close_prices['date'] = pd.to_datetime(close_prices['date'])
    # close_prices.set_index('date', inplace=True)

    # 初始现金
    cash = 10000

    # 交易费用和滑点
    transaction_cost = 0.00  # 0.1%
    slippage = 0.000  # 0.01%

    # 初始化一个新的DataFrame来存储每日的ETF份额
    etf_shares = np.empty((2456,4))

    zz=process_data(etf_open, etf_close, stock_percent)

    # etf_open=np.array(etf_open.loc[stock_percent.index,:])
    # etf_close=np.array(etf_close.loc[stock_percent.index,:])
    # stock_percent=np.array(stock_percent)
    #
    #
    # for i in range(len(stock_percent)):
    #     print(i)
    #     if i == 0:
    #         # 在第一天，按照ETF权重购买
    #         etf_shares[i] = (cash * (1 - transaction_cost) * stock_percent[i])/(etf_open[i] * (1 + slippage))
    #         buy_value = (etf_shares[i] * etf_close[i] * (1 + slippage)).sum()
    #         cash -= buy_value * (1 + transaction_cost)
    #
    #     else:
    #         # 计算新的ETF份额
    #         new_shares = (stock_percent[i] * ((etf_shares[i-1] * etf_close[i-1]).sum()+cash))/(etf_close[i-1] * (1 + slippage))
    #
    #         # 计算需要卖出的ETF份额
    #         sell_shares = etf_shares[i - 1] - new_shares
    #         sell_shares[sell_shares < 0]=0
    #         # 计算卖出的成本
    #         sell_value = (sell_shares * etf_open[i] * (1 - slippage)).sum()
    #         # 扣除卖出的交易成本并增加现金
    #         cash += sell_value * (1 - transaction_cost)
    #
    #         # 计算需要购买的ETF份额
    #         buy_shares = new_shares - etf_shares[i - 1]
    #         buy_shares[buy_shares < 0]=0
    #         if np.all(buy_shares == 0):
    #
    #             etf_shares[i] = etf_shares[i - 1] + buy_shares - sell_shares
    #             continue
    #         # 计算购买的成本
    #         buy_value = (buy_shares * etf_close[i] * (1 + slippage)).sum()
    #
    #         if buy_value* (1 + transaction_cost)>cash:
    #             buy_shares=buy_shares/buy_value* (1 + transaction_cost)*cash
    #             buy_value = (buy_shares * etf_close[i] * (1 + slippage)).sum()
    #         # 扣除购买的交易成本并减少现金
    #         cash -= buy_value * (1 + transaction_cost)
    #
    #
    #
    #         # 更新ETF份额
    #         etf_shares[i] = etf_shares[i - 1] + buy_shares - sell_shares
    #
    # # 计算每日的投资组合价值
    # portfolio_value = (etf_shares * etf_close).sum(axis=1)+cash
    #
    # # 输出最终的投资组合价值
    # print(portfolio_value)
    #
    #
    #
    #
    #
    #
    #
    #
