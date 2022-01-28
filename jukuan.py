from jqdatasdk import *
from jqdatasdk import opt

from sqlalchemy.sql import func
import pandas as pd
import math
# get_query_count()
auth('13119680825','13138620023Asdf')

q=query(opt.OPT_DAILY_PREOPEN).limit(10)
# q=query(opt.OPT_DAILY_PREOPEN.code,
#         opt.OPT_DAILY_PREOPEN.trading_code,
#         opt.OPT_DAILY_PREOPEN.name,
#         opt.OPT_DAILY_PREOPEN.exercise_date,
#         opt.OPT_DAILY_PREOPEN.date
# ).limit(10)
qq=opt.run_query(q)
p=get_price('510050.XSHG','2018-01-01 09:00:00','2018-12-23 12:00:00','1d')
print(p)
print(get_bars('10001313.XSHG', 10, unit='1d',
         fields=['date','open','high','low','close'],
         include_now=False, end_dt='2019-01-01'))

q=query(opt.OPT_DAILY_PREOPEN.code,
        opt.OPT_DAILY_PREOPEN.trading_code,
        opt.OPT_DAILY_PREOPEN.name,
        opt.OPT_DAILY_PREOPEN.exercise_date,
        ).filter(
            opt.OPT_DAILY_PREOPEN.date=='2018-05-31')
df=opt.run_query(q)
print(df)
zz=get_price('510050.XSHG', start_date=None, end_date=None, frequency='daily', fields=None, skip_paused=False, fq='pre', count=None)
print(zz)