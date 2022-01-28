# -*- coding: utf-8 -*-
import datetime
import time
import numpy as np
from sqlalchemy.sql import func
import pandas as pd
import math
from pandas import DataFrame
import akshare as ak

def get_day_nday_ago(date,n):
    t = time.strptime(date, "%Y-%m-%d")
    y, m, d = t[0:3]
    before_n_days=[]
    for i in range(1, n + 1)[::-1]:

        before_n_days.append(str(datetime.datetime(y, m, d)- datetime.timedelta(days=i))[0:10])
    # Date = str(datetime.datetime(y, m, d) - datetime.timedelta(n)).split()

    return before_n_days


data=pd.read_csv('天华超净daily.csv',index_col=0)
# data = ak.stock_zh_a_hist(symbol='300390', adjust="qfq")
var1=(data['high']+data['low']+data['close'])/3
data2=data.shift(1)

var2_pre=((var1-data2['low'])-(data['high']-var1))*data['volume']/10000000/(data['high']-data['low'])
var2_pre=var2_pre.replace([np.inf, -np.inf], np.nan)
var2_pre=var2_pre.dropna()
var2_pre=var2_pre.round(decimals=2)
date_start='2005-01-05'
t = time.strptime(date_start, "%Y-%m-%d")
y, m, d = t[0:3]
# df[~df.isin([inf]).any(1)]


res={}
for i in list(var2_pre.index):
    zzz=var2_pre.truncate(after=i,axis="rows")
    # zzzz=zzz.drop(i)
    res[i]=sum(zzz)




# jcs=var2.ewm(span=1,adjust=False).mean()
# jcm=var2.ewm(span=12,adjust=False).mean()
# jcl=var2.ewm(span=26,adjust=False).mean()
# VAR1:=(CLOSE*2+HIGH+LOW)/4;
#  VAR2:=EMA(VAR1,13)-EMA(VAR1,34);
#  VAR3:=EMA(VAR2,5);

# var1=(data['high']+data['low']+2*data['close'])/4
# var2=var1.ewm(span=13,adjust=False).mean()-var1.ewm(span=34,adjust=False).mean()
# var3=var2.ewm(span=5,adjust=False).mean()
import akshare as ak