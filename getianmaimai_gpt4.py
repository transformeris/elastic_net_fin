import pandas as pd
from hmmlearn import hmm
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import akshare as ak
n = 6  # 6个隐藏状态

data_proto=ak.stock_zh_index_daily(symbol="sh000300")
data = ak.stock_zh_index_daily(symbol="sh000300")
# 读取CSV文件
# data = pd.read_csv('your_file.csv')

# 计算每天的收益率（今天以开盘价买入，明天以收盘价卖出）
data['daily_return_rate'] = (data['close'].shift(-1) - data['open']) / data['open']
data.dropna(inplace=True)  # 删除最后一行，因为没有下一天的数据



# 计算每天的复合收益
initial_capital = 10000  # 假设初始资产为10000元
capital_changes_t1 = [initial_capital]
for i in range(len(data)):
    current_capital = capital_changes_t1[-1] * (1 + data.loc[i, 'daily_return_rate'])
    capital_changes_t1.append(current_capital)

# 计算持有股票不买卖时的每天复合收益
data['hold_return_rate'] = data['close'] / data['close'].shift(1)
capital_changes_hold = [initial_capital]
for i in range(1, len(data)):
    current_capital = capital_changes_hold[-1] * data.loc[i, 'hold_return_rate']
    capital_changes_hold.append(current_capital)

# 绘制图形
plt.figure(figsize=(12, 6))
plt.plot(data.index, capital_changes_t1[1:], label='T+1 策略收益')
plt.plot(data.index, capital_changes_hold, label='持有股票收益')
plt.xlabel('日期')
plt.ylabel('资产')
plt.title('T+1策略收益 vs 持有股票收益')
plt.legend()
plt.grid()
plt.show()
