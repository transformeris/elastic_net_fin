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



class ETFBacktest(bt.Strategy):
    params = (
        ('growth_etf', '510050.SH'),  # 创成长ETF
        ('dividend_etf', '510880.SH'),  # 红利低波ETF
        ('period', None),  # 计算涨跌幅的周期
        ('rebalance_days', 1),  # 调仓周期
        ('commission', 0.01), # 手续费
        ('cheat_on_open', False), # 开盘成交

    )

    def __init__(self):
        self.returns = []
        self.max_drawdown = None
        self.sharpe_ratio = None
        self.information_ratio = None
        self.win_rate = None


        self.cyb_etf = self.datas[0]
        self.hs300_etf = self.datas[1]
        self.ndaq_etf = self.datas[2]
        self.gold_etf = self.datas[3]
        self.holding_signal = self.datas[4]
        self.rebalance_counter = 0
        self.etf_num={0:'cyb_etf',1:'hs300_etf',2:'ndaq_etf',3:'gold_etf'}

        self.log_returns = []
        self.log_df = pd.DataFrame(columns=[
            'date', 'growth_etf_position', 'dividend_etf_position',
            'total_position', 'cash', 'calculate_returns_growth_etf',
            'calculate_returns_dividend_etf','value'
        ])

        self.trade_type = None


    def next(self):
        """
        This method is called for each new bar (or candle) in the data feed.
        It is used to calculate the RSRS indicator, check if it is above the
        threshold, and place orders accordingly.
        """


        self.etf_num=[0,1,2,3]
        long=[]
        short=[]


        self.order_target_percent(self.datas[0], target=self.datas[4].cyb_etf,exectype=bt.Order.Market)
        self.order_target_percent(self.datas[1], target=self.datas[4].hs300_etf, exectype=bt.Order.Market)
        self.order_target_percent(self.datas[2], target=self.datas[4].ndaq_etf, exectype=bt.Order.Market)
        self.order_target_percent(self.datas[3], target=self.datas[4].gold_etf, exectype=bt.Order.Market)




        self.rebalance_counter += 1

        # self.log_returns.append([
        #     self.datas[0].datetime.date(0),
        #     self.calculate_returns(self.growth_etf),
        #     self.calculate_returns(self.dividend_etf),
        #     self.log_returns
        # ])
        #

        # # 计算持仓股、份额、账户总份额和现金等信息


        cash = self.broker.get_cash()
        date = self.datas[0].datetime.date(0)
        value = self.broker.getvalue()
        #
        # 将信息添加到log_df中
        self.log_df = self.log_df.append({
            'date': date,
            'cash': cash,
            'value': value
        }, ignore_index=True)



    def calculate_returns(self, data):

        returns = (data.close[0] - data.close[-self.params.period]) / data.close[-self.params.period]
        return returns


    def get_log_df(self):
        return self.log_df

    def stop(self):
        print(self.log_df)


class OrderRecorder(bt.Analyzer):
    def __init__(self):

        self.orders = []

    def notify_order(self, order):

        self.orders.append([self.strategy.datetime.datetime(0),order])


class TradeRecorder(bt.Analyzer):
    def __init__(self):
        self.trades = []

    def notify_trade(self, trade):

        self.trades.append([self.strategy.datetime.datetime(0),trade])

