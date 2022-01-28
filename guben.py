import requests
import re
import bs4
import pandas as pd
# url = 'https://emweb.securities.eastmoney.com/PC_HSF10/CapitalStockStructure/PageAjax?code=SH600004'
url = 'https://emweb.securities.eastmoney.com/PC_HSF10/CapitalStockStructure/Index?type=web&code=SH600004#'
header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
req = requests.get(url,headers=header)
r = requests.get(url)
# temp_df = pd.read_html(r.text)



req.encoding = req.apparent_encoding
html=req.content.decode("utf-8")
import akshare as ak
stock_fund_stock_holder_df = ak.stock_fund_stock_holder(stock="300270")
print(stock_fund_stock_holder_df)
# bs.find('a')
# bs.find_all('div',class_="maincont")
# # print(bs.find_all('div',class_="maincont",id="lssj",'table'))
# print(bs.find_all("table"))
# table=bs.find_all('span',class_="green")
# url="http://datacenter-web.eastmoney.com/securities/api/data/get?callback=jQuery112305835185241448702_1625319192434&type=RPT_MUTUAL_NETINFLOW_DETAILS&sty=DIRECTION_TYPE%2CTRADE_DATE%2CNET_INFLOW_SH%2CNET_INFLOW_SZ%2CNET_INFLOW_BOTH%2CTIME_TYPE&token=894050c76af8597a853f5b408b759f5d&client=WEB&filter=(DIRECTION_TYPE%3D%222%22)(TIME_TYPE%3D%221%22)&st=TRADE_DATE&sr=1&_=1625319192435"
# tables = pd.read_html(url)
# pat = re.compile('.*?')
# page_all = re.search(pat, html)
# data_page = re.findall(r"\{[^{}]*\}", html)
data_page=re.findall("^lngbbd+$",html)
money_flow_in=re.findall("""\{([^{}]+)\}""",html)
zz=re.findall("""{[^{}]+}""",html)

zzz=re.findall("""(?<=\{).*(?=\})""",html)
zzzzz=re.findall("""(?<=\[).*(?=\])""",html)
stock_first_number=re.findall('"gbgc":\[.*\]', zzzzz[0])
gbgc=re.findall('"gbgc":\[(?<=\[).*(?=\])', html)
zzzzzzzz=re.findall('{[^{}]+}', gbgc[0])
lngbbd=re.findall('"lngbbd":\[(?<=\[).*(?=\])', html)


def stock_fund_stock_holder(stock: str = "600004") -> pd.DataFrame:
    """
    新浪财经-股本股东-基金持股
    https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_FundStockHolder/stockid/600004.phtml
    :param stock: 股票代码
    :type stock: str
    :return: 新浪财经-股本股东-基金持股
    :rtype: pandas.DataFrame
    """
    url = f"https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructure/stockid/{stock}.phtml"
    r = requests.get(url)
    temp_df = pd.read_html(r.text)[13].iloc[:, :5]
    temp_df.columns = [*range(5)]
    big_df = pd.DataFrame()
    need_range = temp_df[temp_df.iloc[:, 0].str.find("截止日期") == 0].index.tolist() + [len(temp_df)]
    for i in range(len(need_range)-1):
        truncated_df = temp_df.iloc[need_range[i]: need_range[i + 1], :]
        truncated_df = truncated_df.dropna(how="all")
        temp_truncated = truncated_df.iloc[2:, :]
        temp_truncated.reset_index(inplace=True, drop=True)
        concat_df = pd.concat([temp_truncated, truncated_df.iloc[0, 1:]], axis=1)
        concat_df.columns = truncated_df.iloc[1, :].tolist() + ["截止日期"]
        concat_df["截止日期"] = concat_df["截止日期"].fillna(method="ffill")
        concat_df["截止日期"] = concat_df["截止日期"].fillna(method="bfill")
        big_df = pd.concat([big_df, concat_df], axis=0, ignore_index=True)
    big_df.dropna(inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df

zz=stock_fund_stock_holder('600004')