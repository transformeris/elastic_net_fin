# -*- coding: utf-8 -*-
from jqdatasdk import *
from jqdatasdk import opt
from jqdatasdk import *
from jqdatasdk import opt
from jqdatasdk import finance
import datetime
import time
from sqlalchemy.sql import func
import pandas as pd
import math
# get_query_count()
auth('13119680825','13138620023Asdf')
# q=query(finance.FUND_MAIN_INFO).filter((finance.FUND_MAIN_INFO.id<3000)&(finance.FUND_MAIN_INFO.id>200))

q=query(finance.FUND_PORTFOLIO_STOCK).filter(finance.FUND_PORTFOLIO_STOCK.code=='000001').limit(10).offset(2)
df=finance.run_query(q)
for i in range(1,2):
    start=i * 3000
    end=(i+1) * 3000
    q2 = query(finance.FUND_PORTFOLIO_STOCK).filter((finance.FUND_PORTFOLIO_STOCK.pub_date >datetime.date(1998, 1, 1))&(finance.FUND_PORTFOLIO_STOCK.pub_date <datetime.date(2021, 7, 30)))
    df2 = finance.run_query(q2)
    #time.sleep(10)
