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
auth('18826075966','Van951023')
#auth('13119680825','13138620023Asdf')
# z=query(opt.OPT_DAILY_PREOPEN).limit(10)
# zz=opt.run_query(z)
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import func
import sqlalchemy

import sqlalchemy
host = '127.0.0.1'
port = 3306
db = 'world'
user = 'root'
password = '18826076791asdf!'
chartset='utf8'

# engine = create_engine(str(r"mysql+mysqldb://%s:" + '%s' + "@%s/%s") % (user, password, host, db),encoding='utf-8')
engine = create_engine('mysql+mysqldb://root:18826076791asdf!@127.0.0.1/world?charset=utf8',encoding='utf-8')
t0=time.time()
query(func.count(finance.FUND_NET_VALUE.id)).scalar()
# for i in range(0,3300):
#     print(i)
#     start=i * 3000
#     end=(i+1) * 3000
#     q=query(finance.FUND_NET_VALUE).limit(3000).offset(915000+start)
#     df=finance.run_query(q)
#     df.to_sql('fund_net_value',con=engine,if_exists='append',index=True)
#     if df.empty:
#         sql = 'SELECT COUNT(*) FROM world.fund_net_value;'
#
#         print('该项数据已下载完毕')
#         print('数据总数量：')
#         print(pd.read_sql(sql,engine))
#         break
# t_end=time.time()-t0

#sql='select * from world.fund_portfolio_stock;'
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