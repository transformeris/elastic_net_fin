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

mm_s_m=mms-mmm
mm_s_m_ref=mm_s_m.shift(1)
mm_s_m_flag=mm_s_m*mm_s_m_ref
mm_s_m_date=list(mm_s_m_flag[mm_s_m_flag<0].index)
mm_s_m_positive=[]
mm_s_m_negative=[]
for i in mm_s_m_date:
    if mm_s_m[i]>0:
        mm_s_m_positive.append(i)
    elif mm_s_m[i]<0:
        mm_s_m_negative.append(i)


mm_m_l=mmm-mml
mm_m_l_ref=mm_m_l.shift(1)
mm_m_l_flag=mm_m_l*mm_m_l_ref
mm_m_l_date=list(mm_m_l_flag[mm_m_l_flag<0].index)
mm_m_l_positive=[]
mm_m_l_negative=[]
for i in mm_m_l_date:
    if mm_m_l[i]>0:
        mm_m_l_positive.append(i)
    elif mm_m_l[i]<0:
        mm_m_l_negative.append(i)

mm_s_l=mms-mml
mm_s_l_ref=mm_s_l.shift(1)
mm_s_l_flag=mm_s_l*mm_s_l_ref
mm_s_l_date=list(mm_s_l_flag[mm_s_l_flag<0].index)
mm_s_l_positive=[]
mm_s_l_negative=[]
for i in mm_s_l_date:
    if mm_s_l[i]>0:
        mm_s_l_positive.append(i)
    elif mm_s_l[i]<0:
        mm_s_l_negative.append(i)


# res={}
# res2={}
# money=10000
# for i in range(0,len(mm_s_m_positive)):
#     price0=data['收盘'][mm_s_m_positive[i]]
#     mairujia=money/data['收盘'][mm_s_m_positive[i]]
#     price1 = data['收盘'][mm_s_m_negative[i+1]]
#     money=data['收盘'][mm_s_m_negative[i+1]]*mairujia
#     res[(mm_s_m_positive[i],mm_s_m_negative[i+1])]=price1-price0
#     res2[(mm_s_m_positive[i],mm_s_m_negative[i+1])]=money
# res={}
# res2={}
# money=10000
# mm_s_l_negative.pop(0)
# for i in range(0,len(mm_s_l_positive)):
#     price0=data['收盘'][mm_s_l_positive[i]]
#     mairujia=money/data['收盘'][mm_s_l_positive[i]]
#     price1 = data['收盘'][mm_s_l_negative[i]]
#     money=data['收盘'][mm_s_l_negative[i]]*mairujia
#     res[(mm_s_l_positive[i],mm_s_l_negative[i])]=price1-price0
#     res2[(mm_s_l_positive[i],mm_s_l_negative[i])]=money
#     if (mm_s_l_positive[i],mm_s_l_negative[i])==(pd.Timestamp('2007-05-23 00:00:00+0000', tz='UTC'), pd.Timestamp('2007-05-30 00:00:00+0000', tz='UTC')):
#         zz=[mairujia,money,data['收盘'][mm_s_l_positive[i]],data['收盘'][mm_s_l_negative[i+1]]]
#
# zlmm={}
# data['mms']=mms
# data['mmm']=mmm
# data['mml']=mml

jc_s_m=jcs-jcm
jc_s_m_ref=jc_s_m.shift(1)
jc_s_m_flag=jc_s_m*jc_s_m_ref
jc_s_m_date=list(jc_s_m_flag[jc_s_m_flag<0].index)
jc_s_m_positive=[]
jc_s_m_negative=[]
for i in jc_s_m_date:
    if jc_s_m[i]>0:
        jc_s_m_positive.append(i)
    elif jc_s_m[i]<0:
        jc_s_m_negative.append(i)

