from hmmlearn import hmm
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import akshare as ak
n = 6  # 6个隐藏状态
# stock_zh_index_daily_df = ak.stock_zh_index_daily_dfck_zh_index_daily(symbol="sh000300")
# data = pd.read_csv('沪深300.csv', index_col=0)
data_proto=ak.stock_zh_index_daily(symbol="sh000300")
data = ak.stock_zh_index_daily(symbol="sh000300")

trade_back=[3665,3915]

data=data_proto[721:]
data.set_index(data['date'],inplace=True)
volume = data['volume']
close = data['close']

logDel = np.log(np.array(data['high'])) - np.log(np.array(data['low']))
logRet_1 = np.array(np.diff(np.log(close)))
logRet_5 = np.log(np.array(close[5:])) - np.log(np.array(close[:-5]))
logVol_5 = np.log(np.array(volume[5:])) - np.log(np.array(volume[:-5]))

# 保持所有的数据长度相同
logDel = logDel[5:]
logRet_1 = logRet_1[4:]
close = close[5:]

Date = pd.to_datetime(data.index[5:])
A = np.column_stack([logDel, logRet_5, logVol_5])

# zz=np.count_nonzero(A)

for i in range(3665,3915):
    A_hist=A[0:3665]

    model = hmm.GaussianHMM(n_components=n, covariance_type="full", n_iter=2000).fit(A_hist)
    hidden_states = model.predict(A)
