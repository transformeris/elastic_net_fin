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
def max_rolling_returns(stock_df):
    """
    计算股票过去10、20、30、40、50天的收益率，并取其最大值
    symbol: 股票代码
    start_date: 开始日期
    """
    # 获取历史行情数据
    # stock_df = ak.stock_zh_a_hist(symbol=symbol, start_date=start_date)

    # 计算收益率
    returns = stock_df['close'].pct_change()

    # 计算滚动收益率
    rolling_returns = returns.rolling(window=10).max()

    # 取最大值
    max_return = rolling_returns.max()

    # 将结果添加到DataFrame中
    result_df = pd.DataFrame(max_return)

    # 将结果与历史行情数据合并
    result_df = pd.concat([stock_df, result_df], axis=1)

    return result_df





if __name__ == '__main__':

    etf1_data = ak.fund_etf_hist_em(symbol='159915', adjust='qfq')

    etf2_data = ak.stock_zh_index_daily_em(symbol='sh000013')
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

    # data=max_rolling_returns(etf1_data)

    signals_df = pd.DataFrame(index=etf1_data.index)
    signals_df['signal'] = pd.Series(np.where(etf1_pct_change > etf2_pct_change, 'buy_etf1', 'buy_etf2'),
                                     index=etf1_data.index)
    signals_df['holding'] = pd.Series(np.where(etf1_pct_change > etf2_pct_change, 'etf1', 'etf2'),
                                      index=etf1_data.index)

    signals_df['change_position'] = signals_df['holding'].shift(1) != signals_df['holding']

    maotai_df = etf1_data
    # 计算收益率
    returns = maotai_df['close'].pct_change(periods=20)
    etf1_data['return_20']=etf1_data['close'].pct_change(periods=20)
    etf1_data['return_40']=etf1_data['close'].pct_change(periods=40)
    etf1_data['return_60']=etf1_data['close'].pct_change(periods=60)

    etf2_data['return_20']=etf2_data['close'].pct_change(periods=20)
    etf2_data['return_40']=etf2_data['close'].pct_change(periods=40)
    etf2_data['return_60']=etf2_data['close'].pct_change(periods=60)

    tiaochangzhouqi=5
    etf1=etf1_data
    etf2=etf2_data
    start_date= '2010-01-01'
    end_date= '2021-01-01'
    etf1_data=etf1_data.loc[start_date:end_date,:]
    etf2_data=etf2_data.loc[start_date:end_date,:]
    # etf1_data.to_excel('etf1_data.xlsx')
    # etf2_data.to_excel('etf2_data.xlsx')
    signals_df=signals_df.loc[start_date:end_date,:]
    etf1_resample_f=etf1_data.resample('M').first()
    etf1_resample_l=etf1_data.resample('M').last()
    etf2_resample_f=etf2_data.resample('M').first()
    etf2_resample_l=etf2_data.resample('M').last()




    etf1_yuedushouyi=((etf1_resample_l.loc[:,'close']-etf1_resample_f.loc[:,'close'])/etf1_resample_f.loc[:,'close'])

    etf2_yuedushouyi=((etf2_resample_l.loc[:,'close']-etf2_resample_f.loc[:,'close'])/etf2_resample_f.loc[:,'close'])

    etf1_pre=etf1_resample_f.loc[:,'close'].shift(1)

    best_holding = pd.Series(np.where(etf1_yuedushouyi > etf2_yuedushouyi, 'etf1', 'etf2'),
                                      index=etf1_yuedushouyi.index)
    # best_holding=best_holding

    best_return20_select=pd.Series(np.where(etf1_resample_l['return_20'] > etf2_resample_l['return_20'], 'etf1', 'etf2'),
                                      index=etf1_resample_l['return_20'].index).shift(1)

    best_return40_select = pd.Series(
        np.where(etf1_resample_l['return_40'] > etf2_resample_l['return_40'], 'etf1', 'etf2'),
        index=etf1_resample_l['return_40'].index).shift(1)


    date_list=list(best_holding.index)
    res=pd.Series(index=best_holding.index)
    for i in date_list:
        if best_holding[i]==best_return20_select[i] and best_holding[i]!=best_return40_select[i]:
            res[i]='return_20'
        elif best_holding[i]!=best_return20_select[i] and best_holding[i]==best_return40_select[i]:
            res[i]='return_40'
        elif best_holding[i]==best_return20_select[i] and best_holding[i]==best_return40_select[i]:
            res[i]='return_20'
        elif best_holding[i]!=best_return20_select[i] and best_holding[i]!=best_return40_select[i]:
            res[i]='null'
    res=res.shift(1)
    holding=pd.Series(index=best_holding.index)
    date_list = list(best_holding.index)
    for i in list(res.index):
        if res[i]=='return_20':
            holding[i]=best_return20_select[i]
        elif res[i]=='return_40':
            holding[i]=best_return40_select[i]
        elif res[i]=='null':
            holding[i]='etf2'
    holding_real=holding.shift(1)

    # shouyi={}
    # for i,j in holding.items():
    #     if j=='etf1':
    #         shouyi[i]=etf1_yuedushouyi[i]
    #     elif j=='etf2':
    #         shouyi[i]=etf2_yuedushouyi[i]



    # signals_df.to_csv('signal_df.csv')

    # data1 = bt.feeds.PandasData(dataname=etf1_data)
    # data2 = bt.feeds.PandasData(dataname=etf2_data)
    #
    # cerebro.adddata(data1)
    # cerebro.adddata(data2)
    #
    # cerebro.broker.setcash(100000.0)
    # cerebro.broker.setcommission(commission=0.001)
    #
    # print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # cerebro.run()
    # print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())


