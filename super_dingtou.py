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
    def __init__(self):
        # create a variable to track the current position
        self.my_position = 0
        self.split_value = self.broker.getvalue() / 5.0
        # self.data.signal=self.data.signal

    def next(self):

        # check if we have a signal to buy
        if self.data.signal[0]==1:
            self.split_value = self.broker.getvalue() / 5.0
            # check if we are not already in a position

            # calculate the number of shares to buy
            shares = int(self.split_value / self.data)

            # buy the shares
            self.buy(size=shares)

            # update the position variable
            self.my_position = 1

        # check if we have a signal to sell
        if self.data.signal==-1:
            self.split_value = self.broker.getvalue() / 5.0
            # check if we have a position
            if self.position != 0:
                shares = int(self.split_value / self.data)

                # sell one share
                self.sell(size=shares)

                # update the position variable
                # self.position -= 1
        print(self.broker.getcash())
        print(self.broker.getvalue())

if __name__=='__main__':
    etf_kline_all = load_obj('etf_all')
    zhengquan_kline = etf_kline_all['sh512880']
    zhengquan_kline.loc[:, 'trade_date'] = zhengquan_kline.index
    pd.to_datetime(zhengquan_kline.loc[:, 'trade_date'])
    zhengquan_kline.set_index(pd.to_datetime(zhengquan_kline.loc[:, 'trade_date']), inplace=True)

    zhengquan_kline['ma_20']=zhengquan_kline['close'].rolling(60).mean()
    zhengquan_kline['delta_close']=(zhengquan_kline['close']-zhengquan_kline['ma_20'])/zhengquan_kline['ma_20']
    zhengquan_kline['trade_date_shift']=pd.to_datetime(zhengquan_kline['trade_date'].shift(periods=60))
    for i in zhengquan_kline.iterrows():
        delta_close_window=zhengquan_kline.loc[i[1]['trade_date_shift']:i[0],'delta_close']
        zz=scipy.stats.percentileofscore(delta_close_window, zhengquan_kline.loc[i[0],'delta_close'])
        zhengquan_kline.loc[i[0], 'delta_percent']=zz
    zhengquan_kline.loc[zhengquan_kline['delta_percent']==1.639344262295082,'signal']=1
    zhengquan_kline.loc[zhengquan_kline['delta_percent'] ==100, 'signal'] = -1
    data = zhengquan_kline.to_dict(orient='list')
    zhengquan_kline.loc[zhengquan_kline['signal']!=0,'signal']=0



    # # create a Backtrader data feed
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
    # cerebro.addwriter(bt.WriterFile, out='results.csv', csv=True)
    # # 获取回测结果
    # result = results
    # strategy = result[0]
    # ta = strategy.analyzers.ta.get_analysis()
    # print(ta)
    # cerebro.plot(style='candlestick')