jc_s_l=jcs-jcl
jc_s_l_ref=jc_s_l.shift(1)
jc_s_l_flag=jc_s_l*jc_s_l_ref
jc_s_l_date=list(jc_s_l_flag[jc_s_l_flag<0].index)
jc_s_l_positive=[]
jc_s_l_negative=[]
for i in jc_s_l_date:
    if jc_s_l[i]>0:
        jc_s_l_positive.append(i)
    elif jc_s_l[i]<0:
        jc_s_l_negative.append(i)


bias_jc_s_m=((jcs-jcm)/jcm)*100
bias_jc_s_l=((jcs-jcl)/jcl)*100

jcm_delta=jcm.diff()
jcl_delta=jcl.diff()

maidian=set(mm_s_m[mm_s_m>0].index)&set(jcm_delta[jcm_delta>0].index)&set(jcl_delta[jcl_delta>0].index)
mm_s_m_bias=((mms-mmm)/mmm)*100

maidian=list(maidian)
maidian2=pd.DataFrame(maidian)
trade_day=list(data.index)
res={}
for i in range(0,len(trade_day)):
    if trade_day[i] in list(maidian):
        res[i]=trade_day[i]
    else:
        res[i]='-'
date_buy=[]
for i in range(0,len(res.values())-1):
    if res[i+1]!='-' and res[i]=='-':
        date_buy.append(res[i+1])
data_buy=pd.DataFrame(date_buy)

maichu=pd.DataFrame(mm_s_m[mm_s_m<0].index)
mm_s_l_bias=((mms-mml)/mml)*100
zz=mm_s_l_bias.rolling(window=20).std()
zzz=mm_s_l_bias.rolling(window=20).mean()
zzzz=zzz+1.2*zz
caomai=mm_s_l_bias-zzzz
caomai2=caomai[caomai>0]
caomai3=mm_s_l_bias[mm_s_l_bias>10]

date_sell=[]
maichu=set(mm_s_m[mm_s_m<0].index)&set(caomai3.index)
res={}
for i in range(0,len(trade_day)):
    if trade_day[i] in list(maichu):
        res[i]=trade_day[i]
    else:
        res[i]='-'

date_sell=[]
for i in range(0,len(res.values())-1):
    if res[i+1]!='-' and res[i]=='-':
        date_sell.append(res[i+1])

maichu2=set(mm_s_m[mm_s_m<0].index)&set(mm_s_l[mm_s_l<0].index)
for i in range(0,len(trade_day)):
    if trade_day[i] in list(maichu2):
        res[i]=trade_day[i]
    else:
        res[i]='-'

for i in range(0,len(res.values())-1):
    if res[i+1]!='-' and res[i]=='-':
        date_sell.append(res[i+1])




for i in list(data.index):
    if i in date_buy:
        data.loc[i,'收盘信号']=1
    if i in date_sell:
        data.loc[i,'收盘信号']=0

data['当天仓位']=data['收盘信号'].shift(1)
data['当天仓位'].fillna(method='ffill',inplace=True)
data['ret']=data['收盘']/data['收盘'].shift(1)-1
from datetime import datetime,timedelta

d=datetime.strptime(data[data['当天仓位']==1].index[0],'%Y-%m-%d')-timedelta(days=1)
d=d.strftime('%Y-%m-%d')
df_new=data.loc[d:]
df_new['ret'][0]=0
df_new['当天仓位'][0]=0
df_new['资金指数']=(df_new.ret*data['当天仓位']+1.0).cumprod()
df_new['指数净值']=(df_new.ret+1.0).cumprod()
df1=data[3000:]
df1['策略净值']=(df1.ret*df1['当天仓位']+1.0).cumprod()
df1['指数净值']=(df1.ret+1.0).cumprod()
df1['策略收益率']=df1['策略净值']/df1['策略净值'].shift(1)-1
df1['指数收益率']=df1.ret

