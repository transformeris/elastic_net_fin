import akshare as ak
import pandas as pd


def rename_columns(datas):
    res= {}
    for j,i in datas.items():

        i.rename(columns={
            '日期': 'date', '收盘': 'close', '开盘': 'open', '最高': 'high',
            '最低': 'low', '成交量': 'volume', '成交额': 'amount',
            '振幅': 'amplitude', '涨跌幅': 'pct_change'
        }, inplace=True)
        i.set_index(pd.to_datetime(i.loc[:, 'date']), inplace=True)
        res[j]=i
    return res



if __name__=='__main__':

    cyb_etf = ak.fund_etf_hist_em(symbol='159915', adjust='qfq')
    hs300_etf= ak.fund_etf_hist_em(symbol='510300', adjust='qfq')
    ndaq_etf= ak.fund_etf_hist_em(symbol='513100', adjust='qfq')
    gold_etf= ak.fund_etf_hist_em(symbol='518880', adjust='qfq')

    stock_collection={1:cyb_etf,2:hs300_etf,3:ndaq_etf,4:gold_etf}
    stock_name={1:'cyb_etf',2:'hs300_etf',3:'ndaq_etf',4:'gold_etf'}
    stock_list=list(stock_collection.values())
    etfs=rename_columns(stock_collection)


    # 假设cyb_etf、hs300_etf、ndaq_etf、gold_etf是四个pandas dataframe表格


    # 计算二十日收益率
    for etf in etfs.values():
        etf['return_20'] = etf['close'].pct_change(periods=21)

    # 合并四个表格
    holding_df = pd.concat(etfs, axis=1, join='inner')
    holding_df=holding_df.filter(regex='return_20')
    holding_df.columns=stock_name.values()
    etf_number=[0,1,2,3]
    holding_df['max_return_20_etf_name']=holding_df.idxmax(axis=1)
    holding_df['max_return_20_etf_number']=holding_df['max_return_20_etf_name'].replace(['cyb_etf','hs300_etf','ndaq_etf','gold_etf'],etf_number)




