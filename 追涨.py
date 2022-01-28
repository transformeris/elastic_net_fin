import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
etf_fund_daily = ak.fund_em_etf_fund_daily()
code=[]
for i in etf_fund_daily.iterrows():
    if '指数型' in i[1]['类型']:
        code.append(i[1]['基金代码'])
res=[]
res2=[]
zhengzhang=[]

for i in code[0:1]:
    fund_em_etf_fund_info_df = ak.fund_em_etf_fund_info(fund='510300')
    fund_em_etf_fund_info_df.set_index(['净值日期'], inplace=True)
    fund_em_etf_fund_info_df=fund_em_etf_fund_info_df.sort_index()
    fund_em_etf_fund_info_df_shift=fund_em_etf_fund_info_df.shift(-1)
    for ii in fund_em_etf_fund_info_df.iterrows():
        if ii[1]['日增长率']=='' or fund_em_etf_fund_info_df_shift.loc[ii[0]]['日增长率']=='':
            continue
        if float(ii[1]['日增长率'])>2 and float(fund_em_etf_fund_info_df_shift.loc[ii[0]]['日增长率'])>0:
            res.append(ii[0])
            zhengzhang.append(float(fund_em_etf_fund_info_df_shift.loc[ii[0]]['日增长率']))
        if float(ii[1]['日增长率'])>2 and float(fund_em_etf_fund_info_df_shift.loc[ii[0]]['日增长率'])<0:
            res2.append(ii[0])

            zhengzhang.append(float(fund_em_etf_fund_info_df_shift.loc[ii[0]]['日增长率']))

    zhengzhang=pd.DataFrame(zhengzhang)
    zhengzhang[zhengzhang<-2]=-2
    zhengzhang2=zhengzhang/100+1

    zzz = zhengzhang2.cumprod()
    plt.plot(zzz)

    plt.show()