class MyAnalyzer(bt.Analyzer):
    def __init__(self):
        self.log_df = pd.DataFrame(columns=[
            'date', 'cyb_etf_position', 'hs300_etf_position','ndaq_etf_position','gold_etf_position',
            'total_position', 'cash', 'calculate_returns_growth_etf',
            'calculate_returns_dividend_etf', 'value'
        ])

    def next(self):

        # 计算持仓股、份额、账户总份额和现金等信息
        cyb_etf_position = self.strategy.getposition(self.strategy.cyb_etf).size
        hs300_etf_position = self.strategy.getposition(self.strategy.hs300_etf).size
        ndaq_etf_position = self.strategy.getposition(self.strategy.ndaq_etf).size
        gold_etf_position = self.strategy.getposition(self.strategy.gold_etf).size
        total_position = cyb_etf_position + hs300_etf_position+ndaq_etf_position+gold_etf_position
        cash = self.strategy.broker.get_cash()
        date = self.strategy.datas[0].datetime.date(0)
        # calculate_returns_cyb_etf = self.strategy.calculate_returns(self.strategy.cyb_etf)
        # calculate_returns_dividend_etf = self.strategy.calculate_returns(self.strategy.dividend_etf)
        value = self.strategy.broker.getvalue()

        self.log_df = self.log_df.append({
            'date': date,
            'cyb_etf_position': cyb_etf_position,
            'hs300_etf_position':hs300_etf_position,
            'ndaq_etf_position':ndaq_etf_position,
            'gold_etf_position':gold_etf_position,
            'total_position': total_position,
            'cash': cash,
            # 'calculate_returns_growth_etf': calculate_returns_growth_etf,
            # 'calculate_returns_dividend_etf': calculate_returns_dividend_etf,
            'value': value
        }, ignore_index=True)

    def get_analysis(self):
        return {'log_df': self.log_df}



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

class MyData(bt.feeds.PandasData):
    lines= ('cyb_etf','hs300_etf','ndaq_etf','gold_etf',)
    params = (
        ('cyb_etf', -1),
        ('hs300_etf', -1),
        ('ndaq_etf', -1),
        ('gold_etf', -1),
    )



if __name__ == '__main__':

    cerebro = bt.Cerebro(tradehistory=True)
    # cerebro.optstrategy(ETFBacktest,period=range(1,150))
    cerebro.addstrategy(ETFBacktest)

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


    etf_open=np.array(etf_open.loc[stock_percent.index,:])
    etf_close=np.array(etf_close.loc[stock_percent.index,:])
    stock_percent=np.array(stock_percent)
    a=np.array(holding_df.iloc[21:,0:4].shift(1).fillna(0))
    stock_percent=np.where(a == np.max(a, axis=1, keepdims=True), 1, 0)
    stock_percent[0]=np.array([0,0,0,0])

    # stock_percent= np.where(stock_percent == np.max(stock_percent, axis=1, keepdims=True), 1, 0)


    for i in range(len(stock_percent)):
        print(i)
        if i == 0:
            # 在第一天，按照ETF权重购买
            etf_shares[i] = (cash * (1 - transaction_cost) * stock_percent[i])/(etf_open[i] * (1 + slippage))
            buy_value = (etf_shares[i] * etf_close[i] * (1 + slippage)).sum()
            cash -= buy_value * (1 + transaction_cost)

        else:
            # 计算新的ETF份额
            new_shares = (stock_percent[i] * ((etf_shares[i-1] * etf_close[i-1]).sum()+cash))/(etf_close[i-1] * (1 + slippage))

            # 计算需要卖出的ETF份额
            sell_shares = etf_shares[i - 1] - new_shares
            sell_shares[sell_shares < 0]=0
            # 计算卖出的成本
            sell_value = (sell_shares * etf_open[i] * (1 - slippage)).sum()
            # 扣除卖出的交易成本并增加现金
            cash += sell_value * (1 - transaction_cost)

            # 计算需要购买的ETF份额
            buy_shares = new_shares - etf_shares[i - 1]
            buy_shares[buy_shares < 0]=0
            if np.all(buy_shares == 0):

                etf_shares[i] = etf_shares[i - 1] + buy_shares - sell_shares
                continue
            # 计算购买的成本
            buy_value = (buy_shares * etf_close[i] * (1 + slippage)).sum()

            if buy_value* (1 + transaction_cost)>cash:
                buy_shares=buy_shares/buy_value* (1 + transaction_cost)*cash
                buy_value = (buy_shares * etf_close[i] * (1 + slippage)).sum()
            # 扣除购买的交易成本并减少现金
            cash -= buy_value * (1 + transaction_cost)



            # 更新ETF份额
            etf_shares[i] = etf_shares[i - 1] + buy_shares - sell_shares

    # 计算每日的投资组合价值
    portfolio_value = (etf_shares * etf_close).sum(axis=1)+cash

    # 输出最终的投资组合价值
    print(portfolio_value)








