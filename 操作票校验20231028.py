import pandas as pd
import re
import os
import numpy as np
from difflib import SequenceMatcher
from itertools import combinations
# 读取Excel表格

import re
def extract_string(s, verb_list):
    for v in verb_list:
        if s.startswith(v):
            return s[len(v):].split('。')[0]


data_ = pd.read_excel('D:\新建文件夹 (3)\OneDrive - 7x541z\桌面\操作票/合山全.xlsx')
data=data_.groupby('操作任务')
list_of_groups = [group for name, group in data]
step_all=np.array(data_['操作步骤'])

verb=['取下','投上','拉开','检查','汇报','再经','合上','断开','将','切换','拆除','核对','投入','测量','在','撤销','复归','退出','确认','记录','对']
res1=[]
res2=[]
刀闸=[]
空气开关=[]
熔断器=[]
地刀=[]
压板=[]
rest=[]
##对取下进行分析##
for i in step_all:
    if i.startswith('取下'):
        res1.append(i)
