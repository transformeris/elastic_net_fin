import pandas as pd

from statsmodels.tools.tools import add_constant
from statsmodels.regression.linear_model import OLS
def calc_mkt_factor(df):
    mkt_cap = df['close'] * df['volume']
    mkt_cap.name = 'Mkt_Cap'
    return mkt_cap

def calc_bmv_ratio(df):
    bmv = (df['money'] - df['close'] * df['volume']) / df['volume']
    mkt_cap = calc_mkt_factor(df)
    bmv_ratio = bmv / mkt_cap
    bmv_ratio.name = 'BMV_Ratio'
    return bmv_ratio
def calc_return(df):
    df['Return'] = df['close'].pct_change()
    return df
def calc_three_factor_model(df):
    mkt = pd.DataFrame({'Market_Return': [0.01, 0.02, 0.03, 0.02, 0.01]})
    smb = pd.DataFrame({'SMB_Return': [0.02, 0.01, 0.03, 0.02, 0.01]})
    hml = pd.DataFrame({'HML_Return': [0.01, 0.03, 0.02, 0.02, 0.01]})
    factors = pd.concat([mkt, smb, hml], axis=1)
    factors = add_constant(factors)
    df.name = 'Returns'
    df = pd.concat([df, factors], axis=1).dropna()
    y = df['Return']
    X = df[['const', 'Market_Return', 'SMB_Return', 'HML_Return']]
    results = OLS(y, X).fit()
    return results.params[1:]

data=pd.read_csv('上证50_daily.csv')
data = calc_return(data)
mkt_cap = calc_mkt_factor(data)
bmv_ratio = calc_bmv_ratio(data)
data= pd.concat([data, mkt_cap, bmv_ratio], axis=1).dropna()
params = calc_three_factor_model(data)
expected_return = params[0] + params[1] * data.iloc[-1]['Mkt_Cap'] + params[2] * data.iloc[-1]['BMV_Ratio'] + params[3] * data.iloc[-1]['BMV_Ratio']
print('Expected Return:', expected_return)
#三因子策略
# Path: 三因子策略.py
# Compare this snippet from liangjia.py:
# import pandas as pd
# from numba import njit
# import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
from statsmodels.tools.tools import add_constant
from statsmodels.regression.linear_model import OLS
def calc_mkt_factor(df):
    mkt_cap = df['close'] * df['volume']
    mkt_cap.name = 'Mkt_Cap'
    return mkt_cap

def calc_bmv_ratio(df):
    bmv = (df['money'] - df['close'] * df['volume']) / df['volume']
    mkt_cap = calc_mkt_factor(df)
    bmv_ratio = bmv / mkt_cap
    bmv_ratio.name = 'BMV_Ratio'
    return bmv_ratio
def calc_return(df):
    df['Return'] = df['close'].pct_change()
    return df
def calc_three_factor_model(df):
