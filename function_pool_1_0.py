import requests
import re
import bs4
import pandas as pd
import akshare as ak




def get_StockStructure(stock):

    '''

    :param stock_code: 股票代码
    :return: 以股本变动时间戳为标签pandasDateframe
    '''
    url = f"https://money.finance.sina.com.cn/corp/go.php/vCI_StockStructure/stockid/{stock}.phtml"
    r = requests.get(url)
    temp_df = pd.read_html(r.text)
    big_df = pd.DataFrame()
    temp_df = temp_df[12:len(temp_df)]
    temp_df0 = temp_df[0].T
    temp_df0.rename(
        columns={0: '变动日期', 1: '公告日期', 2: '股本结构图', 3: '变动原因', 4: '总股本', 5: '流通股', 6: '；流通A股', 7: '高管股', 8: '限售A股',
                 9: '流通B股', 10: '限售B股', 11: '流通H股', 12: '国家股', 13: '国有法人股', 14: '境内法人股', 15: '境内发起人股', 16: '募集法人股',
                 17: '一般法人股', 18: '战略投资者持股', 19: '基金持股', 20: '转配股', 21: '内部职工股', 22: '优先股'}, inplace=True)
    # temp_df0.set_index(0,inplace=True)
    temp_df0 = temp_df0.drop(temp_df0.index[0], axis=0)
    temp_df0['变动日期'] = pd.to_datetime(temp_df0['变动日期'], format='%Y%m%d')

    temp_df0.set_index('变动日期', inplace=True)

    res = []
    for i in range(0, len(temp_df)):
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
    res2 = pd.concat(res, axis=0)
    res2 = res2.dropna(how='all')
    res2 = res2.sort_index(ascending=True)
    return res2

def combanation_stock_hist_structure(stock_zh_a_hist_df,res2):
    date_list = list(res2.index)
    date = iter(date_list)
    # for i in date:
    #     print(i)
    #     print('fuck',next(date))
    date_start_end = []
    date_stock = set(list(stock_zh_a_hist_df.index))
    for previous, current in zip(date_list, date_list[1:]):
        print(previous, current)
        date_start_end.append([previous, current])
        date_range0 = pd.date_range(previous, current)
        date_range = date_stock & set(list(date_range0))
        stock_zh_a_hist_df.loc[date_range, '总股本'] = float(res2.loc[previous]['总股本'][0:-2]) * 10000

    today = str(stock_zh_a_hist_df.index[-1])
    date_range0 = pd.date_range(current, today)
    date_range = date_stock & set(list(date_range0))
    stock_zh_a_hist_df.loc[date_range, '总股本'] = float(res2.loc[current]['总股本'][0:-2]) * 10000
    return stock_zh_a_hist_df


def jinlirun(stock_zh_a_hist_df,stock):
    '''

    :param stock: 股票代码
    :param stock_zh_a_hist_df: 股票日走势
    :return:
    '''
    stock_financial_report_sina_df = ak.stock_financial_report_sina(stock=stock, symbol="利润表")
    stock_financial_report_sina_df2=pd.DataFrame(stock_financial_report_sina_df)
    stock_financial_report_sina_df2['报表日期'] = pd.to_datetime(stock_financial_report_sina_df['报表日期'], format='%Y%m%d')

    stock_financial_report_sina_df2.set_index('报表日期', inplace=True)
    stock_financial_report_sina_df2 = stock_financial_report_sina_df2.sort_index(ascending=True)

    date_list = list(stock_financial_report_sina_df2.index)
    date = iter(date_list)
    # for i in date:
    #     print(i)
    #     print('fuck',next(date))
    date_start_end = []
    date_stock = set(list(stock_zh_a_hist_df.index))
    for previous, current in zip(date_list, date_list[1:]):
        print(previous, current)
        date_start_end.append([previous, current])
        date_range0 = pd.date_range(previous, current)
        date_range = date_stock & set(list(date_range0))
        stock_zh_a_hist_df.loc[date_range, '净利润'] = float(stock_financial_report_sina_df2.loc[previous]['五、净利润'])
    today = str(stock_zh_a_hist_df.index[-1])
    date_range0 = pd.date_range(current, today)
    date_range = date_stock & set(list(date_range0))
    stock_zh_a_hist_df.loc[date_range, '净利润'] = float(stock_financial_report_sina_df2.loc[current]['五、净利润'])
    return stock_zh_a_hist_df

def jinlirun_ttm(stock_zh_a_hist_df,stock):
    stock_structure = get_StockStructure(stock)

    stock_zh_a_hist_df['日期'] = pd.to_datetime(stock_zh_a_hist_df['日期'], format='%Y-%m-%d')
    stock_zh_a_hist_df.set_index('日期', inplace=True)
    zz = combanation_stock_hist_structure(stock_zh_a_hist_df, stock_structure)
    stock_financial_report_sina_df = ak.stock_financial_report_sina(stock="000001", symbol="利润表")

    stock_financial_report_sina_df = ak.stock_financial_report_sina(stock="000001", symbol="利润表")
    stock_financial_report_sina_df = pd.DataFrame(stock_financial_report_sina_df)
    stock_financial_report_sina_df['报表日期'] = pd.to_datetime(stock_financial_report_sina_df['报表日期'], format='%Y%m%d')
    stock_financial_report_sina_df.set_index('报表日期', inplace=True)
    stock_financial_report_sina_df = stock_financial_report_sina_df.sort_index(ascending=True)

    # for i in stock_financial_report_sina_df.iterrows():
    #     d = str(i[0])
    #     # z=pd.to_datetime('2019-09-18 00:00:00','%Y-%m-%d')
    #     # dd=str(float(d[0:4])-1)
    #     dd = i[0] - pd.Timedelta('380 days')
    #     year_range = pd.date_range(dd, i[0])
    #     date_range = set(list(stock_financial_report_sina_df.index)) & set(list(year_range))
    #     year0 = list(date_range)
    #     year0.sort()
    #     year1 = year0[1:]
    #     profit_ttm = stock_financial_report_sina_df.loc[year1, '五、净利润']

    date_stock = set(list(stock_zh_a_hist_df.index))
    date_list = list(stock_financial_report_sina_df.index)
    for previous, current in zip(date_list, date_list[1:]):
        print(previous, current)
        dd = previous - pd.Timedelta('380 days')
        year_range = pd.date_range(dd, previous)
        date_range = set(list(stock_financial_report_sina_df.index)) & set(list(year_range))
        year0 = list(date_range)
        year0.sort()
        year1 = year0[1:]
        profit_ttm = stock_financial_report_sina_df.loc[year1, '五、净利润']

        date_hist = pd.date_range(previous, current - pd.Timedelta('1 days'))
        date_hist2 = date_stock & set(list(date_hist))
        stock_zh_a_hist_df.loc[date_hist2, '净利润_ttm'] = sum(pd.to_numeric(profit_ttm))

    return stock_zh_a_hist_df

