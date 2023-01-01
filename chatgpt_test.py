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
import sys  # 获取当前运行脚本的路径 (in argv[0])

#导入backtrader框架
import backtrader as bt
def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
# 创建一个回测策略类
class MyStrategy(bt.Strategy):
    def __init__(self):
        # 初始化已买入的标志
        pass


    def log_trade(self,trade):


        print(f"Trade closed - Entry price: {trade.price} - Exit price: {trade.exitprice}")
        print(f"Trade size: {trade.size} - PnL: {trade.pnl}")



    def next(self):

        if self.data.datetime.date(0).weekday() == 0:  # 如果是周一
            print(self.data.datetime.date())
            print(cerebro.broker.getvalue())
            trade = self.getposition(self.data)
            print(trade)
            self.order_target_percent(target=1.0,price=self.data.open[0])  # 买入
            self.order_target_percent(target=0.0,price=self.data.close[0])  # 卖出
            # if self.order.status == bt.Order.Completed:
            #     # The order was completed successfully
            #     print("Order completed successfully.")
            # else:
            #     # The order failed
            #     print("Order failed.")

            # self.log_trade(self.trade)
    # def next(self):
    #     print(f'当前总资产：{self.broker.getvalue()}')
    #     if self.order:
    #         # 如果存在未完成的订单，则检查是否完成
    #         if self.order.isbuy():
    #             # 如果是买入订单，则检查是否成交
    #             if self.order.status == bt.Order.Completed:
    #                 # 如果订单成交，则打印成交信息
    #                 print(f'买入时间：{self.data.datetime.date()}，买入金额：{self.order.executed.price * self.order.executed.size}')
    #
    #         elif self.order.issell():
    #             # 如果是卖出订单，则检查是否成交
    #             if self.order.status == bt.Order.Completed:
    #                 # 如果订单成交，则打印成交信息
    #                 print(f'卖出时间：{self.data.datetime.date()}，卖出金额：{self.order.executed.price * self.order.executed.size}')
    #
    #
    #
    #     # 如果当前时间是周一
    #     if self.datetime.date().weekday() == 0:
    #         # 如果上一个交易日没有持仓，则以当天开盘价买入
    #         if not self.position:
    #             self.order = self.buy(price=self.data.open[0],size = self.broker.getvalue()/self.data.open[0])
    #
    #     # 如果有持仓，且当前时间是周二
    #     if self.position and self.datetime.date().weekday() == 0:
    #         print('sell')
    #         # 以隔天收盘价卖出
    #         self.order = self.sell(price=self.data.close[0],size = None)



# 创建一个 backtrader 的回测实例
cerebro = bt.Cerebro()

# 加载历史数据
# data = bt.feeds.YahooFinanceData(dataname="AAPL", fromdate=datetime.datetime(2020, 1, 1), todate=datetime.datetime(2020, 12, 31))
etf_kline_all = load_obj('etf_all')

zhengquan_kline = etf_kline_all['sh512880']
zhengquan_kline.loc[:, 'trade_date'] = zhengquan_kline.index
pd.to_datetime(zhengquan_kline.loc[:, 'trade_date'])
zhengquan_kline.set_index(pd.to_datetime(zhengquan_kline.loc[:,'trade_date']),inplace=True)
# 将数据添加到回测实例中
data_=zhengquan_kline[datetime.datetime(2016,1,1):datetime.datetime(2019,1,30)]
data=bt.feeds.PandasData(dataname=zhengquan_kline,fromdate=datetime.datetime(2016,1,1),todate=datetime.datetime(2019,1,30))
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
# MyStrategy.notify_trade()

您可以在策略类的 next() 方法中使用 backtrader 的 order_target_percent() 方法来实现这一目标。

例如，您可以使用如下代码在偏离程度达到一定程度时买入股票：

Copy code
if self.data.close > self.sma:
    self.order_target_percent(target=0.33)  # Buy 1/3 of the total capital
