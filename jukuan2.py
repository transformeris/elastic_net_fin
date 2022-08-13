# -*- coding: utf-8 -*-
from jqdatasdk import *
from jqdatasdk import opt
from jqdatasdk import *
from jqdatasdk import opt
import jqdatasdk
import time
from sqlalchemy.sql import func
import pandas as pd
import math
# get_query_count()
# auth('18826075966','Van951023')
# auth('13119680825','13138620023Asdf')
auth('15323303725','13138620023Asdf')
# z=query(opt.OPT_DAILY_PREOPEN).limit(10)
# zz=opt.run_query(z)
# import pandas as pd
# from sqlalchemy import create_engine
# import sqlalchemy
# host = '127.0.0.1'
# port = 3306
# db = 'world'
# user = 'root'
# password = '18826076791asdf!'
# chartset='utf8'
#
# # engine = create_engine(str(r"mysql+mysqldb://%s:" + '%s' + "@%s/%s") % (user, password, host, db),encoding='utf-8')
# engine = create_engine('mysql+mysqldb://root:18826076791asdf!@127.0.0.1/world?charset=utf8',encoding='utf-8')
# t0=time.time()
#
#
# # df=get_all_securities()
# # df.to_sql('index',con=engine,if_exists='replace',index=False)
df4=get_price('512480.XSHG', start_date='1990-01-01', end_date='2200-01-01', frequency='1m', fields=['open', 'close', 'low', 'high', 'volume', 'money', 'factor', 'high_limit', 'low_limit', 'avg', 'pre_close', 'paused'], skip_paused=True,panel=False)
df4.to_csv('半导体ETF_min.csv',encoding='utf_8_sig')
#a=get_all_securities(types=['stock'], date=None)[0:3]
# for i in range(0,904):
#     print(i)
#     start=i * 5000
#     end=(i+1) * 5000
#     q=query(finance.FUND_SHARE_DAILY).limit(5000).offset(start)
#     df=finance.run_query(q)
#     df.to_sql('fund_share_daily',con=engine,if_exists='append',index=True)
#     if df.empty:
#         sql = 'SELECT COUNT(*) FROM world.fund_share_daily;'
#
#         print('该项数据已下载完毕')
#         print('数据总数量：')
#         print(pd.read_sql(sql,engine))
#         break
# t_end=time.time()-t0
# # sql='select * from world.opt_daily_price;'
# changneijijin=pd.read_sql(sql,engine)
# aaa=list(changneijijin.index)
#df=get_extras('acc_net_value', security_list=list(changneijijin.index), start_date='2004-12-20', end_date='2004-12-30', df=True,count=None)


# zz=get_all_securities(['fund'])

#zz=get_price('000788.XSHE', frequency='daily', fields=None, skip_paused=False, fq='pre', panel=True)


#'#sql='select * from world.fund_portfolio_stock;'
# data=pd.read_sql(sql,engine)
# sql='select * from world.fund_portfolio_stock limit 5915622,100;'
# data=pd.read_sql(sql,engine)
# sql='Select * From world.fund_portfolio_stock Where id In (Select id From world.fund_portfolio_stock Group By id Having Count(*)>1)'
# data5=pd.read_sql(sql,engine)
# delete from people where peopleId in (select peopleId from people group by peopleId having count(peopleId) > 1) and rowid not in (select min(rowid) from people group by peopleId having count(peopleId )>1)
# sql='SELECT COUNT(*) FROM world.fund_portfolio_stock;'

# sql='delete from world.fund_portfolio_stock where id in (select id from world.fund_portfolio_stock group by id having count(id) > 1) and rowid not in (select min(rowid) from world.fund_portfolio_stock group by id having count(id )>1)'
# sql='SELECT * FROM world.fund_portfolio_stock GROUP BY (id);'
# data7=pd.read_sql(sql,engine)
#
# sql='select * from world.fund_portfolio_stock limit 2 offset 6088568;'
# sql='drop table world.fund_portfolio_stock'
# finance.run_query(finance.FUND_PORTFOLIO_STOCK)
# for i in zz.index:
#     df = get_extras('acc_net_value', security_list=[i], start_date='2004-12-20',
#                     end_date='2021-12-30', df=True, count=None)
#     df.to_sql('acc_net_value', con=engine, if_exists='append', index=True)
#         if df.empty:
#             sql = 'SELECT COUNT(*) FROM world.opt_trade_rank;'
#
#             print('该项数据已下载完毕')
#             print('数据总数量：')
#             print(pd.read_sql(sql,engine))
#             break