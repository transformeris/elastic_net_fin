import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
etf_fund_daily = ak.fund_em_etf_fund_daily()
code=[]
for i in etf_fund_daily.iterrows():
    if '指数型' in i[1]['类型']:
        code.append(i[1]['基金代码'])

for i in code[0:1]:
    fund_em_etf_fund_info_df = ak.fund_em_etf_fund_info(fund='510050')
    fund_em_etf_fund_info_df.set_index(['净值日期'], inplace=True)
    fund_em_etf_fund_info_df=fund_em_etf_fund_info_df.sort_index()
    ma12 = fund_em_etf_fund_info_df['累计净值'].rolling(window=5).mean()
    jinzi=fund_em_etf_fund_info_df['累计净值']
    jinzi = pd.to_numeric(jinzi)
    jinzi=jinzi.sort_index()
    buy_date=[]
    index=list(fund_em_etf_fund_info_df.index)

    jinzi_shift=jinzi.shift(1)
    ma12_shift = ma12.shift(1)
    jinzi_dict=jinzi.to_dict()
    jinzi_shift_dict=jinzi_shift.to_dict()
    ma12_dict=ma12.to_dict()
    ma12_shift_dict = ma12_shift.to_dict()
    buy_date=[]
    sell_date=[]
    a=8
    for i,j in jinzi.items():
        a=a+1
        if jinzi_shift_dict[i]<ma12_shift_dict[i] and jinzi_dict[i]>ma12_dict[i]:
            # print('当天价格：', j, '当天均值：', ma12_dict[i])
            buy_date.append(i)
            a=0
        if a==2:
            sell_date.append(i)

    # for i in range(1,len(index)):
    #     try:
    #         if float(jinzi.loc[index[i]])>ma12.loc[index[i]] and float(jinzi.loc[index[i+1]])<ma12.loc[index[i+1]]:
    #             buy_date.append(index[i+1])
    #     except:
    #         pass
    # jinzi_dict=jinzi.to_dict()
    # ma12_dict=ma12.to_dict()
    # for i,j in jinzi_dict.items():
    #     if
    jinzi=pd.to_numeric(jinzi)
    jinzi_shift = jinzi.shift(-2)
    jinzi_buy=jinzi[buy_date]
    jinzi_sell=jinzi_shift[buy_date]
    delta_jinzi = (jinzi - jinzi_shift) / jinzi * 100
    shenglv=jinzi_sell-jinzi_buy
    zz = shenglv[shenglv > 0]
    zzz=shenglv[shenglv<0]
    zzzz=shenglv[shenglv==0]


