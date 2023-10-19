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
        ##对取下进行分析##
        if '''“禁止合闸，线路有人工作”''' in i:
            if '操作把手上' in i:
                pattern = r'''取下(.*)操作把手上“禁止合闸，线路有人工作”标示牌。'''
                match = re.search(pattern, i)
                if match:  # 添加一个条件判断以防止没有匹配时产生的错误
                    刀闸.append(match.group(1))
            elif '监控后台' in i:
                pattern = r'''取下监控后台(.*)“禁止合闸，线路有人工作”标示牌。'''
                match = re.search(pattern, i)
                if match:  # 添加一个条件判断以防止没有匹配时产生的错误
                    刀闸.append(match.group(1))
            elif '空气开关' in i:
                pattern = r'''取下(.*)“禁止合闸，线路有人工作”标示牌。'''
                match = re.search(pattern, i)
                if match:  # 添加一个条件判断以防止没有匹配时产生的错误
                    空气开关.append(match.group(1))
            elif '熔断器' in i:
                pattern = r'''取下(.*)“禁止合闸，线路有人工作”标示牌。'''
                match = re.search(pattern, i)
                if match:  # 添加一个条件判断以防止没有匹配时产生的错误
                    熔断器.append(match.group(1))
        elif '熔断器' in i:
            pattern = r'''取下(.*)。'''
            match = re.search(pattern, i)
            if match:  # 添加一个条件判断以防止没有匹配时产生的错误
                熔断器.append(match.group(1))
        else:
            rest.append(i)
    elif i.startswith('投上'):
        if '熔断器' in i:
            pattern = r'''投上(.*)。'''
            match = re.search(pattern, i)
            if match:  # 添加一个条件判断以防止没有匹配时产生的错误
                熔断器.append(match.group(1))
        else:
            rest.append(i)

    elif i.startswith('拉开'):
        if '地刀' in i:
            pattern = r'''拉开(.*)。'''
            match = re.search(pattern, i)
            if match:  # 添加一个条件判断以防止没有匹配时产生的错误
                地刀.append(match.group(1))

        elif '刀闸' in i:
            pattern = r'''拉开(.*)。'''
            match = re.search(pattern, i)
            if match:  # 添加一个条件判断以防止没有匹配时产生的错误
                刀闸.append(match.group(1))
        else:
            rest.append(i)

    elif i.startswith('检查'):
        res1.append(i)
        if '压板' in i:
            rest.append(i)
