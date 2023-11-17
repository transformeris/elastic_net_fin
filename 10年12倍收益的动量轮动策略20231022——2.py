import akshare as ak
import pandas as pd
import datetime
import numpy as np

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



def price_percent_align(etf_open, etf_close, stock_percent):
    # ... 省略前面的部分 ...

    # 仓位调节

    # 删除包含 NaN 的行
    etf_open = etf_open.dropna()
    etf_close = etf_close.dropna()
    stock_percent = stock_percent.dropna()

    # 将每个 DataFrame 转换为 MultiIndex DataFrame
    etf_open.columns = pd.MultiIndex.from_product([['open'], etf_open.columns])
    etf_close.columns = pd.MultiIndex.from_product([['close'], etf_close.columns])
    stock_percent.columns = pd.MultiIndex.from_product([['percent'], stock_percent.columns])

    # 根据日期索引进行对齐
    df_merged = pd.concat([etf_open, etf_close, stock_percent], join='inner', axis=1)

    # 删除 NaN 值
    df_merged = df_merged.dropna()

    # 根据一级索引分离数据给 etf_open, etf_close 和 stock_percent
    etf_open = df_merged['open']
    etf_close = df_merged['close']
    stock_percent = df_merged['percent']

    return etf_open, etf_close, stock_percent


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

    a=etf['date'].shift(20)[-1]
    b=etf.shift(21)
    # 合并四个表格
    holding_df = pd.concat(etfs, axis=1, join='inner')
    holding_df=holding_df.filter(regex='return_20')
    holding_df.columns=stock_name.values()
    etf_number=[0,1,2,3]
    holding_df['max_return_20_etf_name']=holding_df.idxmax(axis=1)
    holding_df['max_return_20_etf_number']=holding_df['max_return_20_etf_name'].replace(['cyb_etf','hs300_etf','ndaq_etf','gold_etf'],etf_number)
    holding_df_last21=holding_df.tail(21).to_html()
    etf_close = pd.concat(etfs, axis=1, join='inner').filter(regex='close').tail(21).to_html()
    res=[holding_df_last21,etf_close]



