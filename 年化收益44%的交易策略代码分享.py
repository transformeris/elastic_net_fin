import backtrader as bt
import akshare as ak
import pandas as pd
import datetime
import json
import warnings

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
        ('etf1', '510050.SH'), # 创成长ETF
        ('etf2', '510880.SH'), # 红利低波ETF
        ('period', 25), # 计算涨跌幅的周期
        ('rebalance_days', 1), # 调仓周期
        ('commission', 0.0001),  # 手续费
        ('rsrs_threshold', 0)  # RSRS指标阈值
    )

    def __init__(self):
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analyzer')
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        cerebro.addanalyzer(bt.analyzers.SharpeRatio_A, _name='sharpe')
        self.etf1 = self.datas[0]
        print('cusk',etf1_data)
        self.etf2 = self.datas[1]
        self.rebalance_counter = 0

        self.log_returns = []
        self.log_df = pd.DataFrame(columns=['date', 'etf1_position', 'etf2_position', 'total_position', 'cash'])
        self.rsrs = RSRS(self.etf1.close, period=self.params.period)
        self.zscore = (self.rsrs - pd.Series(self.rsrs)) / bt.indicators.StandardDeviation(self.rsrs)
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analyzer')
        self.trade_type = None


    def record_trade(self):
        if abs(self.zscore[0]) < 0.1 and self.trade_type != 'none':
            if self.trade_type == 'long':
                self.trade_pnl = (self.etf1.close[0] - self.trade_price) * self.trade_size - self.trade_commission
            elif self.trade_type == 'short':
                self.trade_pnl = (self.trade_price - self.etf2.close[0]) * self.trade_size - self.trade_commission
            self.trade_dict['date'].append(self.trade_date)
            self.trade_dict['type'].append(self.trade_type)
            self.trade_dict['size'].append(self.trade_size)
            self.trade_dict['price'].append(self.trade_price)
            self.trade_dict['commission'].append(self.trade_commission)
            self.trade_dict['pnl'].append(self.trade_pnl)
            self.trade_size = None
            self.trade_price = None
            self.trade_type = None
            self.trade_date = None
            self.trade_commission = None
            self.trade_pnl = None

    def next(self):
        if self.rebalance_counter == self.params.rebalance_days:
            self.rebalance_counter = 0
            etf1_returns = self.calculate_returns(self.etf1)
            etf2_returns = self.calculate_returns(self.etf2)
            if self.rsrs[0] > self.params.rsrs_threshold:
                if etf1_returns > etf2_returns:
                    self.order_target_percent(self.etf2, target=0)
                    self.order_target_percent(self.etf1, target=1.0)


                else:
                    self.order_target_percent(self.etf1, target=0)
                    self.order_target_percent(self.etf2, target=1.0)

                    self.trade_size = int(self.broker.getcash() / self.etf2.close[0])
                    self.trade_price = self.etf2.close[0]
                    self.trade_type = 'short'
                    self.trade_date = self.data.datetime.date(0)
                    self.trade_commission = self.trade_size * self.trade_price * self.params.commission
            else:
                self.order_target_percent(self.etf1, target=0)
                self.order_target_percent(self.etf2, target=0)
                self.record_trade()
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
        trades = pd.DataFrame.from_dict(self.trade_dict)
        trades.set_index('date', inplace=True)
        trades.to_csv('trades.csv')
        # self.log_df.to_csv('backtest_log.csv', index=False)
        # returns = self.broker.getvalue() / self.broker.getcash() - 1.0
        # max_drawdown = self.analyzers.drawdown.get_analysis()['max']['drawdown']
        # trade_analyzer = self.analyzers.trade_analyzer.get_analysis()
        # # sharpe_dict = self.analyzers.sharpe.get_analysis()
        # sharpe_dict = self.analyzers.sharpe.get_analysis()
        # print(trade_analyzer)
        # # sharpe_ratio = self.analyzers.sharpe.get_analysis()['len']
        # # sharpe_ratio = self.analyzers.Sharpe.get_analysis()['len']
        # # information_ratio = self.stats.inforatio.get_analysis()['rnorm100']
        # # win_rate = self.stats.won.total / self.stats.len.total
        #
        # # 将回测指标转换为JSON格式
        # results = {
        #     'returns': returns,
        #     'max_drawdown': max_drawdown,
        #     # 'sharpe_ratio': sharpe_ratio,
        #     # 'information_ratio': information_ratio,
        #     # 'win_rate': win_rate
        # }
        # results_json = json.dumps(results)
        # print(results_json)
        #
        # # 将JSON格式的回测指标写入文件中
        # with open('backtest_results.json', 'w') as f:
        #     f.write(results_json)



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

    start_date = datetime.datetime(2018, 1, 1)
    end_date = datetime.datetime(2023, 12, 31)
    etf1_data = bt.feeds.PandasData(dataname=etf1_data, fromdate=start_date, todate=end_date)
    etf2_data = bt.feeds.PandasData(dataname=etf2_data, fromdate=start_date, todate=end_date)
    cerebro.adddata(etf1_data)
    cerebro.adddata(etf2_data)
    cerebro.broker.setcash(1000000.0)
    cerebro.run()
    cerebro.plot()

    # cerebro.plot(data0=etf1_data, data1=etf2_data)