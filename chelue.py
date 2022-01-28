# -*- coding: utf-8 -*-
import datetime
import time

from sqlalchemy.sql import func
import pandas as pd
import math


data=pd.read_csv('上证50_daily.csv',index_col=0)
t=data.index
f=0
jiange=30
res=[]
import datetime
# def get_day_nday_ago(date,n):
#     t = time.strptime(date, "%Y-%m-%d")
#     y, m, d = t[0:3]
#     Date = str(datetime.datetime(y, m, d) - datetime.timedelta(n)).split()
#     return Date[0]

def get_day_nday_ago(date,n):
    t = time.strptime(date, "%Y-%m-%d")
    y, m, d = t[0:3]
    before_n_days=[]
    for i in range(1, n + 1)[::-1]:

        before_n_days.append(str(datetime.datetime(y, m, d)- datetime.timedelta(days=i))[0:10])
    # Date = str(datetime.datetime(y, m, d) - datetime.timedelta(n)).split()

    return before_n_days

aa=get_day_nday_ago('2018-06-10',7)
set(aa)&set(list(data.index))
t=list(data.index)
time_window=30
res={}
for i in t:
    aa = get_day_nday_ago(i, time_window)
    data_time_window=list(set(aa) & set(list(data.index)))
    tt=data.loc[data_time_window]
    if len(data_time_window)<=1:
        continue
    res[i]=sum(tt['volume'])/len(data_time_window)
res2={}
for i in t:
    data_day=data.loc[i]
    res2[i]=data_day['volume']

res3={}
res4={}
mairu={}
maichu={}
for i,j in res.items():
    res3[i]=res2[i]-res[i]
    if res[i]>=1.2*res2[i]:
        res4[i]=1
        mairu[i]=1
        maichu[i]=0
    elif res[i]<0.8*res2[i]:
        res4[i]=-1
        maichu[i]=-1
        mairu[i]=0
    else:
        res4[i]=0
        mairu[i]=0
        maichu[i]=0
zz=pd.DataFrame(res,index=[0]).T

flag=0
res5={}
for i in res4.keys():
    if res4[i]==1:
        flag=flag+1




# import matplotlib.pyplot as plt
# plt.plot(zz)
# plt.show()
