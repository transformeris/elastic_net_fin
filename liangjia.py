import xlrd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
jiu=pd.read_csv('D:\onedrive\金融/酒512690ETF_min.csv')
jiu.loc[:,'avg_price']=jiu.loc[:,'money']/jiu.loc[:,'volume']
# jiu['Cum_Volume'] = jiu['volume'].cumsum()
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
data=jiu[0:3000]
a=data.loc[:,['close','volume']].sort_values(by='close')
total_volume=data['volume'].sum()
half_volume=total_volume/2
data['cumsum_volume']=data['volume'].cumsum()
aa=data[data['cumsum_volume']<half_volume]
a['cumsum_volume']=a['volume'].cumsum()
aaa=a[a['cumsum_volume']<half_volume]
np.percentile(a,50)
# plt.plot(jiu['close'])
# plt.plot(jiu['VWAP'])
plt.show()