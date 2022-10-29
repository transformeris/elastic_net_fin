import datetime  #
import os.path  # 路径管理
import sys  # 获取当前运行脚本的路径 (in argv[0])
import pickle
import numpy as np
import pandas as pd
import matplotlib as plt

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

# 创建策略继承bt.Strategy
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        # 记录策略的执行日志
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 保存收盘价的引用
        self.dataclose = self.datas[0].close

    def next(self):
        # 记录收盘价
        self.log('Close, %.2f' % self.dataclose[0]) ##self.dataclose[0]即为收盘价


class GridStrategy(bt.Strategy):
    params = (
        ("printlog", True),
        ("top", 2),
        ("buttom", 0),
    )

    def __init__(self):

        self.mid = (self.p.top + self.p.buttom) / 2.0
        print(self.mid)
        # 百分比区间计算
        # 这里多1/2，是因为arange函数是左闭右开区间。
        perc_level = [x for x in np.arange(1 + 0.02 * 5, 1 - 0.02 * 5 - 0.02 / 2, -0.02)]
        # 价格区间
        # print(self.mid)
        self.price_levels = [self.mid * x for x in perc_level]
        # 记录上一次穿越的网格
        self.last_price_index = None
        # 总手续费


        self.comm = 0.0


    def next(self):
        # print(self.last_price_index)
        # 开仓
        if self.last_price_index == None:
            # print("b", len(self.price_levels))
            for i in range(len(self.price_levels)):
                price = self.data.close[0]
                print("c", i, price, self.price_levels)
                if self.data.close[0] > self.price_levels[i]:
                    self.last_price_index = i
                    self.order_target_percent(target=i / (len(self.price_levels) - 1))
                    print("a")
                    return
        # 调仓
        else:
            signal = False
            while True:
                upper = None
                lower = None
                if self.last_price_index > 0:
                    upper = self.price_levels[self.last_price_index - 1]
                if self.last_price_index < len(self.price_levels) - 1:
                    lower = self.price_levels[self.last_price_index + 1]
                # 还不是最轻仓，继续涨，再卖一档
                if upper != None and self.data.close > upper:
                    self.last_price_index = self.last_price_index - 1
                    print("fuck",  self.price_levels,self.last_price_index,[upper,lower])
                    signal = True
                    continue
                # 还不是最重仓，继续跌，再买一档
                if lower != None and self.data.close < lower:
                    self.last_price_index = self.last_price_index + 1
                    signal = True
                    continue
                break
            if signal:
                self.long_short = None
                self.order_target_percent(target=self.last_price_index / (len(self.price_levels) - 1))
                print(self.last_price_index / (len(self.price_levels) - 1))


    # 输出交易记录
    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))


    def notify_order(self, order):
        # 有交易提交/被接受，啥也不做
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 交易完成，报告结果
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '执行买入, 价格: %.2f, 成本: %.2f, 手续费 %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                self.buyprice = order.executed.price


                self.comm += order.executed.comm
            else:
                self.log(
                '执行卖出, 价格: %.2f, 成本: %.2f, 手续费 %.2f' %
                (order.executed.price,
                 order.executed.value,
                 order.executed.comm))
            self.comm += order.executed.comm
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("交易失败")
            self.order = None


    # 输出手续费
    def stop(self):
        self.log("手续费:%.2f 成本比例:%.5f" % (self.comm, self.comm / self.broker.getvalue()))