import matplotlib.pyplot as plt
# plt.plot(data['收盘'])
data=data[3000:3100]
data['收盘'].plot(figsize=(16,7))
# plt.annotate('买', xy=(np.datetime64(data.index[i]), data['收盘'][i]), arrowprops=dict(facecolor='r', shrink=0.05))
for i in range(len(data)):
    if data['收盘信号'][i]==1:
        plt.annotate('买', xy=(i, data['收盘'][i]), arrowprops=dict(facecolor='r', shrink=0.05))
    if data['收盘信号'][i]==0:
        plt.annotate('卖',xy=(i,data['收盘'][i]),arrowprops=dict(facecolor='g',shrink=0.1))

plt.title('上证指数2000-2019年MFI买卖信号',size=15)
plt.xlabel('')
ax=plt.gca()
# ax.spines['right'].set_color('none')
# ax.spines['top'].set_color('none')
plt.show()
# j=-1
# for i in range(j+1,len(maidian)):
#     data_buy0.append(maidian.iloc[i,0])
#     for j in range(i+1,len(maidian)):
#         # if maidian.iloc[j,0] in trade_day:
#
#             data_buy0.append(maidian.iloc[j, 0])
#         else:
#             date_buy.append(data_buy0)
#             data_buy0 = []
#             break


# 主力进出
# 白线为短期主力运作轨迹，黄线为中期主力运作轨迹，紫线为长期主力运作轨迹。
# 1、主力进出指标的白线向上突破黄线、紫线且三线向上发散，表示主力有效控盘，可逢底介入，持股待涨。
# 2、主力进出指标的白线上涨过快远离黄、紫线，出现较大乖离，表示短线获利筹码较多，宜注意控制风险，可适当卖出。
# 3、当白线回落至黄、紫线处受支撑时，而黄紫线发散向上，表示上升趋势未改，前期股价回落仅是途中的回调，可适量跟进。
# 4、主力进出三线“死亡交叉”，盘口呈空头排列，投资者宜尽快出局。
# 5、主力进出三线相近并平行向下时，表明主力尚未进场或正在出货，此时不宜介入。
# 6、主力进出是一种趋势指标，但趋势改变信号有时会出现滞后现象，此时就要用主力买卖指标加以配合使用。


# 主力买卖
# 白线为短期趋势线，黄线为中期趋势线，紫线为长期趋势线。
# 1、主力买卖与主力进出配合使用时准确率极高。
# 2、当底部构成发出信号，且主力进出线向上时判断买点，准确率极高。
# 3、当短线上穿中线及长线时，形成最佳短线买点交叉形态（如底部构成已发出信号或主力进出线也向上且短线乖离率不大时）。
# 4、当短线、中线均上穿长线，形成中线最佳买点形态（如底部构成已发出信号或主力进出线也向上且三线均向上时）。
# 5、当短线下穿中线，且短线与长线正乖离率太大时，形成短线最佳卖点交叉形态。
# 6、当短线、中线下穿长线，且是主力进出已走平或下降时，形成中线最佳卖点交叉形态。
# 7、在上升途中，短、中线回落受长线支撑再度上行之时，为较佳的买入时机。
# 8、指标在0以上表明个股处于强势，指标跌穿0线表明该股步入弱势。



#
#
#
#
# # jcs=var2.ewm(span=1,adjust=False).mean()
# # jcm=var2.ewm(span=12,adjust=False).mean()
# # jcl=var2.ewm(span=26,adjust=False).mean()
# # VAR1:=(CLOSE*2+HIGH+LOW)/4;
# #  VAR2:=EMA(VAR1,13)-EMA(VAR1,34);
# #  VAR3:=EMA(VAR2,5);

# var1=(data['high']+data['low']+2*data['close'])/4
# var2=var1.ewm(span=13,adjust=False).mean()-var1.ewm(span=34,adjust=False).mean()
# var3=var2.ewm(span=5,adjust=False).mean()
import akshare as ak
# import matplotlib.pyplot as plt
# plt.plot(list(res.values()))
# plt.show()
