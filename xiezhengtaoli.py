import datetime
import seaborn as sns
import tqdm
from hmmlearn import hmm
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import akshare as ak
import statsmodels.api as sm
import itertools
import seaborn as sns
data_proto=ak.stock_zh_index_daily(symbol="sh000300")
data = ak.stock_zh_index_daily(symbol="sh000300")
close=data['close']
from statsmodels.tsa.stattools import adfuller
import numpy as np
import pandas as pd
import pickle
def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def set_date_index(data):
    pass

adf_test = adfuller(close, autolag='AIC')

diff1 = close.diff(1).dropna()  # 1阶差分
adftest_diff1 = adfuller(diff1,autolag = 'AIC')
# adf_test_output = pd.Series(adftest[0:4],
#                             index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
#
# for key, value in adf_test[4].items():
#     　adf_test_output['Critical Value (%s)' % key] = value
# 　　  print(adf_test_output)


z=pd.read_excel('指数列表格 .xlsx')
stock_zh_index_spot_df = ak.stock_zh_index_spot()

stock_pair=load_obj('jieguo')

zh_index=load_obj('指数日k')
stock1=zh_index[stock_pair[638][0]]
stock2=zh_index[stock_pair[638][1]]
stock1.set_index('date',inplace=True)
stock2.set_index('date',inplace=True)
x = stock1['close']

y =stock2['close']

# plt.plot(x)
# plt.plot(y)
# plt.show()


date_public=set(x.index)&set(y.index)
stock1_1=x[date_public].sort_index()
stock2_1=y[date_public].sort_index()

stock1_1_1=stock1_1[min(stock1_1.index):datetime.date(2019,1,1)]
stock2_1_1=stock2_1[min(stock2_1.index):datetime.date(2019,1,1)]
# x=x[min(stock1_1.index):datetime.date(2019,1,1)]
# y=y[min(stock1_1.index):datetime.date(2019,1,1)]
x=x[datetime.date(2015,1,1):datetime.date(2019,1,1)]
y=y[datetime.date(2015,1,1):datetime.date(2019,1,1)]
X = sm.add_constant(x)

result = (sm.OLS(y,X)).fit()

print(result.summary())

plt.plot(X,y,'o')
plt.show()
# zhishu={}
# for i in stock_zh_index_spot_df['代码']:
#     print(i)
#     zhishu[i]=ak.stock_zh_index_daily(symbol=i)
# save_obj(zhishu,'指数日k')

# zhishu=load_obj('指数日k')
# pair=[]
# desh=list(stock_zh_index_spot_df['代码'])
#
#
#
# for i in tqdm.tqdm(itertools.combinations(desh,2)):
#     print(i)
#     # stock_zh_index_daily_df1 = ak.stock_zh_index_daily(symbol="sh000300")
#     #
#     # stock_zh_index_daily_df2 = ak.stock_zh_index_daily(symbol="sh000001")
#     stock_zh_index_daily_df1=zhishu[i[0]]
#     stock_zh_index_daily_df2 = zhishu[i[1]]
#     try:
#         stock_zh_index_daily_df1.set_index('date',inplace=True)
#
#     except:
#         pass
#     try:
#         stock_zh_index_daily_df2.set_index('date', inplace=True)
#     except:
#         pass
#     stock1=stock_zh_index_daily_df1['close']
#     stock2=stock_zh_index_daily_df2['close']
#
#
#     # result = sm.tsa.stattools.coint(stock1, stock2)
#
#
#     date_public=set(stock1.index)&set(stock2.index)
#     stock1_1=stock1[date_public].sort_index()
#     stock2_1=stock2[date_public].sort_index()
#
#     stock1_1_1=stock1_1[min(stock1_1.index):datetime.date(2019,1,1)]
#     stock2_1_1=stock2_1[min(stock2_1.index):datetime.date(2019,1,1)]
#
#     l1=len(stock1_1_1)
#     l2=len(stock2_1_1)
#     if l1==0 or l2==0:
#         continue
#     result = sm.tsa.stattools.coint(stock1_1_1, stock2_1_1)
#     pvalue = result[1]
#     if pvalue<0.05:
#         pair.append([i[0],i[1],pvalue])