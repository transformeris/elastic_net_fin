import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
shangzheng=pd.read_csv('上证50_daily.csv')
shangzheng.set_index('Unnamed: 0',inplace=True)
shangzheng['mtm_20']=shangzheng['close']-shangzheng['close'].shift(20)
shangzheng['close_20']=shangzheng['close'].shift(20)
shangzheng['fff']=shangzheng['mtm_20']/shangzheng['close_20']*100
shangzheng['rishouyi']=(shangzheng['close']-shangzheng['open'])/shangzheng['open']
a=shangzheng.loc['2020-01-04':'2021-01-04','fff']
a_p=np.percentile(a,[90])
# ddd=a[a>a_p[0]]

ddd=a[a>15]
zz=shangzheng.loc[list(ddd.index),:]
print(np.cumprod(zz['rishouyi']+1))


# plt.plot(shangzheng.loc[2750:3000,'fff'])
# plt.hist(shangzheng.loc[2700:2900,'fff'],bins=300)
# plt.show()