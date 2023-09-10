import pandas as pd
import re
import os
import numpy as np
from difflib import SequenceMatcher
from itertools import combinations
# 读取Excel表格
data_ = pd.read_excel('D:\新建文件夹 (3)\OneDrive - 7x541z\桌面\操作票/合山全.xlsx')
buzhou=np.array(data_['操作步骤'])

verb=['取下','投上','拉开','检查','汇报','再经','合上','断开','将','切换','拆除','核对','投入','测量','在','撤销','复归','退出','确认','记录','对']
res=[]
for i in buzhou:
    if i.startswith(tuple(verb)):
        print(i)
    else:
        res.append(i
# qiongju=list(combinations(buzhou,2))
# res=[]
# for i in combinations(buzhou,2):
#     common = os.path.commonprefix([i[0], i[1]])
#     if common!='':
#         res.append(common)
#
# res=list(set(res))
# res2=[]
# for i in combinations(res,2):
#     common = os.path.commonprefix([i[0], i[1]])
#     if common!='':
#         res2.append(common)
#
# res2= list(set(res2))
#
# res3=[]
# for i in combinations(res2,2):
#     common = os.path.commonprefix([i[0], i[1]])
#     if common!='':
#         res3.append(common)
#
# res4= list(set(res3))
# z=[]
# res5=[]
# for i in combinations(res4,2):
#     common = os.path.commonprefix([i[0], i[1]])
#     if common!='':
#         res5.append(common)
#     if common=='检':
#         z.append([common,[i[0], i[1]]])
#
# res5= list(set(res5))