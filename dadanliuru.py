# -*- coding: utf-8 -*-
import datetime
import time
import numpy as np
from sqlalchemy.sql import func
import pandas as pd
import math
from pandas import DataFrame
import akshare as ak
import scipy
import talib
import matplotlib.pyplot as plt
from scipy import stats
from chinese_calendar import is_workday
import chinese_calendar

data = ak.stock_zh_index_daily_em(symbol='sh000016')
# data=ak.stock_zh_a_hist(symbol='300390',adjust='hfq')
data.rename(columns={'open': '开盘', 'high': '最高', 'low': '最低', 'close': '收盘', 'volume': '成交量'}, inplace=True)
data['日期'] = data.index
data = data.set_index(['date'])
data['日期'] = data.index

import akshare as ak
stock_individual_fund_flow_df = ak.stock_individual_fund_flow(stock="000001", market="sh")
# stock_individual_fund_flow_df = ak.stock_individual_fund_flow(stock="000001", market="sh",start_date='2015-01-01',end_date='2021-05-09')
print(stock_individual_fund_flow_df)