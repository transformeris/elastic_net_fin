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
    ma12 = fund_em_etf_fund_info_df['累计净值'].rolling(window=5).mean()
    jinzi=fund_em_etf_fund_info_df['累计净值']
    buy_date=[]
    index=list(fund_em_etf_fund_info_df.index)
    for i in range(1,len(index)):
        try:
            if float(jinzi.loc[index[i]])<ma12.loc[index[i]] and float(jinzi.loc[index[i+1]])>ma12.loc[index[i+1]]:
                buy_date.append(index[i])
        except:
            pass
    res={}
    fuck2=[]
    fuck = []
    fuck3 = []
    # for i in buy_date:
    #     res0={}
    #     b=index.index(i)
    #     res0[index[b-2]]=jinzi[index[b-2]]
    #     fuck2.append(index[b-2])
    #     res[(i,jinzi[index[b]])]=res0
    # jinzi=pd.to_numeric(jinzi)
    # jinzi=jinzi.sort_index()
    # jinzi_shift=jinzi.shift(4)
    # delta_jinzi=(jinzi-jinzi_shift)/jinzi*100
    #
    # delta_jinzi2=delta_jinzi[fuck2]
    # for i in delta_jinzi2:
    #     if i>0:
    #        fuck.append(i)
    #     if i < 0:
    #         fuck3.append(i)
jinzi=pd.to_numeric(jinzi)
jinzi=jinzi.sort_index()
jinzi_shift=jinzi.shift(4)
delta_jinzi=(jinzi-jinzi_shift)/jinzi*100
delta_jinzi2=delta_jinzi
delta_jinzi2=delta_jinzi2.sort_index()
delta_jinzi2=delta_jinzi2/100+1
shouyi=[]
zzz=delta_jinzi2.cumprod()
plt.plot(zzz)

plt.show()