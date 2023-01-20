import requests
import re
import bs4
import pandas as pd
# url = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?callback=jQuery112309149170311082313_1625319963468&st=DetailDate&sr=-1&ps=10&p=2&type=HSGTHIS&token=894050c76af8597a853f5b408b759f5d&js=%7Bpages%3A(tp)%2Cdata%3A(x)%7D&filter=(MarketType%3D1)'
url='http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp'
header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
req = requests.get(url,headers=header)
req.encoding = req.apparent_encoding
html=req.content.decode("utf-8")

# bs=bs4.BeautifulSoup(html,'html.parser')
# bs.find('a')
# bs.find_all('div',class_="maincont")
# # print(bs.find_all('div',class_="maincont",id="lssj",'table'))
# print(bs.find_all("table"))
# table=bs.find_all('span',class_="green")
# url="http://datacenter-web.eastmoney.com/securities/api/data/get?callback=jQuery112305835185241448702_1625319192434&type=RPT_MUTUAL_NETINFLOW_DETAILS&sty=DIRECTION_TYPE%2CTRADE_DATE%2CNET_INFLOW_SH%2CNET_INFLOW_SZ%2CNET_INFLOW_BOTH%2CTIME_TYPE&token=894050c76af8597a853f5b408b759f5d&client=WEB&filter=(DIRECTION_TYPE%3D%222%22)(TIME_TYPE%3D%221%22)&st=TRADE_DATE&sr=1&_=1625319192435"
# tables = pd.read_html(url)
# pat = re.compile('.*?')
# page_all = re.search(pat, html)
