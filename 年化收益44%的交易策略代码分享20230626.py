import backtrader as bt
import akshare as ak
import pandas as pd
import datetime
import numpy as np



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



class RSRS(bt.Indicator):
    lines = ('rsrs',)
    params = (('period', 30),)

    def __init__(self):
        self.addminperiod(self.params.period)
        self.rolling_window = self.params.period + 1

    def next(self):
        if len(self) < self.rolling_window:
            return
        x = range(self.rolling_window)

        y = self.data.get(size=self.rolling_window)
        x_mean = sum(x) / self.rolling_window
        y_mean = sum(y) / self.rolling_window
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(self.rolling_window))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(self.rolling_window))
        self.lines.rsrs[0] = numerator / denominator


class ETFBacktest(bt.Strategy):
    params = (
        ('growth_etf', '510050.SH'),  # 创成长ETF
        ('dividend_etf', '510880.SH'),  # 红利低波ETF
        ('period', 21),  # 计算涨跌幅的周期
        ('rebalance_days', 1),  # 调仓周期
        ('commission', 0.0001), # 手续费
        ('cheat_on_open', False), # 开盘成交
        ('rsrs_threshold', -1)  # RSRS指标阈值
    )

    def __init__(self):
        self.returns = []
        self.max_drawdown = None
        self.sharpe_ratio = None
        self.information_ratio = None
        self.win_rate = None

        self.growth_etf = self.datas[0]
        self.dividend_etf = self.datas[1]
        # self.hs_300 = self.datas[2]
        self.rebalance_counter = 0

        self.log_returns = []
        self.log_df = pd.DataFrame(columns=[
            'date', 'growth_etf_position', 'dividend_etf_position',
            'total_position', 'cash', 'calculate_returns_growth_etf',
            'calculate_returns_dividend_etf','value'
        ])

        self.rsrs = RSRS(self.growth_etf.close, period=self.params.period)
        self.zscore = (self.rsrs - pd.Series(self.rsrs)) / bt.indicators.StandardDeviation(self.rsrs)

        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analyzer')
        self.trade_type = None

    def next(self):
        """
        This method is called for each new bar (or candle) in the data feed.
        It is used to calculate the RSRS indicator, check if it is above the
        threshold, and place orders accordingly.
        """
        if self.rebalance_counter == self.params.rebalance_days:
            self.rebalance_counter = 0
            growth_etf_returns = self.calculate_returns(self.growth_etf)
            dividend_etf_returns = self.calculate_returns(self.dividend_etf)

            if self.rsrs[0] > self.params.rsrs_threshold:
                if growth_etf_returns > dividend_etf_returns:
                    self.order_target_percent(self.dividend_etf, target=0,price=self.dividend_etf.open[0])
                    self.order_target_percent(self.growth_etf, target=1.0,exectype=bt.Order.Close)

                    self.trade_size = int(self.broker.getcash() / self.growth_etf.close[0])
                    self.trade_price = self.growth_etf.close[0]
                    self.trade_type = 'short'
                    self.trade_date = self.data.datetime.date(0)
                    self.trade_commission = self.trade_size * self.trade_price * self.params.commission

                else:
                    self.order_target_percent(self.growth_etf, target=0,price=self.growth_etf.open[0])
                    self.order_target_percent(self.dividend_etf, target=1.0,exectype=bt.Order.Close)

                    self.trade_size = int(self.broker.getcash() / self.dividend_etf.close[0])
                    self.trade_price = self.dividend_etf.close[0]
                    self.trade_type = 'short'
                    self.trade_date = self.data.datetime.date(0)
                    self.trade_commission = self.trade_size * self.trade_price * self.params.commission
            else:
                self.order_target_percent(self.growth_etf, target=0)
                self.order_target_percent(self.dividend_etf, target=0)

        self.rebalance_counter += 1

        self.log_returns.append([
            self.datas[0].datetime.date(0),
            self.calculate_returns(self.growth_etf),
            self.calculate_returns(self.dividend_etf),
            self.log_returns
        ])

        # 计算持仓股、份额、账户总份额和现金等信息
        growth_etf_position = self.getposition(self.growth_etf).size
        dividend_etf_position = self.getposition(self.dividend_etf).size
        total_position = growth_etf_position + dividend_etf_position
        cash = self.broker.get_cash()
        date = self.datas[0].datetime.date(0)
        calculate_returns_growth_etf = self.calculate_returns(self.growth_etf)
        calculate_returns_dividend_etf = self.calculate_returns(self.dividend_etf)
        value = self.broker.getvalue()

        # 将信息添加到log_df中
        self.log_df = self.log_df.append({
            'date': date,
            'growth_etf_position': growth_etf_position,
            'dividend_etf_position': dividend_etf_position,
            'total_position': total_position,
            'cash': cash,
            'calculate_returns_growth_etf': calculate_returns_growth_etf,
            'calculate_returns_dividend_etf': calculate_returns_dividend_etf,
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


def rename_columns(data):
    data.rename(columns={
        '日期': 'date', '收盘': 'close', '开盘': 'open', '最高': 'high',
        '最低': 'low', '成交量': 'volume', '成交额': 'amount',
        '振幅': 'amplitude', '涨跌幅': 'pct_change'
    }, inplace=True)
    data.set_index(pd.to_datetime(data.loc[:, 'date']), inplace=True)
    return data

if __name__ == '__main__':
    cerebro = bt.Cerebro(tradehistory=True)
    cerebro.addstrategy(ETFBacktest)
    # hs_300=ak.stock_zh_index_daily_em(symbol='sh000300')
    growth_etf_data = ak.fund_etf_hist_em(symbol='159915', adjust='qfq')
    dividend_etf_data = ak.fund_etf_hist_em(symbol='512890', adjust='qfq')
    # dividend_etf_data=ak.fund_etf_hist_sina(symbol='sz159649')
    dividend_etf_data=ak.stock_zh_index_daily_em(symbol='csiH30269')
    '''
    红利低波在15年股市崩溃后出现了50%的回测，如果用国债替代，回测结果应该会更好
    '''
    growth_etf_data=rename_columns(growth_etf_data)
    # hs_300=rename_columns(hs_300)
    zzzzz=ak.stock_zh_index_spot()
    dividend_etf_data=rename_columns(dividend_etf_data)

    start_date = datetime.datetime(2018, 1, 1)
    end_date = datetime.datetime(2023, 12, 31)

    growth_etf_data0=growth_etf_data
    dividend_etf_data0=dividend_etf_data
    growth_etf_data = bt.feeds.PandasData(dataname=growth_etf_data, fromdate=start_date, todate=end_date)
    dividend_etf_data = bt.feeds.PandasData(dataname=dividend_etf_data, fromdate=start_date, todate=end_date)
    # hs_300 =bt.feeds.PandasData(dataname=hs_300, fromdate=start_date, todate=end_date)
    cerebro.adddata(growth_etf_data)
    cerebro.adddata(dividend_etf_data)
    # cerebro.adddata(hs_300)
    cerebro.broker.setcash(1000000.0)
    cerebro.run()
    cerebro.addanalyzer(TradeRecorder, _name='trade_recorder')
    cerebro.addanalyzer(OrderRecorder, _name='order_recorder')


    strat = cerebro.run()[0]

    strategy = cerebro.runstrats[0][0]
    log_df = strategy.get_log_df()
    values=list(log_df.loc[:, 'value'])
    dates=list(log_df.loc[:, 'date'])
    # 计算每个时间点的净值相对于之前的最高净值的回撤值
    max_values = np.maximum.accumulate(values)
    drawdowns = (max_values - values) / max_values

    # 找到回撤值最大的时间点，即最大回撤发生的时间点
    max_drawdown_index = np.argmax(drawdowns)

    # 找到最大回撤发生的开始时间和结束时间
    end_index = max_drawdown_index
    start_index = np.argmax(values[:max_drawdown_index])
    max_drawdown_start_date = dates[start_index]
    max_drawdown_end_date = dates[end_index]

    # 打印结果
    print('Max Drawdown:', drawdowns[max_drawdown_index])
    print('Max Drawdown Start Date:', max_drawdown_start_date)
    print('Max Drawdown End Date:', max_drawdown_end_date)
    trade= strat.analyzers.trade_recorder.trades
    zz=strat.analyzers.order_recorder.orders

    ref_num=[]
    for i in zz:
        ref_num.append(i[1].ref)

    res={}
    for i in set(ref_num):
        res0=[]
        for ii in zz:
            if ii[1].ref==i:
                res0.append(ii)
        res[i]=res0
    cerebro.plot()
