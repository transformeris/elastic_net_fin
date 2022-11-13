import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
shangzheng=pd.read_csv('上证50_daily.csv')
shangzheng.set_index('Unnamed: 0',inplace=True)
shangzheng['mtm_20']=shangzheng['close']-shangzheng['close'].shift(20)
shangzheng['close_20']=shangzheng['close'].shift(20)
shangzheng['fff']=shangzheng['mtm_20']/shangzheng['close_20']*100

a=shangzheng.loc['2005-01-04':'2006-01-04','fff']
np.percentile(a,[0.95])
# plt.plot(shangzheng.loc[2750:3000,'fff'])
# plt.hist(shangzheng.loc[2700:2900,'fff'],bins=300)
# plt.show()