def guxi(stock_zh_a_hist_df,stock):
    stock_structure = get_StockStructure(stock)
    stock_zh_a_hist_df['日期'] = pd.to_datetime(stock_zh_a_hist_df['日期'], format='%Y-%m-%d')
    stock_zh_a_hist_df.set_index('日期', inplace=True)

    fenhong = ak.stock_history_dividend_detail("分红", stock, "")
    fenhong = fenhong.drop(fenhong[fenhong['派息(税前)(元)'] == 0].index)
    fenhong = fenhong.dropna(how='all')
    fenhong['除权除息日'] = pd.to_datetime(fenhong['除权除息日'], format='%Y-%m-%d')
    fenhong.set_index('除权除息日', inplace=True)
    date_list = list(fenhong.index)
    one_year_ago_date = date_list[0] - pd.DateOffset(months=12)

    date_stock = set(list(stock_zh_a_hist_df.index))
    zz = set(date_list) & date_stock

    for i in fenhong.iterrows():
        date_after = i[0] + pd.DateOffset(days=14)
        date_after_range = pd.date_range(i[0], date_after)
        date_set = min(date_stock & set(list(date_after_range)))
        stock_zh_a_hist_df.loc[date_set, '派息'] = fenhong.loc[i[0], '派息(税前)(元)']

    stock_zh_a_hist_df = combanation_stock_hist_structure(stock_zh_a_hist_df, stock_structure)
    stock_zh_a_hist_df['派息'] = stock_zh_a_hist_df['派息'].fillna(0)
    stock_zh_a_hist_df.loc[:, '股息'] = stock_zh_a_hist_df['派息'] * stock_zh_a_hist_df['总股本'] / 10
    # stock_zh_a_hist_df.loc[:, '滑动股息'] = stock_zh_a_hist_df['股息'].rolling(window=250, min_periods=1).sum()

    stock_zh_a_hist_df.loc[:, '滑动股息'] = stock_zh_a_hist_df['股息'].rolling('365d', min_periods=1).sum()
    return stock_zh_a_hist_df

def zhichan():
    stock_structure = get_StockStructure('000001')
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", start_date="19900101", end_date='20211230', adjust="")
    stock_zh_a_hist_df['日期'] = pd.to_datetime(stock_zh_a_hist_df['日期'], format='%Y-%m-%d')
    stock_zh_a_hist_df.set_index('日期', inplace=True)

    zhichanfuzhai = ak.stock_financial_report_sina(stock='000001', symbol='资产负债表')
    zhichanfuzhai['报表日期'] = pd.to_datetime(zhichanfuzhai['报表日期'], format='%Y%m%d')

    zhichanfuzhai.set_index('报表日期', inplace=True)
    zhichanfuzhai = zhichanfuzhai.sort_index(ascending=True)

    date_list = list(zhichanfuzhai.index)
    date = iter(date_list)
    # for i in date:
    #     print(i)
    #     print('fuck',next(date))
    date_start_end = []
    date_stock = set(list(stock_zh_a_hist_df.index))
    for previous, current in zip(date_list, date_list[1:]):
        date_start_end.append([previous, current])
        date_range0 = pd.date_range(previous, current)
        date_range = date_stock & set(list(date_range0))
        stock_zh_a_hist_df.loc[date_range, '净资产'] = float(zhichanfuzhai.loc[previous]['股东权益合计'])
        stock_zh_a_hist_df.loc[date_range, '总资产'] = float(zhichanfuzhai.loc[previous]['负债及股东权益总计'])
    today = str(stock_zh_a_hist_df.index[-1])
    date_range0 = pd.date_range(current, today)
    date_range = date_stock & set(list(date_range0))
    stock_zh_a_hist_df.loc[date_range, '净资产'] = float(zhichanfuzhai.loc[current]['股东权益合计'])
    stock_zh_a_hist_df.loc[date_range, '总资产'] = float(zhichanfuzhai.loc[previous]['负债及股东权益总计'])


if __name__=='__main__':
    shangzheng = pd.read_csv('上证50_daily.csv')

    from dateutil.relativedelta import relativedelta
    import datetime

    shangzheng.set_index('Unnamed: 0', inplace=True)

    s_time = datetime.datetime.now()





    now_date=datetime.datetime(2020,10,9)

    z=now_date- relativedelta(years=1)

    rrr=shangzheng.loc[str(z):str(now_date),:]
    if str(now_date) in rrr.index:
        pd.DataFrame.drop(rrr,labels=str(now_date))