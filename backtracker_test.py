import datetime  #
import os.path  # 路径管理
import sys  # 获取当前运行脚本的路径 (in argv[0])
import pickle

import pandas as pd


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
#导入backtrader框架
import backtrader as bt
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
    # data=zhengquan_kline[datetime.date(2016, 8, 10):datetime.date(2020, 8, 30)]
    zhengquan_kline.loc[:,'trade_date']=zhengquan_kline.index
    # zhengquan_kline.set_index(datetime.datetime(zhengquan_kline.index))
    pd.to_datetime(zhengquan_kline.loc[:,'trade_date'])
    zhengquan_kline.set_index(pd.to_datetime(zhengquan_kline.loc[:,'trade_date']),inplace=True)
    data=bt.feeds.PandasData(dataname=zhengquan_kline,fromdate=datetime.datetime(2016,8,1),todate=datetime.datetime(2016,8,9))


    # 加载交易数据
    cerebro.adddata(data)


    # 设置投资金额100000.0
    cerebro.broker.setcash(100000.0)
    # 引擎运行前打印期出资金
    print('组合期初资金: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    # 引擎运行后打期末资金
    print('组合期末资金: %.2f' % cerebro.broker.getvalue())