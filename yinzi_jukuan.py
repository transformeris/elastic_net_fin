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
auth('13119680825','13138620023Asdf')
# get_query_count()
factor_code=pd.read_csv('因子库.csv')
factor=list(factor_code['factor'])
factor_data = get_factor_values(securities=['000001.XSHE','000002.XSHE'], factors=factor, start_date='2017-01-01', end_date='2017-01-03')