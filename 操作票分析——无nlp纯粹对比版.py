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
data=data_.group_by('操作任务')
buzhou=np.array(data_['操作步骤'])

verb=['取下','投上','拉开','检查','汇报','再经','合上','断开','将','切换','拆除','核对','投入','测量','在','撤销','复归','退出','确认','记录','对']
res=[]
rest=[]
for i in buzhou:
    if i.startswith(tuple(verb)):
        print(i)
        rest.append(extract_string(i, verb))
    else:
        res.append(i)
res2=[]
device_name=[]
rest=[]
for i in buzhou:
    if i.startswith('合上'):
        heshang_pattern = r'合上(.*)。'
        match = re.search(heshang_pattern, i)
        if match:  # 添加一个条件判断以防止没有匹配时产生的错误
            device_name.append(match.group(1))



    cheliang_pattern = r'测量(.*?)两端对地电位正常'
    match = re.search(cheliang_pattern, i)
    if match:  # 添加一个条件判断以防止没有匹配时产生的错误
        device_name.append(match.group(1))

    #
    toushang_pattern = r'投上(.*)。'
    match = re.search(toushang_pattern, i)
    if match:  # 添加一个条件判断以防止没有匹配时产生的错误
        device_name.append(match.group(1))
    #
    # if i.startswith('合上'):
    #     heshang_pattern = r'合上(.*)。'
    #     match = re.search(heshang_pattern, i)
    #     if match:  # 添加一个条件判断以防止没有匹配时产生的错误
    #         device_name.append(match.group(1))
    #

#
# from docx import Document
#
# # 加载Word文档
# doc = Document('D:/新建文件夹 (3)/OneDrive - 7x541z/桌面/02 第二册 二次设备部分（合山站）.docx')
#
# # 遍历文档中的所有表格
# for table in doc.tables:
#     # 遍历表格中的所有行
#     for row in table.rows:
#         # 遍历行中的所有单元格
#         for cell in row.cells:
#             print(cell.text)
# # 创建一个空的DataFrame
# ta_co=[]
# df = pd.DataFrame()
#
# # 遍历文档中的所有表格
# for i, table in enumerate(doc.tables):
#     # 对于每个表格，我们将其转化为一个临时的DataFrame
#     temp_data = [[cell.text for cell in row.cells] for row in table.rows]
#     temp_df = pd.DataFrame(temp_data)
#     ta_co.append(temp_df)
#
# zz=[]
# for i in ta_co:
#     if '压板名称' in i.values or '压板编号' in i.values:
#         zz.append(i)





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