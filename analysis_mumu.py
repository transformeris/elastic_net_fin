from hmmlearn import hmm
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import akshare as ak
2589631
zz=pd.read_excel('D:\chrome下载/县以上机关.xlsx')
res=[]
for i in zz.iterrows():
    target=i[1]
    target2=np.array(target)
    if target2[7]!='研究生' and target2[16]!='是' and ('人力' in str(target2[10]) or '工商管理类' in str(target2[10])) and str(target2[18]) in ['省直','广州','佛山','珠海','江门','肇庆','珠海','中山','茂名']:

        res.append(target2)

zzzzzzz=pd.DataFrame(res)

zzzzzzz.to_excel('1.xls')
#获取pandas DataFrame 某两行之间的数据
def get_data(df, start, end):
    return df.iloc[start:end]
