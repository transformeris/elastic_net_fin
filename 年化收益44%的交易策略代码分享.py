import backtrader as bt
import akshare as ak
import pandas as pd
import datetime
import warnings
class ETFBacktest(bt.Strategy):
    params = (
        ('etf1', '510050.SH'), # 创成长ETF
        ('etf2', '510880.SH'), # 红利低波ETF
        ('period', 21), # 计算涨跌幅的周期
        ('rebalance_days', 1), # 调仓周期
        ('commission', 0.00001)  # 手续费
    )

    def __init__(self):
        self.etf1 = self.datas[0]
        self.etf2 = self.datas[1]
        self.rebalance_counter = 0
        self.log_returns = []
        self.log_df = pd.DataFrame(columns=['date', 'etf1_position', 'etf2_position', 'total_position', 'cash'])


    def next(self):
        if self.rebalance_counter == self.params.rebalance_days:
            self.rebalance_counter = 0
            etf1_returns = self.calculate_returns(self.etf1)
            etf2_returns = self.calculate_returns(self.etf2)
            if etf1_returns > etf2_returns:
                self.order_target_percent(self.etf2, target=0)
                self.order_target_percent(self.etf1, target=1.0)
            else:
                self.order_target_percent(self.etf1, target=0)
                self.order_target_percent(self.etf2, target=1.0)
        self.rebalance_counter += 1
        self.log_returns.append([self.datas[0].datetime.date(0), self.calculate_returns(self.etf1), self.calculate_returns(self.etf2),self.log_returns])
        # 计算持仓股、份额、账户总份额和现金等信息
        position_etf1 = self.getposition(self.etf1).size
        position_etf2 = self.getposition(self.etf2).size
        total_position = position_etf1 + position_etf2
        cash = self.broker.get_cash()
        date = self.datas[0].datetime.date(0)
        calculate_returns_etf1 = self.calculate_returns(self.etf1)
        calculate_returns_etf2 = self.calculate_returns(self.etf2)

        # 将信息添加到log_df中
        self.log_df = self.log_df.append({'date': date, 'etf1_position': position_etf1, 'etf2_position': position_etf2,
                                          'total_position': total_position, 'cash': cash,'calculate_returns_etf1':calculate_returns_etf1,'calculate_returns_etf2':calculate_returns_etf2}, ignore_index=True)
    def calculate_returns(self, data):
        returns = (data.close[0] - data.close[-self.params.period]) / data.close[-self.params.period]
        return returns

    def stop(self):
        self.log_df.to_csv('backtest_log.csv', index=False)

if __name__ == '__main__':
    cerebro = bt.Cerebro()
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

    start_date = datetime.datetime(2022, 1, 1)
    end_date = datetime.datetime(2022, 12, 31)
    etf1_data = bt.feeds.PandasData(dataname=etf1_data, fromdate=start_date, todate=end_date)
    etf2_data = bt.feeds.PandasData(dataname=etf2_data, fromdate=start_date, todate=end_date)
    cerebro.adddata(etf1_data)
    cerebro.adddata(etf2_data)
    cerebro.broker.setcash(1000000.0)
    cerebro.run()
    cerebro.plot()

    # cerebro.plot(data0=etf1_data, data1=etf2_data)