import requests
import re
import bs4
import pandas as pd
import akshare as ak
stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", start_date="19900101", end_date='20210907', adjust="")
stock_zh_a_hist_df['日期']=pd.to_datetime(stock_zh_a_hist_df['日期'], format='%Y-%m-%d')
stock_zh_a_hist_df.set_index('日期',inplace=True)
url = f"https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructure/stockid/000001.phtml"

# url = f"https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_FundStockHolder/stockid/000001.phtml"

r = requests.get(url)
temp_df = pd.read_html(r.text)
big_df = pd.DataFrame()
temp_df=temp_df[12:len(temp_df)]
temp_df0=temp_df[0].T
temp_df0.rename(columns={0:'变动日期',1:'公告日期',2:'股本结构图',3:'变动原因',4:'总股本',5:'流通股',6:'；流通A股',7:'高管股',8:'限售A股',9:'流通B股',10:'限售B股',11:'流通H股',12:'国家股',13:'国有法人股',14:'境内法人股',15:'境内发起人股',16:'募集法人股',17:'一般法人股',18:'战略投资者持股',19:'基金持股',20:'转配股',21:'内部职工股',22:'优先股'},inplace=True)
# temp_df0.set_index(0,inplace=True)
temp_df0=temp_df0.drop(temp_df0.index[0],axis=0)
temp_df0['变动日期']=pd.to_datetime(temp_df0['变动日期'], format='%Y%m%d')

temp_df0.set_index('变动日期',inplace=True)



res=[]
for i in range(0,len(temp_df)):
    temp_df0 = temp_df[i].T
    temp_df0.rename(
        columns={0: '变动日期', 1: '公告日期', 2: '股本结构图', 3: '变动原因', 4: '总股本', 5: '流通股', 6: '；流通A股', 7: '高管股', 8: '限售A股',
                 9: '流通B股', 10: '限售B股', 11: '流通H股', 12: '国家股', 13: '国有法人股', 14: '境内法人股', 15: '境内发起人股', 16: '募集法人股',
                 17: '一般法人股', 18: '战略投资者持股', 19: '基金持股', 20: '转配股', 21: '内部职工股', 22: '优先股'}, inplace=True)
    # temp_df0.set_index(0,inplace=True)
    temp_df0 = temp_df0.drop(temp_df0.index[0], axis=0)
    temp_df0['变动日期'] = pd.to_datetime(temp_df0['变动日期'], format='%Y%m%d')
    temp_df0.set_index('变动日期', inplace=True)
    # temp_df0 = temp_df0.loc[~temp_df0.index.duplicated(keep='first')]

    res.append(temp_df0)
res2=pd.concat(res,axis=0)
res2=res2.dropna(how='all')
res2=res2.sort_index(ascending=True)
date_list=list(res2.index)
date=iter(date_list)
# for i in date:
#     print(i)
#     print('fuck',next(date))
date_start_end=[]
date_stock=set(list(stock_zh_a_hist_df.index))
for previous, current in zip(date_list, date_list[1:]):
    print(previous, current)
    date_start_end.append([previous, current])
    date_range0=pd.date_range(previous,current)
    date_range=date_stock&set(list(date_range0))
    stock_zh_a_hist_df.loc[date_range,'总股本']=float(res2.loc[previous]['总股本'][0:-2])*10000

today='2021-12-23'
date_range0=pd.date_range(current,today)
date_range=date_stock&set(list(date_range0))
stock_zh_a_hist_df.loc[date_range,'总股本']=float(res2.loc[current]['总股本'][0:-2])*10000

