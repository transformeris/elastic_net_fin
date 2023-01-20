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

class mydata(bt.feeds.PandasData):
    lines = ('signal',)
    params = (('signal', -1),)


class SignalBuySellStrategy(bt.Strategy):
    params=(('maperiod',15),
            ('printlog',True),)
    def __init__(self):
        # create a variable to track the current position
        self.my_position = 0
        self.split_value = self.broker.getvalue() / 5.0
        # self.data.signal=self.data.signal

    def next(self):

        # check if we have a signal to buy
        if self.data.signal[0]==1:
            # print('fuckme')
            self.split_value = self.broker.getvalue() / 5.0
            # check if we are not already in a position

            # calculate the number of shares to buy
            shares = int(self.split_value / self.data)

            # buy the shares
            # self.buy(size=500)

            self.order_target_percent(target=1)
            # self.notify_order()
            # update the position variable
            self.my_position = 1

        # check if we have a signal to sell
        if self.data.signal[0]==-1 and self.getposition().size>0:
            # print('fuck',self.getposition().size)
            self.split_value = self.broker.getvalue() / 5.0
            # check if we have a position

                # shares = int(self.split_value / self.data)

                # sell one share
            # self.sell(size=500)
            self.order_target_percent(target=0)
                # update the position variable
                # self.position -= 1
        # print(self.broker.getcash())
        # print(self.broker.getvalue())

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
            else:
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


if __name__=='__main__':
    etf_kline_all = load_obj('etf_all')
    zhengquan_kline = etf_kline_all['sh513050']
    zhengquan_kline.loc[:, 'trade_date'] = zhengquan_kline.index
    pd.to_datetime(zhengquan_kline.loc[:, 'trade_date'])
    zhengquan_kline.set_index(pd.to_datetime(zhengquan_kline.loc[:, 'trade_date']), inplace=True)

    zhengquan_kline['ma_20']=zhengquan_kline['close'].rolling(30).mean()
    zhengquan_kline['delta_close']=(zhengquan_kline['close']-zhengquan_kline['ma_20'])/zhengquan_kline['ma_20']
    zhengquan_kline['trade_date_shift']=pd.to_datetime(zhengquan_kline['trade_date'].shift(periods=30))
    for i in zhengquan_kline.iterrows():
        delta_close_window=zhengquan_kline.loc[i[1]['trade_date_shift']:i[0],'delta_close']
        zz=scipy.stats.percentileofscore(delta_close_window, zhengquan_kline.loc[i[0],'delta_close'])
        zhengquan_kline.loc[i[0], 'delta_percent']=zz
    # zhengquan_kline.loc[zhengquan_kline['delta_percent']==1.639344262295082,'signal']=1
    zhengquan_kline.loc[zhengquan_kline['delta_percent']<30,'signal']=1

    # zhengquan_kline.loc[zhengquan_kline['delta_percent'] ==100, 'signal'] = -1
    zhengquan_kline.loc[zhengquan_kline['delta_percent'] >99, 'signal'] = -1

    data = zhengquan_kline.to_dict(orient='list')
    zhengquan_kline['changwei'] = 0
    zhengquan_kline.loc[zhengquan_kline['signal']==1,'changwei']=1
    zhengquan_kline.loc[zhengquan_kline['signal'] == -1, 'changwei'] = -1

    zhengquan_kline['mtm_20']=(zhengquan_kline['close']-zhengquan_kline['close'].shift(20))/zhengquan_kline['close'].shift(20)


    # create a Backtrader data feed
    # data_feed = mydata(dataname=zhengquan_kline)
    # # data_feed.addcolumn('signal', zhengquan_kline['signal'])
    # # data = bt.feeds.PandasData(dataname=zhengquan_kline, fromdate=datetime.datetime(2016, 1, 1),todate=datetime.datetime(2019, 1, 30))
    #
    # cerebro = bt.Cerebro()
    # cerebro.adddata(data_feed)
    # cerebro.broker.setcash(10000.0)
    # # 将策略添加到回测实例中
    # cerebro.addstrategy(SignalBuySellStrategy)
    # cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='ta')
    # # 运行回测
    # # 运行回测
    # results = cerebro.run()
    # # cerebro.addwriter(bt.WriterFile, out='results.csv', csv=True)
    # # # 获取回测结果
    # # result = results
    # # strategy = result[0]
    # # ta = strategy.analyzers.ta.get_analysis()
    # # print(ta)
    # cerebro.plot(style='candlestick')
    #


