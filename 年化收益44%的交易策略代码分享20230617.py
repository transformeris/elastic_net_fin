import backtrader as bt
import akshare as ak
import pandas as pd
import datetime
import json
import warnings
import numpy as np



if __name__ == '__main__':
    # cerebro = bt.Cerebro()
    # cerebro.addstrategy(ETFBacktest)
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

    # 计算涨跌幅
    etf1_pct_change = etf1_data['close'].pct_change(21)
    etf2_pct_change = etf2_data['close'].pct_change(21)

    # 生成交易信号和持仓品种
    signals_df = pd.DataFrame(index=etf1_data.index)
    signals_df['signal'] = pd.Series(np.where(etf1_pct_change > etf2_pct_change, 'buy_etf1', 'buy_etf2'),
                                     index=etf1_pct_change.index)
    signals_df['holding'] = pd.Series(np.where(etf1_pct_change > etf2_pct_change, 'etf1', 'etf2'),
                                      index=etf1_pct_change.index)


