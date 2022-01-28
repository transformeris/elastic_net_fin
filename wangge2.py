import pandas as pd

v=pd.read_csv('D:\onedrive\pythonProject\沪深300.csv')
changwei=pd.Series(list(range(0,100)))/100
chushijine=1000000
fene=0
start_date=600
data=v.iloc[start_date:len(v)]
delta_point=data['close'].diff()
zhangdie=delta_point/data['close'].shift(1)*100
data['changeo']=zhangdie
data.loc[start_date,'money_rest']=chushijine
data.loc[start_date,'money_hold']=0
data.loc[start_date,'money_all']=chushijine
data.loc[start_date,'volume_hold']=0
data.loc[start_date,'signal_hold']=0
data.loc[start_date,'volume_in']=0
data.loc[start_date,'volume_out']=0
data.loc[start_date,'money_in']=0
data.loc[start_date,'money_out']=0
data.loc[603,'trade_sign']=1


for i in range(start_date+1,start_date+len(data)):
    if data.loc[i,'signal_hold']==1:
        data.loc[i, 'volume_in'] = 100
        data.loc[i, 'money_in'] = data.loc[i, 'volume_in']*
    elif data.loc[i,'signal_hold']==-1:
        data.loc[i, 'volume_out'] = -100
        data.loc[i,'volume_hold']=data.loc[i-1,'volume_hold']+data.loc[i, 'volume_out']
    elif data.loc[i,'signal_hold']==0:
        data.loc[i, 'volume_hold'] = data.loc[i - 1, 'volume_hold']
