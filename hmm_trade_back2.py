from hmmlearn import hmm
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import akshare as ak
n = 6  # 6个隐藏状态

data_proto=ak.stock_zh_index_daily(symbol="sh000300")
data = ak.stock_zh_index_daily(symbol="sh000300")

data=data_proto[721:3535]
data['number']=np.arange(1,len(data)+1)
data.set_index(data['date'],inplace=True)
volume = data['volume']
close = data['close']

logDel = np.log(np.array(data['high'])) - np.log(np.array(data['low']))
logRet_1 = np.array(np.diff(np.log(close)))
logRet_5 = np.log(np.array(close[5:])) - np.log(np.array(close[:-5]))
logVol_5 = np.log(np.array(volume[5:])) - np.log(np.array(volume[:-5]))

logDel = logDel[5:]
logRet_1 = logRet_1[4:]
close = close[5:]

Date = pd.to_datetime(data.index[5:])
A = np.column_stack([logDel, logRet_5, logVol_5])
date2=data.index[5:]
cheshichangdu=2300
train_collection=A[0:cheshichangdu]
check_collection=A[cheshichangdu+1:len(A)]
model = hmm.GaussianHMM(n_components=n, covariance_type="full", n_iter=2000).fit(train_collection)
hidden_states = model.predict(train_collection)

res = pd.DataFrame({'logReg_1': logRet_1[0:cheshichangdu], 'state': hidden_states})
series = res.logReg_1
souyi=[]
for i in range(n):
    pos = (hidden_states == i)
    pos = np.append(1, pos[:-1])
    res['state_ret%d' % i] = series.multiply(pos)
    data_i = np.exp(res['state_ret%d' % i].cumsum()) #模式i带来的收益倍数
    souyi.append(data_i[len(data_i)-1])
    res['data_i%d' % i]=data_i
moshi=np.flipud(np.argsort(souyi))
chong1=moshi[0]
chong2=moshi[1]
state=res.state
if hidden_states[np.size(state)-1]==chong1 or hidden_states[np.size(state)-1]==chong2:
    data.loc[date2[np.size(state)],'上扬信号']=1
print(len(check_collection))
for i in range(0,len(check_collection)):
    print(i)
    train_collection=A[cheshichangdu+i-1000:cheshichangdu+i]
    model = hmm.GaussianHMM(n_components=n, covariance_type="full", n_iter=2000).fit(train_collection)
    hidden_states = model.predict(train_collection)

    res = pd.DataFrame({'logReg_1': logRet_1[cheshichangdu+i-1000:cheshichangdu+i], 'state': hidden_states})
    series = res.logReg_1
    souyi = []
    for i in range(n):
        pos = (hidden_states == i)
        pos = np.append(1, pos[:-1])
        res['state_ret%d' % i] = series.multiply(pos)
        data_i = np.exp(res['state_ret%d' % i].cumsum())  # 模式i带来的收益倍数
        souyi.append(data_i[len(data_i) - 1])
        res['data_i%d' % i] = data_i
    moshi = np.flipud(np.argsort(souyi))
    chong1 = moshi[0]
    chong2 = moshi[1]
    state = res.state
    if hidden_states[np.size(state) - 1] == chong1 or hidden_states[np.size(state) - 1] == chong2:
        data.loc[date2[np.size(state)], '上扬信号'] = 1








for i in range(2900+1,len(A)):
    pass


