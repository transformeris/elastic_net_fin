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
        ('rebalance_days', 5),  # 调仓周期
        ('commission', 0.01), # 手续费
        ('cheat_on_open', False), # 开盘成交

    )

    def __init__(self):
        self.returns = []
        self.max_drawdown = None
        self.sharpe_ratio = None
        self.information_ratio = None
        self.win_rate = None

        stock_name = {1: 'cyb_etf', 2: 'hs300_etf', 3: 'ndaq_etf', 4: 'gold_etf'}
        self.holding_signal = self.datas[0]
        self.cyb_etf = self.datas[1]
        self.hs300_etf = self.datas[2]
        self.ndaq_etf = self.datas[3]
        self.gold_etf = self.datas[4]
        self.jp_etf = self.datas[5]
        # self.holding_signal = self.datas[4]
        self.rebalance_counter = 0
        # self.etf_num={0:'cyb_etf',1:'hs300_etf',2:'ndaq_etf',3:'gold_etf'}
        self.etf_num=list(range(1,len(self.datas)))
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
        select_etf_number= self.holding_signal.max_return_20_etf_number[0]
        print(select_etf_number)


        long=[]
        short=[]

        for i in self.etf_num:
            if i!=select_etf_number:
                short.append(i)
        for j in short:
            self.order_target_percent(self.datas[j], target=0,exectype=bt.Order.Market)
        self.order_target_percent(self.datas[int(select_etf_number)], target=0.99,exectype=bt.Order.Close)



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
            'date', 'cyb_etf_position', 'hs300_etf_position','ndaq_etf_position','gold_etf_position','jp_etf_position',
            'total_position', 'cash', 'calculate_returns_growth_etf',
            'calculate_returns_dividend_etf', 'value'
        ])

    def next(self):

        # 计算持仓股、份额、账户总份额和现金等信息
        etf_position=[]
        for i in range(1,len(self.strategy.datas)):
            etf_position.append(self.strategy.getposition(self.strategy.datas[i]).size)
        cyb_etf_position = self.strategy.getposition(self.strategy.cyb_etf).size
        hs300_etf_position = self.strategy.getposition(self.strategy.hs300_etf).size
        ndaq_etf_position = self.strategy.getposition(self.strategy.ndaq_etf).size
        gold_etf_position = self.strategy.getposition(self.strategy.gold_etf).size
        jp_etf_position = self.strategy.getposition(self.strategy.jp_etf).size
        total_position = sum(etf_position)
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
    lines= ('max_return_20_etf_number',)
    params = (
        ('max_return_20_etf_number', -1),
    )



if __name__ == '__main__':
    cerebro = bt.Cerebro(tradehistory=True)
    # cerebro.optstrategy(ETFBacktest,period=range(1,150))
    cerebro.addstrategy(ETFBacktest)

    # hs_300=ak.stock_zh_index_daily_em(symbol='sh000300')
    cyb_etf = ak.fund_etf_hist_em(symbol='159915', adjust='qfq')
    hs300_etf= ak.fund_etf_hist_em(symbol='510300', adjust='qfq')
    ndaq_etf= ak.fund_etf_hist_em(symbol='513100', adjust='qfq')
    gold_etf= ak.fund_etf_hist_em(symbol='518880', adjust='qfq')
    jp_etf= ak.fund_etf_hist_em(symbol='513520', adjust='qfq')
    stock_collection={1:cyb_etf,2:hs300_etf,3:ndaq_etf,4:gold_etf,5:jp_etf}
    stock_name={1:'cyb_etf',2:'hs300_etf',3:'ndaq_etf',4:'gold_etf',5:'jp_etf'}
    stock_name_list=list(stock_name.values())
    # dividend_etf_data = ak.fund_etf_hist_em(symbol='512890', adjust='qfq')
    # dividend_etf_data=ak.fund_etf_hist_sina(symbol='sz159649')
    # growth_etf_data=ak.stock_zh_index_daily_em(symbol='sh000300')
    # growth_etf_data=ak.stock_zh_a_hist(symbol="600519", start_date="20000101")
    # dividend_etf_data=ak.stock_zh_index_daily_em(symbol='sh000013')
    etfs=rename_columns(stock_collection)


    # 假设cyb_etf、hs300_etf、ndaq_etf、gold_etf是四个pandas dataframe表格


    # 计算二十日收益率
    for etf in etfs.values():
        etf['return_20'] = etf['close'].pct_change(periods=21)

    # 合并四个表格
    holding_df = pd.concat(etfs, axis=1, join='inner')
    holding_df=holding_df.filter(regex='return_20')
    holding_df.columns=stock_name.values()
    etf_number=list(range(1,len(stock_name)+1))
    holding_df['max_return_20_etf_name']=holding_df.idxmax(axis=1)
    holding_df['max_return_20_etf_number']=holding_df['max_return_20_etf_name'].replace(stock_name_list,etf_number)


    # 找出每天二十日收益率最大的品种



    # dividend_etf_data=ak.stock_zh_index_daily_em(symbol='sh000016')

    # hs_300=rename_columns(hs_300)
    # zzzzz=ak.stock_zh_index_spot()
    # dividend_etf_data=rename_columns(dividend_etf_data)


    date_start_list = []
    for i in stock_collection.values():
        date_start_list.append(i.index[0])

    start_date = max(date_start_list)
    end_date = datetime.datetime(2023, 12, 31)

    holding_signal = MyData(dataname=holding_df, fromdate=start_date, todate=end_date)
    cerebro.adddata(holding_signal)
    data_collection = []
    for i in stock_collection.values():
        data_collection.append(bt.feeds.PandasData(dataname=i, fromdate=start_date, todate=end_date))
    for i in data_collection:
        cerebro.adddata(i)


    # cyb_etf_data = bt.feeds.PandasData(dataname=cyb_etf, fromdate=start_date, todate=end_date)
    # hs300_etf_data=bt.feeds.PandasData(dataname=hs300_etf, fromdate=start_date, todate=end_date)
    # ndaq_etf_data=bt.feeds.PandasData(dataname=ndaq_etf, fromdate=start_date, todate=end_date)
    # gold_etf_data=bt.feeds.PandasData(dataname=gold_etf, fromdate=start_date, todate=end_date)
    #
    # holding_signal=MyData(dataname=holding_df, fromdate=start_date, todate=end_date)
    #
    # # hs_300 =bt.feeds.PandasData(dataname=hs_300, fromdate=start_date, todate=end_date)
    #
    # cerebro.adddata(cyb_etf_data)
    # cerebro.adddata(hs300_etf_data)
    # cerebro.adddata(ndaq_etf_data)
    # cerebro.adddata(gold_etf_data)
    #
    # cerebro.adddata(holding_signal)
    # cerebro.addanalyzer(TradeRecorder, _name='trade_recorder')
    cerebro.addanalyzer(MyAnalyzer, _name='log')
    cerebro.broker.setcash(1000000.0)
    cerebro.broker.setcommission(commission=0.0001)
    res = cerebro.run()
    # # cerebro.plot()
    # z=res[0].analyzers.log.get_analysis()

    # res2={}
    # for i in range(0,len(res)):
    #     res2[i]=res[i][0].analyzers.log.get_analysis()
    # import pickle
    # with open('茅台——国债动量配对.pickle', 'wb') as f:
    #     pickle.dump(res2, f)
    # z['log_df'].loc[:,'value'].plot()
    # plt.show()








