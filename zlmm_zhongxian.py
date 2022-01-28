# -*- coding: utf-8 -*-
import datetime
import time
import numpy as np
from sqlalchemy.sql import func
import pandas as pd
import math
from pandas import DataFrame
import akshare as ak
import talib
from chinese_calendar import is_workday
import chinese_calendar
# def SMA(vals, n, m) :
#     # 算法1
#     return (lambda x, y: ((n - m) * x + y * m) / n, vals)
# code= ak.stock_zh_index_spot
def zhibiao():
    #data=pd.read_csv('天华超净daily.csv',index_col=0)
    data = ak.stock_zh_index_daily_em(symbol='sh000300')
    # data=ak.stock_zh_a_hist(symbol='300390',adjust='hfq')
    data.rename(columns={'open':'开盘', 'high':'最高', 'low':'最低','close':'收盘','volume':'成交量'}, inplace = True)
    data['日期']=data.index
    data=data.set_index(['date'])
    data['日期']=data.index
    var1=(data['最高']+data['最低']+data['收盘'])/3
    data2=data.shift(1)

    var2_pre=((var1-data2['最低'])-(data['最高']-var1))*data['成交量']/100000/(data['最高']-data['最低'])




    var2_pre=var2_pre.replace([np.inf, -np.inf], np.nan)
    var2_pre=var2_pre.dropna()
    # var2_pre=var2_pre.round(decimals=2)
    date_start='2005-01-05'
    t = time.strptime(date_start, "%Y-%m-%d")
    y, m, d = t[0:3]
    # df[~df.isin([inf]).any(1)]
    var2=var2_pre.cumsum(axis='index')
    # res={}
    # var2_0= {}
    # for i in range(1,len(var2_pre)):
    #     # zzz=var2_pre.truncate(after=i,axis="rows")
    #     # zzzz=zzz.drop(i)
    #     zzz=var2_pre[0:i]
    #     res[list(var2_pre.index)[i-1]]=sum(zzz)
    #     a=list(var2_pre.index)[i-1]
    #     var2_0[data['日期'].iloc[a]]=sum(zzz)
    #
    # var2=pd.DataFrame(var2_0,index=[0]).T
    var3=var2.ewm(span=1,adjust=False).mean()
    jcs=var2.ewm(span=1,adjust=False).mean()
    jcm=var3.rolling(window=12).mean()
    jcl=var3.rolling(window=26).mean()


    lc=data2['收盘']
    data3=data.set_index(['日期'])
    data2=data3.shift(1)
    lc=data2['收盘']
    aa=(data3['收盘']-data2['收盘'])
    aa[aa<0]=0
    bb=abs(data3['收盘']-data2['收盘'])
    # zz=SMA(aa,12,1)
    zzz={}
    sma_12_1=aa.ewm(span=2*12/1-1).mean()
    rsi2=talib.RSI(data3['收盘'],12)
    rsi3=talib.RSI(data3['收盘'],18)
    sma_16_1=aa.ewm(span=2*16/1-1).mean()
    sma_abs_16_1=bb.ewm(span=2*16/1-1).mean()
    mms_pre=3*rsi2-2*sma_16_1/sma_abs_16_1*100
    mms=talib.MA(mms_pre,3)
    mmm=talib.EMA(mms,8)
    sma_12_1=aa.ewm(span=2*12/1-1).mean()
    sma_abs_12_1=bb.ewm(span=2*12/1-1).mean()
    mml_pre=3*rsi3-2*sma_12_1/sma_abs_12_1*100
    mml=talib.MA(mml_pre,5)
    return data,jcs,jcm,jcl,mms,mmm,mml

