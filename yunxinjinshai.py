import datetime  #
import os.path  # 路径管理
import sys  # 获取当前运行脚本的路径 (in argv[0])
import pickle

import pandas as pd


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
#导入backtrader框架
import backtrader as bt

import datetime  #
import os.path  # 路径管理
import sys  # 获取当前运行脚本的路径 (in argv[0])

#导入backtrader框架
import backtrader as bt


zz=pd.read_excel('运行竞赛.xlsx',sheet_name='分数明细表')
zz=zz.dropna(how='any')
a=zz.loc[0,1:]


resa=[]
for i in zz.iterrows():
    # a = i[1].loc[:,4:]
    resa.append(i[1]['总分'])

gerenzhongfen=pd.DataFrame(resa)
ff1=len(gerenzhongfen[gerenzhongfen.loc[:,0]>=70])
ff2=len(gerenzhongfen[gerenzhongfen.loc[:,0]<70])
ff3=len(gerenzhongfen[gerenzhongfen.loc[:,0]<60])
for i in zz.iterrows():
    ii=i[2]


res2={}
gexunwei=list(zz.groupby('巡维中心'))
for i in gexunwei:
    res=[]
    for ii in i[1].iterrows():
        a = ii[1][4:]
        res.append(sum(a))
    res2[i[0]]=sum(res)/len(res)


res3={}
gezhiwei=list(zz.groupby('岗位'))
for i in gezhiwei:
    res=[]
    for ii in i[1].iterrows():
        a = ii[1][4:]
        res.append(sum(a))
    res3[i[0]]=sum(res)/len(res)

zz=pd.read_excel('运行竞赛成绩信息表.xlsx',sheet_name='变电站值班员竞赛')
zzz=list(zz.groupby('巡维中心'))

# zz=zz.dropna(how='any')
# a=zz.loc[0,1:]