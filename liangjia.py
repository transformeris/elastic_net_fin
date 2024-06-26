import xlrd
import pandas as pd
from numba import njit
import matplotlib.pyplot as plt
import numpy as np
jiu=pd.read_csv('D:\onedrive\金融/酒512690ETF_min.csv')
jiu.loc[:,'avg_price']=jiu.loc[:,'money']/jiu.loc[:,'volume']
jiu=jiu.dropna()
jiu2=jiu.sort_values(by='avg_price')
price_intervals=[]

for i in range(0,100):
    price_intervals.append(max(jiu['close'])/100*i)
volume_by_price = jiu.groupby(pd.cut(jiu['close'], bins=price_intervals))['volume'].sum()
money_by_price = jiu.groupby(pd.cut(jiu['close'], bins=price_intervals))['money'].sum()
print("成交量按价格区间统计：")
print(volume_by_price)
print("\n成交额按价格区间统计：")
print(money_by_price)
total_volume = jiu['volume'].sum()
volume_by_price2= volume_by_price.cumsum()
volume_by_price3=volume_by_price2/total_volume

#iu['Cum_Volume'] = jiu['volume'].cumsum()
# jiu['Cum_Volume_Price'] = jiu['money'].cumsum()
# jiu['VWAP'] = jiu['Cum_Volume_Price'] / jiu['Cum_Volume']
# for i in jiu.iterrows():
#     print(i[0])
#     if i[0]<1000:
#         continue
#     data=jiu[i[0]-1000:i[0]]
#     s_price=np.percentile(data['close'],50)
#     selected_data = data[data['close'] <=s_price]
#     total_volume = selected_data['volume'].sum()
#
#     jiu.loc[i[0],'total_volume']=total_volume

# def fenxi(data):
#     for i in data.iterrows():
#         print(i[0])
#         if i[0]<60000:
#             continue
#         data_win=data[i[0]-60000:i[0]]
#         a=data_win.loc[:,['close','volume']].sort_values(by='close')
#         total_volume=data_win['volume'].sum()
#         half_volume=total_volume/2
#         data['cumsum_volume']=data['volume'].cumsum()
#         aa=data[data['cumsum_volume']<half_volume]
#         a['cumsum_volume']=a['volume'].cumsum()
#         aaa=a[a['cumsum_volume']<half_volume]
#         zhichengjia=max(aaa['close'])
#         data.loc[i[0],'zhichengjia']=zhichengjia
#     return data
#
# da=fenxi(jiu)

# @jit(nopython=False)
# def fenxi2(data):
#     num_rows, num_cols = data.shape
#
#     for i in range(num_rows):
#         if i < 4800:
#             continue
#
#         data_win = data[i-4799:i, :]
#         sorted_indices = np.argsort(data_win[:, 2])
#         sorted_data_win = data_win[sorted_indices]
#
#         total_volume = np.sum(data_win[:, 5])
#         half_volume = total_volume / 2
#         cumsum_volume = np.cumsum(sorted_data_win[:, 5])
#
#         max_index = np.where(cumsum_volume < half_volume)[0][-1]
#         zhichengjia = sorted_data_win[max_index, 2]
#
#         data[i, -1] = zhichengjia
#     return data


# @njit
# def fenxi2(data):
#     num_rows, num_cols = data.shape
#     result = np.zeros((num_rows, 1))
#
#     for i in range(num_rows):
#         if i < 60000:
#             continue
#
#         data_win = data[i-59999:i, :]
#         sorted_indices = np.argsort(data_win[:, 2])
#         sorted_data_win = data_win[sorted_indices]
#
#         total_volume = np.sum(data_win[:, 5])
#         half_volume = total_volume / 2
#         cumsum_volume = np.cumsum(sorted_data_win[:, 5])
#
#         max_index = np.where(cumsum_volume < half_volume)[0][-1]
#         zhichengjia = sorted_data_win[max_index, 2]
#
#         result[i, 0] = zhichengjia
#
#     return result
#
# # fuck=fenxi(jiu)
# jiu2=np.array(jiu)
# jiu2[:,0]=range(0,len(jiu2))
# jiu2=np.array(jiu2,dtype=np.float64)
# fuck=fenxi2(jiu2)
# plt.plot(jiu[:,2])
# plt.plot(fuck)
# plt.show()