def huiche(data,date_buy,date_sell):
    for i in list(data.index):
        if i in date_buy:
            data.loc[i, '收盘信号'] = 1
        if i in date_sell:
            data.loc[i, '收盘信号'] = 0

    data['当天仓位'] = data['收盘信号'].shift(1)
    data['当天仓位'].fillna(method='ffill', inplace=True)
    data['ret'] = data['收盘'] / data['收盘'].shift(1) - 1
    from datetime import datetime, timedelta

    d = datetime.strptime(data[data['当天仓位'] == 1].index[0], '%Y-%m-%d') - timedelta(days=1)
    d = d.strftime('%Y-%m-%d')
    df_new = data.loc[d:]
    df1=data[3000:]
    df1['ret'][0] = 0
    df1['当天仓位'][0] = 0
    df1['资金指数'] = (df1.ret * data['当天仓位'] + 1.0).cumprod()
    df1['指数净值'] = (df1.ret + 1.0).cumprod()

    df1['策略净值'] = (df1.ret * df1['当天仓位'] + 1.0).cumprod()
    df1['指数净值'] = (df1.ret + 1.0).cumprod()
    df1['策略收益率'] = df1['策略净值'] / d
    return df_new


if __name__=='__main__':
    data,jcs, jcm, jcl, mms, mmm, mml=zhibiao()
    bias_jc_s_m = ((jcs - jcm) / jcm) * 100
    bias_jc_s_l = ((jcs - jcl) / jcl) * 100
    data_buy=[]
    jc_kongkou=[]
    for i in jcs.index:
        if jcs[i]<jcm[i] and jcs[i]<jcl[i] and jcm[i]<jcl[i]:
            jc_kongkou.append(i)
    jcm_delta = jcm.diff()
    jcl_delta = jcl.diff()
    jcs_delta=jcs.diff()
    mm_duanxian_buy=[]
    for i in range(1,len(mms)):
        if (mms.iloc[i]>mmm.iloc[i] and mms.iloc[i-1]<mmm.iloc[i-1]) and (mms.iloc[i]>mml.iloc[i] and mms.iloc[i-1]<mml.iloc[i-1]) and jcs_delta[i]>0 and jcm_delta[i]>0 and jcl_delta[i]>0:
            mm_duanxian_buy.append(mms.index[i])


    mm_duanxian_sell=[]
    for i in range(1,len(mms)):
        if (mms.iloc[i]<mmm.iloc[i] and mms.iloc[i-1]>mmm.iloc[i-1]):
            mm_duanxian_sell.append(mms.index[i])
    for i in jc_kongkou:
        mm_duanxian_sell.append(i)




    for i in list(data.index):
        if i in mm_duanxian_buy:
            data.loc[i, '收盘信号'] = 1
        if i in mm_duanxian_sell:
            data.loc[i, '收盘信号'] = 0

    data['当天仓位'] = data['收盘信号'].shift(1)
    data['当天仓位'].fillna(method='ffill', inplace=True)
    data['ret'] = data['收盘'] / data['收盘'].shift(1) - 1
    from datetime import datetime, timedelta

    d = datetime.strptime(data[data['当天仓位'] == 1].index[0], '%Y-%m-%d') - timedelta(days=1)
    d = d.strftime('%Y-%m-%d')
    df_new = data.loc[d:]
    df_new['ret'][0] = 0
    df_new['当天仓位'][0] = 0
    df_new['资金指数'] = (df_new.ret * data['当天仓位'] + 1.0).cumprod()
    df_new['指数净值'] = (df_new.ret + 1.0).cumprod()
    df1 = data[0:]
    df1['策略净值'] = (df1.ret * df1['当天仓位'] + 1.0).cumprod()
    df1['指数净值'] = (df1.ret + 1.0).cumprod()
    df1['策略收益率'] = df1['策略净值'] / df1['策略净值'].shift(1) - 1
    df1['指数收益率'] = df1.ret

    import matplotlib.pyplot as plt

    # plt.plot(data['收盘'])
    data = data[2500:3000]
    data['收盘'].plot(figsize=(16, 7))
    # plt.annotate('买', xy=(np.datetime64(data.index[i]), data['收盘'][i]), arrowprops=dict(facecolor='r', shrink=0.05))
    for i in range(len(data)):
        if data['收盘信号'][i] == 1:
            plt.annotate('买', xy=(i, data['收盘'][i]), arrowprops=dict(facecolor='r', shrink=0.05))
        if data['收盘信号'][i] == 0:
            plt.annotate('卖', xy=(i, data['收盘'][i]), arrowprops=dict(facecolor='g', shrink=0.1))

    plt.title('上证指数2000-2019年MFI买卖信号', size=15)
    plt.xlabel('')
    ax = plt.gca()
    # ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    plt.show()