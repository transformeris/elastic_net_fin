
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels import regression
import matplotlib.pyplot as plt
import requests
import re
import bs4
import akshare as ak
import pickle
import numpy as np
from datetime import datetime
from datetime import date

z=pd.read_excel('指数列表格 .xlsx')
stock_zh_index_spot_df = ak.stock_zh_index_spot()
res={}
for i in z.iterrows():
    fuck=[]
    for j in stock_zh_index_spot_df.iterrows():
        # if abs(i[1]['最新收盘']-j[1]['最新价'])<10:
        if len(list(set(i[1]['指数简称'])&(set(j[1]['名称']))))>=2:
            # fuck.append(i[1]['指数简称'])
            fuck.append(j[1]['名称'])
            fuck.append(i[1]['最新收盘'])
            fuck.append(j[1]['最新价'])
            fuck.append(j[1]['代码'])

    res[i[1]['指数简称']]=fuck
res2=[]
for jj in stock_zh_index_spot_df.iterrows():
    if '全指' in jj[1]['名称']:
        res2.append(jj[1]['名称'])

res3=[]
for jj in stock_zh_index_spot_df.iterrows():
    if '300' in jj[1]['名称']:
        res3.append(jj[1]['名称'])