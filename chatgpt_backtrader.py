import backtrader as bt
import datetime
import datetime  #
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
#导入backtrader框架
import backtrader as bt

import datetime  #
import os.path  # 路径管理





class MyStrategy(bt.Strategy):
    def __init__(self,*args, **kwargs):
        super(MyStrategy, self).__init__(*args, **kwargs)
        bt.indicators.__init__(self,*args, **kwargs)
        sma=self.SimpleMovingAverage(self.datas[0], period=self.params.maperiod)
        print(sma)
    def next(self):
        if self.data.datetime.date(0).weekday() == 0:  # 如果是周一
            # print(self.data.datetime.date(),self.notify_trade(self.notify_trade()))
            self.order_target_percent(target=1.0, price=self.data.open[0])  # 买入
            self.order_target_percent(target=0.0, price=self.data.close[0])  # 卖出

        # If a trade is made, log the trade information
        if self.position:
            trade_info = {
                'date': self.datetime.date(0),

                'qty': self.position.size,
                'price': self.data.close[0],
            }

class SignalBuySellStrategy(bt.Strategy):
    def __init__(self):
        # create a variable to track the current position
        self.position = 0
        self.split_value = self.broker.getvalue() / 5.0

    def next(self):
        # check if we have a signal to buy
        if self.data.signal==1:
            self.split_value = self.broker.getvalue() / 5.0
            # check if we are not already in a position
            if self.position == 0:
                # calculate the number of shares to buy
                shares = int(self.split_value / self.data)

                # buy the shares
                self.buy(size=shares)

                # update the position variable
                self.position = 1

        # check if we have a signal to sell
        if self.data.signal==-1:
            self.split_value = self.broker.getvalue() / 5.0
            # check if we have a position
            if self.position != 0:
                shares = int(self.split_value / self.data)

                # sell one share
                self.sell(size=shares)

                # update the position variable
                self.position -= 1

# class TestStrategy(bt.Strategy):
#     params = (
#         ('maperiod', 15),
#     )
#
#     def log(self, txt, dt=None):
#         ''' 记录'''
#         dt = dt or self.datas[0].datetime.date(0)
#         print('%s, %s' % (dt.isoformat(), txt))
#
#     def __init__(self):
#         # Keep a reference to the "close" line in the data[0] dataseries
#         self.dataclose = self.datas[0].close
#
#         # To keep track of pending orders and buy price/commission
#         self.order = None
#         self.buyprice = None
#         self.buycomm = None
#
#         # 增加移动平均指标
#         self.sma = bt.indicators.SimpleMovingAverage(
#             self.datas[0], period=self.params.maperiod)
#
#         # 增加划线的指标
#         bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
#         bt.indicators.WeightedMovingAverage(self.datas[0], period=25,
#                                             subplot=True)
#         bt.indicators.StochasticSlow(self.datas[0])
#         bt.indicators.MACDHisto(self.datas[0])
#         rsi = bt.indicators.RSI(self.datas[0])
#         bt.indicators.SmoothedMovingAverage(rsi, period=10)
#         bt.indicators.ATR(self.datas[0], plot=False)
#
#     def notify_order(self, order):
#         if order.status in [order.Submitted, order.Accepted]:
#             # Buy/Sell order submitted/accepted to/by broker - Nothing to do
#             return
#
#         # Check if an order has been completed
#         # Attention: broker could reject order if not enough cash
#         if order.status in [order.Completed]:
#             if order.isbuy():
#                 self.log(
#                     'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
#                     (order.executed.price,
#                      order.executed.value,
#                      order.executed.comm))
#
#                 self.buyprice = order.executed.price
#                 self.buycomm = order.executed.comm
#             else:  # Sell
#                 self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
#                          (order.executed.price,
#                           order.executed.value,
#                           order.executed.comm))
#
#             self.bar_executed = len(self)
#
#         elif order.status in [order.Canceled, order.Margin, order.Rejected]:
#             self.log('Order Canceled/Margin/Rejected')
#
#         # Write down: no pending order
#         self.order = None
#
#     def notify_trade(self, trade):
#         if not trade.isclosed:
#             return
#
#         self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
#                  (trade.pnl, trade.pnlcomm))
#
#     def next(self):
#         # Simply log the closing price of the series from the reference
#         self.log('Close, %.2f' % self.dataclose[0])
#
#         # Check if an order is pending ... if yes, we cannot send a 2nd one
#         if self.order:
#             return
#
#         # Check if we are in the market
#         if not self.position:
#
#             # Not yet ... we MIGHT BUY if ...
#             if self.dataclose[0] > self.sma[0]:
#                 # BUY, BUY, BUY!!! (with all possible default parameters)
#                 self.log('BUY CREATE, %.2f' % self.dataclose[0])
#
#                 # Keep track of the created order to avoid a 2nd order
#                 self.order = self.buy()
#
#         else:
#
#             if self.dataclose[0] < self.sma[0]:
#                 # SELL, SELL, SELL!!! (with all possible default parameters)
#                 self.log('SELL CREATE, %.2f' % self.dataclose[0])
#
#                 # Keep track of the created order to avoid a 2nd order
#                 self.order = self.sell()


bt.sizers.FixedSize

etf_kline_all = load_obj('etf_all')

zhengquan_kline = etf_kline_all['sh512880']
zhengquan_kline.loc[:, 'trade_date'] = zhengquan_kline.index
pd.to_datetime(zhengquan_kline.loc[:, 'trade_date'])
zhengquan_kline.set_index(pd.to_datetime(zhengquan_kline.loc[:,'trade_date']),inplace=True)
# 将数据添加到回测实例中
data_=zhengquan_kline[datetime.datetime(2016,1,1):datetime.datetime(2019,1,30)]
data=bt.feeds.PandasData(dataname=zhengquan_kline,fromdate=datetime.datetime(2016,1,1),todate=datetime.datetime(2019,1,30))



cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.broker.setcash(10000.0)
# 将策略添加到回测实例中
cerebro.addstrategy(MyStrategy)

# 运行回测
# 运行回测
results = cerebro.run()
cerebro.addwriter(bt.WriterFile, out='results.csv', csv=True)
# 获取回测结果
result = results[0]
# cerebro.plot()
# 打印交易报告
# print(result.analyzers.TradeAnalyzer.get_analysis())
