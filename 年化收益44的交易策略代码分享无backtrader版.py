import pandas as pd
import akshare as ak

# 读取数据
# growth_etf_data = ak.stock_zh_index_daily_em(symbol='sh000300')
growth_etf_data = ak.stock_zh_a_hist(symbol="600519", start_date="20000101")

dividend_etf_data = ak.stock_zh_index_daily_em(symbol='sh000013')

# 计算涨跌幅
growth_etf_returns = growth_etf_data['close'].pct_change()
dividend_etf_returns = dividend_etf_data['close'].pct_change()

# 计算RSRS指标
period = 20
rsrs = (growth_etf_returns.rolling(period).corr(dividend_etf_returns) * dividend_etf_returns.rolling(period).std() / growth_etf_returns.rolling(period).std()).dropna()

# 计算z-score
zscore = (rsrs - rsrs.mean()) / rsrs.std()

# 设置阈值
rsrs_threshold = -1000

# 初始化持仓
growth_etf_position = 0
dividend_etf_position = 0
cash = 1000000

# 记录交易信息
log_df = pd.DataFrame(columns=[
    'date', 'growth_etf_position', 'dividend_etf_position',
    'total_position', 'cash', 'growth_etf_returns',
    'dividend_etf_returns', 'value'
])

# 开始回测
for i in range(period, len(growth_etf_data)):
    # 判断是否需要调仓
    if True:
        if growth_etf_returns.iloc[i] > dividend_etf_returns.iloc[i]:
            # 卖出红利低波ETF
            dividend_etf_position = 0
            cash += dividend_etf_position * dividend_etf_data['close'].iloc[i] * (1 - 0.0001)
            # 买入创成长ETF
            growth_etf_position = int(cash / growth_etf_data['close'].iloc[i])
            cash -= growth_etf_position * growth_etf_data['close'].iloc[i] * (1 + 0.0001)
        else:
            # 卖出创成长ETF
            growth_etf_position = 0
            cash += growth_etf_position * growth_etf_data['close'].iloc[i] * (1 - 0.0001)
            # 买入红利低波ETF
            dividend_etf_position = int(cash / dividend_etf_data['close'].iloc[i])
            cash -= dividend_etf_position * dividend_etf_data['close'].iloc[i] * (1 + 0.0001)
    else:
        # 卖出创成长ETF和红利低波ETF
        growth_etf_position = 0
        dividend_etf_position = 0
        cash += growth_etf_position * growth_etf_data['close'].iloc[i] * (1 - 0.0001)
        cash += dividend_etf_position * dividend_etf_data['close'].iloc[i] * (1 - 0.0001)

    # 计算总持仓和总价值
    total_position = growth_etf_position + dividend_etf_position
    value = cash + growth_etf_position * growth_etf_data['close'].iloc[i] + dividend_etf_position * dividend_etf_data['close'].iloc[i]

    # 记录交易信息
    log_df.loc[i] = [
        growth_etf_data.index[i], growth_etf_position, dividend_etf_position,
        total_position, cash, growth_etf_returns.iloc[i],
        dividend_etf_returns.iloc[i], value
    ]

# 打印交易信息
print(log_df)