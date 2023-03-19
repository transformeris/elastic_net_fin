import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches
from matplotlib import pyplot as plt
import pandas as pd
import akshare as ak
def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
def backtest_strategy(data, benchmark, commission, slippage, start_date, end_date):
    data = data[(data.index >= start_date) & (data.index <= end_date)]
    benchmark = benchmark[(benchmark.index >= start_date) & (benchmark.index <= end_date)]

    data['daily_return'] = (data['close'] - data['open']) / data['open'] * (1 - commission - slippage)
    data['cumulative_return'] = (1 + data['daily_return']).cumprod()
    data['benchmark_daily_return'] = (benchmark['close'] - benchmark['open']) / benchmark['open']
    data['benchmark_cumulative_return'] = (1 + data['benchmark_daily_return']).cumprod()
    data['excess_return'] = data['cumulative_return'] - data['benchmark_cumulative_return']

    data['drawdown'] = (data['cumulative_return'] / data['cumulative_return'].cummax()) - 1
    max_drawdown = data['drawdown'].min()
    max_drawdown_period = data[data['drawdown'] == max_drawdown].index.tolist()

    annualized_return = data['cumulative_return'][-1] ** (252 / len(data)) - 1
    annualized_benchmark_return = data['benchmark_cumulative_return'][-1] ** (252 / len(data)) - 1
    annualized_excess_return = annualized_return - annualized_benchmark_return

    annualized_volatility = data['daily_return'].std() * np.sqrt(252)
    annualized_benchmark_volatility = data['benchmark_daily_return'].std() * np.sqrt(252)
    sharpe_ratio = (annualized_return - 0.02) / annualized_volatility

    alpha = annualized_excess_return
    plt.figure(figsize=(10, 6))
    plt.plot(data['cumulative_return'], label='策略累计收益')
    plt.plot(data['benchmark_cumulative_return'], label='基准累计收益')
    plt.legend()
    plt.title('策略与基准累计收益')
    plt.savefig('cumulative_return.png', dpi=300)

    doc = Document()
    doc.add_heading('回测报告', 0)
    doc.add_heading('策略表现', level=1)

    doc.add_paragraph(f'策略累计收益: {data["cumulative_return"][-1]:.4f}')
    doc.add_paragraph(f'基准累计收益: {data["benchmark_cumulative_return"][-1]:.4f}')
    doc.add_paragraph(f'策略最大回撤: {max_drawdown:.4f}')
    doc.add_paragraph(f'最大回撤发生时间段: {max_drawdown_period[0]} 至 {max_drawdown_period[-1]}')
    doc.add_paragraph(f'阿尔法收益: {alpha:.4f}')
    doc.add_paragraph(f'夏普比率: {sharpe_ratio:.4f}')
    doc.add_heading('图形展示', level=1)
    doc.add_picture('cumulative_return.png', width=Inches(6))

    doc.save('回测报告.docx')

    return data
if __name__ == '__main__':
    # data = pd.read_csv('data.csv', index_col=0, parse_dates=True)
    # benchmark = pd.read_csv('benchmark.csv', index_col=0, parse_dates=True)
    etf_kline_all = load_obj('etf_all')
    zhengquan_kline = etf_kline_all['sz159905']
    zhengquan_kline.loc[:, 'trade_date'] = zhengquan_kline.index
    pd.to_datetime(zhengquan_kline.loc[:, 'trade_date'])
    zhengquan_kline.set_index(pd.to_datetime(zhengquan_kline.loc[:, 'trade_date']), inplace=True)
    data_proto=zhengquan_kline
    data = zhengquan_kline
    benchmark = zhengquan_kline

    commission = 0.0003
    slippage = 0.0002
    start_date = '2019-01-01'
    end_date = '2020-01-01'

    result = backtest_strategy(data, benchmark, commission, slippage, start_date, end_date)
    print(result)