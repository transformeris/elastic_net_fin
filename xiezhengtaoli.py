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
def single_stock_tradeback(stock_code,etf_kline,money,trade_pay_rate,start_date,end_date):

    '''

    :param stock_code:  str  股票代码，例：'sz159966'
    :param etf_kline:  dict  全部etf基金k线，
    :param money: float  初始买入成本，包含手续费
    :param trade_pay_rate: float，手续费费率，【0-1】
    :param start_date: date   回测开始日期，
    :param end_date: date   回测结束日期，
    :return: pandas.Dataframe  包含净值等信息的
    '''
    etf_kline_stock=etf_kline[stock_code]
    etf_hold = etf_kline_stock[start_date:end_date]
    etf_close = etf_hold['close']
    etf_close_shift = etf_close.shift(1)
    etf_delta = (etf_close - etf_close_shift) / etf_close_shift
    etf_delta = etf_delta.drop(start_date)
    etf_hold['incresing_rate'] = etf_delta
    etf_hold.loc[start_date, 'incresing_rate'] = (etf_hold.loc[start_date, 'close'] - etf_hold.loc[
        start_date, 'open']) / etf_hold.loc[start_date, 'open']
    etf_hold['日增长倍数'] = etf_hold['incresing_rate'] + 1
    etf_hold['净值倍数'] = etf_hold['日增长倍数'].cumprod()
    money_after_trade=money* (1 - trade_pay_rate)
    etf_hold['金额'] = etf_hold['净值倍数'] * money_after_trade
    etf_hold.loc[start_date, '手续费'] = money * trade_pay_rate
    etf_hold.loc[end_date, '手续费'] = etf_hold.loc[end_date, '金额'] * trade_pay_rate

    etf_hold.loc[end_date, '卖出金额_手续费后'] = etf_hold.loc[end_date, '金额'] * (1 - trade_pay_rate)
    return etf_hold,etf_hold.loc[end_date, '金额'] * (1 - trade_pay_rate)


def etf_get():
    etf_list = ak.fund_etf_category_sina(symbol="ETF基金")
    res={}
    res1 = {}
    res2 = {}
    res3 = {}
    res4 = {}
    res5 = {}
    n = 1
    for i in etf_list['symbol']:
        if i == 'sh513200' or i == 'sh513150':
            continue
        print(i)
        print(n)
        fund_etf_hist_sina_df = ak.fund_etf_hist_sina(symbol=i)

        fund_etf_hist_sina_df.set_index(['date'], inplace=True)
        # ma12 = fund_em_etf_fund_info_df['单位净值'].rolling(window=5).mean()
        close = fund_etf_hist_sina_df['close']
        open_etf = fund_etf_hist_sina_df['open']
        high = fund_etf_hist_sina_df['high']
        low = fund_etf_hist_sina_df['low']
        volume = fund_etf_hist_sina_df['volume']
        fund_etf_hist_sina_df=pd.to_numeric(fund_etf_hist_sina_df).sort_index()
        close = pd.to_numeric(close).sort_index()
        open_etf = pd.to_numeric(open_etf).sort_index()
        high = pd.to_numeric(high).sort_index()
        low = pd.to_numeric(low).sort_index()
        volume = pd.to_numeric(volume).sort_index()
        fund_etf_hist_sina_df=fund_etf_hist_sina_df.sort_index()

        close = close.sort_index()
        open_etf = open_etf.sort_index()
        high = high.sort_index()
        low = low.sort_index()
        volume = volume.sort_index()
        # jinzi_delta=jinzi.shift(20)
        # mtm_20=(jinzi-jinzi_delta)/jinzi
        res[i]=fund_etf_hist_sina_df
        res1[i] = close
        res2[i] = open_etf
        res3[i] = high
        res4[i] = low
        res5[i] = volume
        n = n + 1
    save_obj(res, 'etf_all')
    # save_obj(res1, 'etf_close')
    # save_obj(res2, 'etf_open')
    # save_obj(res3, 'etf_high')
    # save_obj(res4, 'etf_low')
    # save_obj(res5, 'etf_volume')

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
x=x[datetime.date(2013,1,1):datetime.date(2019,1,1)]
y=y[datetime.date(2013,1,1):datetime.date(2019,1,1)]
X = sm.add_constant(x)

result = (sm.OLS(y,X)).fit()

print(result.summary())
diff=y-1.3882*x+789.38

mean=np.mean(diff)
std=np.std(diff)

up=mean+std
down=mean-std

stock1_test=stock1_1[datetime.date(2019,1,2):datetime.date(2022,1,1)]
stock2_test=stock2_1[datetime.date(2019,1,2):datetime.date(2022,1,1)]

diff1_1=stock1_test-1.3882*stock2_test+789.38


stock1_test[stock1_test>0]=0
stock1_test[diff1_1>up]=1

stock2_test[stock2_test>0]=0
stock2_test[diff1_1<down]=1

stock1.loc[:,'hold']=stock1_test
stock2.loc[:,'hold']=stock2_test

# plt.plot(X,y,'o')
# plt.show()
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