import requests
import re
import bs4
import pandas as pd
import time
import pandas as pd

url = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?callback=jQuery112309149170311082313_1625319963468&st=DetailDate&sr=-1&ps=10&p='+str(1)+'&type=HSGTHIS&token=894050c76af8597a853f5b408b759f5d&js=%7Bpages%3A(tp)%2Cdata%3A(x)%7D&filter=(MarketType%3D1)'
header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
req = requests.get(url,headers=header)
html=req.content.decode("utf-8")
data_proto=[]
requests.status_codes
requests.adapters.DEFAULT_RETRIES = 1
header = {"Connection": "close",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
def get_data_proto(page):

    for i in page:
        print(i)

        url = 'http://push2his.eastmoney.com/api/qt/stock/kline/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&beg=0&end=20500101&ut=fa5fd1943c7b386f172d6893dbfba10b&rtntype=6&secid=0.300390&klt=101&fqt=1&cb=jsonp1629386901638'
        try:
            req = requests.get(url, headers=header)
            html = req.content.decode("utf-8")
            # data = re.findall(""""DRZJLR":-?\d+\.?\d*""", html)
            data_page = re.findall(r"\{[^{}]*\}", html)
            data_proto.append(data_page)
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            req = requests.get(url, headers=header)
            html = req.content.decode("utf-8")
            #data = re.findall(""""DRZJLR":-?\d+\.?\d*""", html)
            data_page=re.findall(r"\{[^{}]*\}",html)
            data_proto.append(data_page)
    return data_proto


# # time=re.compile(""""LSZJLR":^[0-9]*$""")
# time=re.compile(r"\d+\.?\d*")
# time="LSZJLR"+"-?\d+\.?\d*"
# data=re.findall(""""DRZJLR":-?\d+\.?\d*""",html)

if __name__=='__main__':
    aa=get_data_proto(range(1,155))
    flag=1
    res = {}
    for i in aa:

        for ii in i:
            res0={}
            print(ii)
            print(re.findall('"DetailDate":"?\d*-?\d*-?\d*',ii))
            date=re.findall('"DetailDate":"?\d*-?\d*-?\d*',ii)[0]
            year=date[14:18]
            month=date[19:21]
            day=date[22:24]

            money_flow_in=re.findall(""""DRZJLR":(?<=:).*?(?=,)""",ii)[0][9:]
            money_deal=re.findall(""""DRCJJME":(?<=:).*?(?=,)""",ii)[0][10:]
            money_rest_of_day=re.findall(""""DRYE":(?<=:).*?(?=,)""",ii)[0][7:]
            money_deal_cumulant=re.findall(""""LSZJLR":(?<=:).*?(?=,)""",ii)[0][9:]
            shanghai_index=re.findall(""""SSEChange":(?<=:).*?(?=,)""",ii)[0][12:]
            deal_out = re.findall(""""MCCJE":(?<=:).*?(?=,)""", ii)[0][8:]
            deal_in = re.findall(""""MRCJE":(?<=:).*?(?=,)""", ii)[0][8:]
            shanghai_index_change_percent = re.findall(""""SSEChangePrecent":(?<=:).*?(?=})""", ii)[0][19:]
            # shanghai_index_change_percent=re.findall(""""SSEChangePrecent":-?\d+\.?\d*""", ii)[0][19:]
            stock_first=re.findall('"LCG":"(?<=").*?(?=")"', ii)[0][6:]
            stock_first_change_percent=re.findall(""""LCGZDF":(?<=:).*?(?=,)""", ii)[0][9:]
            stock_first_number=re.findall('"LCGCode":"(?<=").*?(?=")"', ii)[0][11:-1]
            res0['年']=year
            res0['月'] = month
            res0['日']=day
            res0['当日净流入']=float(money_flow_in)
            res0['当日成交净买额']=float(money_deal)
            res0['历史累积净买额']=float(money_deal_cumulant)
            res0['当日余额'] = float(money_rest_of_day)
            res0['上证指数'] = float(shanghai_index)
            res0['卖出成交额'] = float(deal_out)
            res0['买入成交额'] = float(deal_in)
            res0['卖出成交额'] = float(deal_out)
            res0['上证指数涨幅'] = float(shanghai_index_change_percent)
            res0['领涨股'] =stock_first
            res0['领涨股涨幅'] = float(stock_first_change_percent)
            res0['领涨股代码'] = float(stock_first_number)


            res[flag]=res0
            flag=flag+1
    zz=pd.DataFrame(res)
    zzz=zz.T
    zzz.to_excel('沪股通.xlsx')