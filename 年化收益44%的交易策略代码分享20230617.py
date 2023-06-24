import backtrader as bt
import akshare as ak
import pandas as pd
import datetime
import json
import warnings
import numpy as np

class ETFBacktest(bt.Strategy):
    params = (
        ('etf1', '159915'),  # etf1代码
        ('etf2', '512890'),  # etf2代码
        ('etf1_weight', 100),  # etf1权重
        ('etf2_weight', 100),  # etf2权重
        ('printlog', False),
    )

    def __init__(self):
        self.etf1 = self.datas[0]
        self.etf2 = self.datas[1]
        self.holding_etf = None
        self.etf1_weight = self.params.etf1_weight
        self.etf2_weight = self.params.etf2_weight
        self.signal_df = pd.read_csv('signal_df.csv', index_col=0, parse_dates=True)

    def next(self):
        if pd.Timestamp(self.data.datetime.date(0)) in self.signal_df.index:
            signal = self.signal_df.loc[pd.Timestamp(self.data.datetime.date(0)), 'change_position']
            holding= self.signal_df.loc[pd.Timestamp(self.data.datetime.date(0)), 'holding']
            etf_type = self.signal_df.loc[pd.Timestamp(self.data.datetime.date(0)), 'holding']
            if signal:

                self.holding = holding
                if self.holding_etf == 'etf2':
                    print(signal, self.holding_etf)
                    self.order_target_percent(self.etf2, target=0)
                    self.order_target_percent(self.etf1, target=1)
                    self.holding_etf = 'etf1'
                elif self.holding_etf == 'etf1':
                    self.order_target_percent(self.etf1, target=0)
                    self.order_target_percent(self.etf2, target=1)
                    self.holding_etf = 'etf2'
                # self.order_target_percent(self.etf1, target=self.etf1_weight if self.holding_etf == 'etf2' else 0)
                # self.order_target_percent(self.etf2, target=self.etf2_weight if self.holding_etf == 'etf1' else 0)

    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

if __name__ == '__main__':
    cerebro = bt.Cerebro(tradehistory=True)
    cerebro.addstrategy(ETFBacktest)
    etf1_data = ak.fund_etf_hist_em(symbol='159915', adjust='qfq')
    etf2_data = ak.fund_etf_hist_em(symbol='512890', adjust='qfq')
    etf1_data.rename(
        columns={'日期': 'date', '收盘': 'close', '开盘': 'open', '最高': 'high', '最低': 'low', '成交量': 'volume', '成交额': 'amount',
                 '振幅': 'amplitude', '涨跌幅': 'pct_change'}, inplace=True)
    etf2_data.rename(
        columns={'日期': 'date', '收盘': 'close', '开盘': 'open', '最高': 'high', '最低': 'low', '成交量': 'volume', '成交额': 'amount',
                 '振幅': 'amplitude', '涨跌幅': 'pct_change'}, inplace=True)

    etf1_data.set_index(pd.to_datetime(etf1_data.loc[:, 'date']), inplace=True)
    etf2_data.set_index(pd.to_datetime(etf2_data.loc[:, 'date']), inplace=True)

    etf1_data, etf2_data = etf1_data.align(etf2_data, join='inner')
    # 计算涨跌幅
    etf1_pct_change = etf1_data['close'].pct_change(periods=25)
    etf2_pct_change = etf2_data['close'].pct_change(periods=25)

    signals_df = pd.DataFrame(index=etf1_data.index)
    signals_df['signal'] = pd.Series(np.where(etf1_pct_change > etf2_pct_change, 'buy_etf1', 'buy_etf2'),
                                     index=etf1_data.index)
    signals_df['holding'] = pd.Series(np.where(etf1_pct_change > etf2_pct_change, 'etf1', 'etf2'),
                                      index=etf1_data.index)

    signals_df['change_position'] = signals_df['holding'].shift(1) != signals_df['holding']
    # signals_df.to_csv('signal_df.csv')

    data1 = bt.feeds.PandasData(dataname=etf1_data)
    data2 = bt.feeds.PandasData(dataname=etf2_data)

    cerebro.adddata(data1)
    cerebro.adddata(data2)

    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

