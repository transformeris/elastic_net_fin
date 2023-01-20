import backtrader as bt
import datetime
import datetime  #

import lunardate
import scipy.stats
import os.path  # 路径管理
import sys  # 获取当前运行脚本的路径 (in argv[0])
import pickle
import numpy as np
import pandas as pd
import matplotlib as plt
import math
import akshare as ak

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def get_values(x):
    return x


class mydata(bt.feeds.PandasData):
    lines = ('qishuang',)
    params = (('qishuang', -1),)


class SignalBuySellStrategy(bt.Strategy):
    params=(('maperiod',15),
            ('printlog',True),)
    def __init__(self):
        # create a variable to track the current position
        self.my_position = 0
        # self.split_value = self.broker.getvalue() / 5.0
        # self.data.signal=self.data.signal

    def next(self):

        # check if we have a signal to buy
        if self.data.qishuang==1 and self.my_position==0:
            print('fuckkkkkkkkkkkkkkk',self.data.qishuang[0],self.data.datetime[0],self.datas[0].datetime.date(0))
            value = self.broker.get_cash()
            price = self.data.open[0]
            max_quantity = int(value / price)
            self.buy(size=max_quantity,price=1)
            self.my_position = 1

        # check if we have a signal to sell
        if self.data.qishuang==0 and self.my_position==1:
            self.sell(size=self.getposition().size,price=1)
            self.my_position=0

    def log(self, txt, dt=None,doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()},{txt}')


    def notify_order(self, order):
        # 如果order为submitted/accepted,返回空
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 如果order为buy/sell executed,报告价格结果
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'买入:\n价格:{order.executed.price},\
                成本:{order.executed.value},\
                手续费:{order.executed.comm},\
                数量: {order.executed.size}\
                持有现金: {self.broker.getcash()}\
                持有股数: {self.getposition().size}\
                总资产: {self.broker.getvalue()}')
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log(f'卖出:\n价格：{order.executed.price},\
                成本: {order.executed.value},\
                手续费:{order.executed.comm},\
                数量: {order.executed.size}\
                持有现金: {self.broker.getcash()}\
                持有股数: {self.getposition().size}\
                总资产: {self.broker.getvalue()}')
            self.bar_executed = len(self)

        # 如果指令取消/交易失败, 报告结果
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('交易失败')
        self.order = None
    def notify_trade(self,trade):
        if not trade.isclosed:
            return
        self.log(f'策略收益：\n毛收益 {trade.pnl:.2f}, 净收益 {trade.pnlcomm:.2f}')

    #回测结束后输出结果（可省略，默认输出结果）
    def stop(self):
        self.log('(MA均线： %2d日) 期末总资金 %.2f' %
                 (self.params.maperiod, self.broker.getvalue()), doprint=True)


# class mtm(pd.DataFrame):
#     def __init__(self):
#         self.


if __name__ == '__main__':
    stock_zh_index_daily_em_df = ak.stock_zh_index_daily_em(symbol="sz399997")
    stock_zh_index_daily_em_df.loc[::2,'qishuang']=0
    stock_zh_index_daily_em_df.loc[1::2,'qishuang']=1

    # print(stock_zh_index_daily_em_df)
    # etf_kline_all = load_obj('etf_all')
    # zhengquan_kline = etf_kline_all['sh512690']
    # zhengquan_kline.loc[:, 'trade_date'] = zhengquan_kline.index
    # pd.to_datetime(zhengquan_kline.loc[:, 'trade_date'])
    stock_zh_index_daily_em_df.set_index(pd.to_datetime(stock_zh_index_daily_em_df.loc[:, 'date']), inplace=True)

    lunardate.LunarDate(1900, 1, 1).toSolarDate()


    data_feed = mydata(dataname=stock_zh_index_daily_em_df)
    # data_feed.addcolumn('signal', zhengquan_kline['signal'])
    # data = bt.feeds.PandasData(dataname=zhengquan_kline, fromdate=datetime.datetime(2016, 1, 1),todate=datetime.datetime(2019, 1, 30))

    cerebro = bt.Cerebro()
    cerebro.adddata(data_feed)
    cerebro.broker.setcash(1000000.0)
    # 将策略添加到回测实例中
    cerebro.addstrategy(SignalBuySellStrategy)
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='ta')
    # 运行回测
    # 运行回测
    results = cerebro.run()
    cerebro.addwriter(bt.WriterFile, out='results.csv', csv=True)
    # 获取回测结果
    result = results
    strategy = result[0]
    ta = strategy.analyzers.ta.get_analysis()
    # print(ta)
    cerebro.plot(style='candlestick')
    #