elif self.data.close > self.sma * 1.2:
    self.order_target_percent(target=0.66)  # Buy 2/3 of the total capital


if self.data.close < self.sma:
    self.order_target_percent(target=-0.33)  # Sell 1/3 of the total capital
elif self.data.close < self.sma * 0.8:
    self.order_target_percent(target=-0.66)  # Sell 2/3 of the total capital



class MyData(bt.feeds.PandasData):
    lines = ('pe_ratio',)  # Add a line for the P/E ratio

data = MyData(dataname=df)  # df is a Pandas DataFrame containing the data



class MyStrategy(bt.Strategy):
    def next(self):
        pe_ratio = self.data.pe_ratio[0]  # Access the P/E ratio for the current bar
        print(pe_ratio)

# Create the strategy
strategy = MyStrategy(data=data)


在 backtrader 中，您可以使用以下方法来买入股票：

order_target_percent()：使用总资金的一定比例来买入股票。例如，如果您想使用总资金的50%来买入股票，则可以使用如下代码：
Copy code
self.order_target_percent(target=0.5)
order_target_size()：使用固定的股票数量来买入。例如，如果您想买入10股股票，则可以使用如下代码：
Copy code
self.order_target_size(size=10)
order_target_value()：使用固定的资金额来买入股票。例如，如果您想使用1000元的资金来买入股票，则可以使用如下代码：
Copy code
self.order_target_value(target=1000)
order_percent()：使用当前价格来计算股票数量，并使用总资金的一定比例来买入。例如，如果您想使用



1412189000@qq.com
继续
总资金的50%来买入股票，则可以使用如下代码：

Copy code
self.order_percent(percent=0.5)
order_size()：使用固定的股票数量来买入，并自动计算所需的资金额。例如，如果您想买入10股股票，则可以使用如下代码：
Copy code
self.order_size(size=10)
order_value()：使用固定的资金额来买入股票，并自动计算所需的股票数量。例如，如果您想使用1000元的资金来买入股票，则可以使用如下代码：
Copy code
self.order_value(value=1000)


请注意，在使用这些方法时，您需要确保已经创建了一个交易对象，并且该对象已经初始化。例如，如果您想使用 order_target_percent() 方法来买入股票，则需要先创建一个 bt.Order 类的对象，并将其传入 order_target_percent() 方法。

如果您有更多问题，请随时告诉我。


请注意，在使用这些方法时，您需要确保已经创建了一个交易对象，并且该对象已经初始化。例如，如果您想使用 order_target_percent() 方法来买入股票，则需要先创建一个 bt.Order 类的对象，并将其传入 order_target_percent() 方法。

如果您有更多问题，请随时告诉我。




1412189000@qq.com
如果不创建交易对象就使用这些方法，会出现什么错误？

如果在 backtrader 中没有创建交易对象就使用了用于买入股票的方法，则会出现 AttributeError 错误。这是因为，在 backtrader 中，需要在策略类中创建交易对象才能执行交易操作。

例如，如果您想使用 order_target_percent() 方法来买入股票，则需要先创建一个 bt.Order 类的对象，并将其传入 order_target_percent() 方法。例如：

Copy code
order = self.order_target_percent(target=0.5)
如果您没有创建交易对象，则会收到以下错误消息：

Copy code
AttributeError: 'MyStrategy' object has no attribute 'broker'
如果您收到了类似的错误消息，则需要在策略类中创建交易对象。例如，如果您想使用 bt.brokers.BackBroker 类来创建交易对象，则可以使用如下代码：

Copy code
# Create a broker
broker = bt.brokers.BackBroker()

# Set the broker's cash
broker.set_cash(10000)

# Create the strategy
strategy = MyStrategy(broker=broker)
希望这些信息能帮助您。如果您有更多问题，请随时告诉我。

接下来我提的所有问题，你要将每次输出答案的时间限制在50秒以内，在我输入“继续”的时候，再输出剩余的内容