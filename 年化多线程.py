import pickle
import pandas as pd
import matplotlib.pyplot as plt
# with open('res2.pickle','rb') as f:
#     res2=pickle.load(f)
# with open('res21.pickle','rb') as f:
#     res21=pickle.load(f)
#
# res={}
# res.update(res2)
# res.update(res21)
with open('茅台——国债动量配对.pickle','rb') as f:
    res21=pickle.load(f)
value_list=[]
for i in range(0,len(res21)):
    value_list.append(res21[i]['log_df']['value'])
value=pd.concat(value_list,axis=1)
# plt.plot(value.iloc[3281:,:])
# plt.show()
# value.to_excel('value.xlsx')
#最大回撤
import numpy as np

def max_drawdown(net_values):
    """
    计算最大回撤
    p: 价格时间序列
    """
    if len(net_values) == 0:
        return 0

    # 计算净值曲线


    # 计算每个时间点之前的最高净值
    max_net_values = np.maximum.accumulate(net_values)

    # 计算每个时间点的回撤
    drawdowns = (max_net_values - net_values) / max_net_values

    # 计算最大回撤
    max_drawdown = np.max(drawdowns)

    return max_drawdown


dd=max_drawdown(np.array(value.iloc[:,0]))
max_dd=[]
for i in range(0,3000):

    dd=max_drawdown(np.array(value.iloc[:,i]))
    max_dd.append(dd)

#
#
#
#