class jinzitaStrategy(bt.Strategy):
    params = (
        ("printlog", True),
        ("top", 2),
        ("buttom", 0),
    )

    def __init__(self):

        self.mid = (self.p.top + self.p.buttom) / 2.0
        print(self.mid)
        # 百分比区间计算
        # 这里多1/2，是因为arange函数是左闭右开区间。
        perc_level = [x for x in np.arange(1 + 0.02 * 5, 1 - 0.02 * 5 - 0.02 / 2, -0.02)]
        # 价格区间
        # print(self.mid)
        self.price_levels = [self.mid * x for x in perc_level]
        # 记录上一次穿越的网格
        self.last_price_index = None
        # 总手续费


        self.comm = 0.0


    def next(self):
        # print(self.last_price_index)
        # 开仓
        if self.last_price_index == None:
            # print("b", len(self.price_levels))
            for i in range(len(self.price_levels)):
                price = self.data.close[0]
                # print("c", i, price, self.price_levels[i][0])
                if self.data.close[0] > self.price_levels[i]:
                    self.last_price_index = i
                    self.order_target_percent(target=i / (len(self.price_levels) - 1))

                    print("a")
                    return
        # 调仓
        else:
            signal = False
            while True:
                upper = None
                lower = None
                if self.last_price_index > 0:
                    upper = self.price_levels[self.last_price_index - 1]
                if self.last_price_index < len(self.price_levels) - 1:
                    lower = self.price_levels[self.last_price_index + 1]
                # 还不是最轻仓，继续涨，再卖一档
                if upper != None and self.data.close > upper:
                    self.last_price_index = self.last_price_index - 1
                    signal = True
                    continue
                # 还不是最重仓，继续跌，再买一档
                if lower != None and self.data.close < lower:
                    self.last_price_index = self.last_price_index + 1
                    signal = True
                    continue
                break
            if signal:
                self.long_short = None
                self.order_target_percent(target=self.last_price_index / (len(self.price_levels) - 1))
                print(self.last_price_index / (len(self.price_levels) - 1))


    # 输出交易记录
    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))


    def notify_order(self, order):
        # 有交易提交/被接受，啥也不做
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 交易完成，报告结果
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '执行买入, 价格: %.2f, 成本: %.2f, 手续费 %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                self.buyprice = order.executed.price


                self.comm += order.executed.comm
            else:
                self.log(
                '执行卖出, 价格: %.2f, 成本: %.2f, 手续费 %.2f' %
                (order.executed.price,
                 order.executed.value,
                 order.executed.comm))
            self.comm += order.executed.comm
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("交易失败")
            self.order = None


    # 输出手续费
    def stop(self):
        self.log("手续费:%.2f 成本比例:%.5f" % (self.comm, self.comm / self.broker.getvalue()))



class TestStrategy(bt.Strategy):
    def __init__(self):
        # 打印数据集和数据集对应的名称
        print("-------------self.datas-------------")
        print(list(self.datas))
        print(self.datas[0].open)
        # print("-------------self.data-------------")
        # print(self.data._name, list(self.data)) # 返回第一个导入的数据表格，缩写形式
        # print("-------------self.data0-------------")
        # print(self.data0._name, self.data0) # 返回第一个导入的数据表格，缩写形式
        # print("-------------self.datas[0]-------------")
        # print(self.datas[0]._name, list(self.datas[0])) # 返回第一个导入的数据表格，常规形式
        # print("-------------self.datas[1]-------------")
        # # print(self.datas[1]._name, self.datas[1]) # 返回第二个导入的数据表格，常规形式
        # # print("-------------self.datas[-1]-------------")
        # # print(self.datas[-1]._name, self.datas[-1]) # 返回最后一个导入的数据表格
        # # print("-------------self.datas[-2]-------------")
        # # print(self.datas[-2]._name, self.datas[-2]) # 返回倒数第二个导入的数据表格
        # print(list(self.data.line))
        # a=self.data.close*2
        # print(list(a))


if __name__ == '__main__':

    etf_kline_all=load_obj('etf_all')

    zhengquan_kline=etf_kline_all['sh512880']

    # 创建Cerebro引擎
    cerebro = bt.Cerebro()
    # Cerebro引擎在后台创建broker(经纪人)，系统默认资金量为10000

    # 获取当前运行脚本所在目录
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    # 拼接加载路径
    # datapath = os.path.join(zhengquan_kline)

    # 创建交易数据集
    # data = bt.feeds.YahooFinanceCSVData(
    #     dataname=zhengquan_kline,
    #     # 数据必须大于fromdate
    #     fromdate=datetime.datetime(2000, 1, 1),
    #     # 数据必须小于todate
    #     todate=datetime.datetime(2021, 12, 31),
    #     reverse=False)
    # data=zhengquan _kline[datetime.date(2016, 8, 10):datetime.date(2020, 8, 30)]
    zhengquan_kline.loc[:,'trade_date']=zhengquan_kline.index
    # zhengquan_kline.set_index(datetime.datetime(zhengquan_kline.index))
    pd.to_datetime(zhengquan_kline.loc[:,'trade_date'])
    zhengquan_kline.set_index(pd.to_datetime(zhengquan_kline.loc[:,'trade_date']),inplace=True)
    data=bt.feeds.PandasData(dataname=zhengquan_kline,fromdate=datetime.datetime(2018,1,1),todate=datetime.datetime(2019,1,30))

    data_watch=zhengquan_kline[datetime.datetime(2018,1,1):datetime.datetime(2019,1,30)]

    # 加载交易数据
    cerebro.adddata(data)


    # 设置投资金额100000.0
    cerebro.broker.setcash(100000.0)
    # 引擎运行前打印期出资金
    cerebro.addstrategy(TestStrategy)
    print('初: %.2f' % cerebro.broker.getvalue())
    cerebro.addobserver(bt.observers.Broker)
    cerebro.run()

