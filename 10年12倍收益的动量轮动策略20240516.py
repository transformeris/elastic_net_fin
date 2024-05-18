import backtrader as bt
import akshare as ak
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import statsmodels.api as sm
import collections
import pickle
import backtrader as bt
from backtrader import Order, Position
import json
import warnings
import docx
import backtrader as bt
import backtrader.analyzers as btanalyzers
import backtrader.feeds as btfeeds
import backtrader.strategies as btstrats


import math
import itertools
import plotly.graph_objects as go



def rename_columns(datas):
    def process_date_string(date_str):
        # Truncate the string to remove the timezone part
        return date_str[:19]

    # 定义列重命名映射ff
    rename_map = {
        '日期': 'date', '收盘': 'close', '开盘': 'open', '最高': 'high', '最低': 'low',
        '成交量': 'volume', '成交额': 'amount', '振幅': 'amplitude', '涨跌幅': 'pct_change',
        'Date': 'date', 'Close': 'close', 'Open': 'open', 'High': 'high', 'Low': 'low'
    }

    res = {}
    for j, i in datas.items():
        # 重命名列
        i.rename(columns=rename_map, inplace=True)

        # 批量转换时间
        i['date'] = i['date'].apply(process_date_string)
        i['date'] = pd.to_datetime(i['date'], errors='coerce')

        # 设置索引；
        i.set_index('date', inplace=True)

        res[j] = i

    return res


def data_contact(etf_allocation_data,etf_buy_data, etf_sell_data):
    backtest_data = etf_allocation_data.join(etf_sell_data.add_suffix('_sell')).join(etf_buy_data.add_suffix('_buy'))
    return backtest_data



def execute_trades(stock_percent_realtime, etf_shares, cash,initial_capital, sell_price, close_price, buy_price, commission_rate, slippage,min_shares):

    cash_np=np.zeros(shape=(len(stock_percent_realtime)))
    commission_np=np.zeros(shape=(len(stock_percent_realtime)))
    for i in range(len(stock_percent_realtime)):
        if i == 0:
            # Buy ETFs based on initial weights
            etf_shares[i] = (initial_capital * (1 - commission_rate) * stock_percent_realtime[i]) / (buy_price[i] * (1 + slippage))
            etf_shares[i] = np.floor(etf_shares[i] / min_shares) * min_shares
            buy_value = (etf_shares[i] * buy_price[i] * (1 + slippage)).sum()
            cash -= buy_value * (1 + commission_rate)
            cash_np[i]=cash
            commission_np[i]=commission_rate*buy_value
        else:
            cash=cash_np[i-1]*1.00006
            if not np.array_equal(stock_percent_realtime[i], stock_percent_realtime[i-1]):
                # Adjust ETF shares based on new weights
                new_shares = (stock_percent_realtime[i] * ((etf_shares[i-1] * close_price[i-1]).sum() + cash)) / (close_price[i-1] * (1 + slippage))
                new_shares = np.floor(new_shares / min_shares) * min_shares  # Round down to nearest min_shares multiple

                sell_shares = np.maximum(etf_shares[i-1] - new_shares, 0)
                sell_shares = np.floor(sell_shares / min_shares) * min_shares  # Round down to nearest min_shares multiple
                sell_value = (sell_shares * sell_price[i] * (1 - slippage)).sum()
                cash += sell_value * (1 - commission_rate)
                cash_np[i] = cash
                commission_np[i] = sell_value*commission_rate
                buy_shares = np.maximum(new_shares - etf_shares[i-1], 0)
                buy_shares = np.floor(buy_shares / min_shares) * min_shares  # Round down to nearest min_shares multiple
                buy_value = (buy_shares * buy_price[i] * (1 + slippage)).sum()

                if buy_value * (1 + commission_rate) > cash:
                    # Adjust buy shares based on available cash
                    buy_shares = buy_shares / (buy_value * (1 + commission_rate)) * cash
                    buy_shares = np.floor(
                        buy_shares / min_shares) * min_shares  # Round down to nearest min_shares multiple
                    buy_value = (buy_shares * buy_price[i] * (1 + slippage)).sum()
                cash -= buy_value * (1 + commission_rate)
                cash_np[i] = cash
                commission_np[i] = commission_rate*buy_value
                etf_shares[i] = etf_shares[i-1] + buy_shares - sell_shares
            else:
                etf_shares[i] = etf_shares[i-1]
                cash_np[i] = cash
                commission_np[i] = 0

    return etf_shares, cash_np,commission_np


def calculate_max_drawdown_details(portfolio_values_df):

    # 选择 DataFrame 中的第一列进行计算
    portfolio_values = portfolio_values_df.iloc[:, 0]

    # Calculate the cumulative maximum value up to each point
    roll_max = portfolio_values.cummax()
    # Calculate the drawdown as the current value minus the rolling maximum
    drawdown = portfolio_values / roll_max - 1.0
    # Calculate the maximum drawdown
    max_drawdown = drawdown.min()

    # Find the end date of the maximum drawdown
    end_date = drawdown.idxmin()

    # Find the start date of the maximum drawdown
    # We do this by finding the last time the portfolio hit the peak before declining to the minimum
    start_date = roll_max.loc[:end_date][roll_max.loc[:end_date] == roll_max.loc[:end_date].max()].index[0]

    return max_drawdown, start_date, end_date


def calculate_second_largest_drawdown(portfolio_values_df):
    portfolio_values = portfolio_values_df.iloc[:, 0]

    def calculate_drawdown_details(series):
        # Calculate cumulative max and drawdown
        cumulative_max = series.cummax()
        drawdown = series / cumulative_max - 1.0
        # Find the largest drawdown
        max_drawdown = drawdown.min()
        end_date = drawdown.idxmin()
        # Avoid the case where the drawdown ends on the first data point
        if end_date == series.index[0]:
            return max_drawdown, end_date, end_date
        # Find the start date of the largest drawdown
        start_date = series[:end_date][series[:end_date] == cumulative_max[:end_date]].idxmax()
        return max_drawdown, start_date, end_date

    # Calculate the largest drawdown
    largest_drawdown, start_date_largest, end_date_largest = calculate_drawdown_details(portfolio_values)

    # Exclude the period of the largest drawdown and split the series into two parts
    series_before = portfolio_values[:start_date_largest]
    series_after = portfolio_values[end_date_largest:]

    # Calculate the largest drawdown in each part
    drawdown_before, start_before, end_before = calculate_drawdown_details(series_before)
    drawdown_after, start_after, end_after = calculate_drawdown_details(series_after)

    # Determine which one is the second largest drawdown
    if drawdown_before < drawdown_after:
        second_largest_drawdown = drawdown_before
        start_date_second = start_before
        end_date_second = end_before
    else:
        second_largest_drawdown = drawdown_after
        start_date_second = start_after
        end_date_second = end_after

    return second_largest_drawdown, start_date_second, end_date_second


def calculate_annualized_return(portfolio_values):
    total_return = portfolio_values.iloc[-1] / portfolio_values.iloc[0] - 1
    num_days = (portfolio_values.index[-1] - portfolio_values.index[0]).days
    annualized_return = (1 + total_return) ** (365.0 / num_days) - 1
    return annualized_return

def calculate_sharpe_ratio(portfolio_values, risk_free_rate=0.02):
    daily_returns = portfolio_values.pct_change().dropna()
    excess_returns = daily_returns - risk_free_rate / 365
    sharpe_ratio = excess_returns.mean() / excess_returns.std() * np.sqrt(252)
    return sharpe_ratio

def calculate_sortino_ratio(portfolio_values, risk_free_rate=0.02):
    daily_returns = portfolio_values.pct_change().dropna()
    negative_returns = daily_returns[daily_returns < 0]
    annualized_return = calculate_annualized_return(portfolio_values)
    downside_std = negative_returns.std() * np.sqrt(252)
    sortino_ratio = (annualized_return - risk_free_rate) / downside_std
    return sortino_ratio

def calculate_volatility(portfolio_values):
    daily_returns = portfolio_values.pct_change().dropna()
    volatility = daily_returns.std() * np.sqrt(252)
    return volatility

def calculate_win_rate(etf_shares, net_value):
    """
    Calculate the win rate of trade operations based on etf_shares and net_value.

    Parameters:
    etf_shares (np.ndarray): Array containing the ETF shares held over time.
    net_value (np.ndarray): Array containing the net value of holdings over time.

    Returns:
    float: Win rate of the trades.
    np.ndarray: Array indicating which trade days were profitable.
    np.ndarray: Array indicating the days on which trades occurred.
    """
    # Identifying the days on which trades were made
    trade_days = np.where(np.any(np.diff(etf_shares, axis=0) != 0, axis=1))[0] + 1  # +1 because diff reduces index by 1

    # Calculate the net value change on the days after trades were made
    net_value_change = np.diff(net_value)

    # Identify the days with positive net value change (profit)
    profitable_days = net_value_change[trade_days - 1] > 0  # -1 to align with trade day index

    # Calculate win rate
    win_rate = np.sum(profitable_days) / len(profitable_days)

    return win_rate, profitable_days, trade_days










def calculate_drawdowns(df):
    # 计算历史最高净值
    df['Max_NAV'] = df[0].cummax()

    # 计算回撤值：(历史最高净值 - 当前净值) / 历史最高净值
    df['Drawdown'] = (df['Max_NAV'] - df[0]) / df['Max_NAV']

    return df


def calculate_drawdown_details(portfolio_series, large_number=1e6):
    # Convert the series to a dataframe
    portfolio_data = pd.DataFrame(portfolio_series)

    # Calculate the running maximum value up to the current date
    portfolio_data['Max Value'] = portfolio_data[0].cummax()

    # Calculate the drawdown: the percentage loss from the peak
    portfolio_data['Drawdown'] = (portfolio_data[0] - portfolio_data['Max Value']) / portfolio_data['Max Value']

    # Initialize the start date of the drawdown and the number of days since the start
    portfolio_data['Drawdown Start'] = np.nan
    portfolio_data['Days Since Start'] = 0

    # Loop through the dataframe to identify the start of each drawdown and calculate the days since the start
    in_drawdown = False
    for i in range(len(portfolio_data)):
        if portfolio_data['Drawdown'][i] < 0 and not in_drawdown:
            # New drawdown is starting
            in_drawdown = True
            drawdown_start_date = portfolio_data.index[i]
            portfolio_data.at[portfolio_data.index[i], 'Drawdown Start'] = drawdown_start_date
            portfolio_data.at[portfolio_data.index[i], 'Days Since Start'] = 0
        elif portfolio_data['Drawdown'][i] < 0 and in_drawdown:
            # Continuing the current drawdown
            portfolio_data.at[portfolio_data.index[i], 'Drawdown Start'] = drawdown_start_date
            portfolio_data.at[portfolio_data.index[i], 'Days Since Start'] = (
                        portfolio_data.index[i] - drawdown_start_date).days
        elif portfolio_data['Drawdown'][i] == 0:
            # End of the drawdown
            in_drawdown = False

    # Forward fill the drawdown start dates so each day in the drawdown period has the same start date
    portfolio_data['Drawdown Start'] = portfolio_data['Drawdown Start'].fillna(method='ffill')

    # Calculate drawdown speed as Drawdown / Days Since Start, avoiding division by zero
    portfolio_data['Drawdown Speed (Per Day)'] = portfolio_data['Drawdown'] / portfolio_data[
        'Days Since Start'].replace(0, np.nan)

    # Fill NaN values in 'Drawdown Speed (Per Day)' with a large number
    portfolio_data['Drawdown Speed (Per Day)'].fillna(large_number, inplace=True)
    portfolio_data['Drawdown Speed (Per Day)_shift']=portfolio_data['Drawdown Speed (Per Day)'].shift(1)
    # Clean up the dataframe (optional)
    portfolio_data = portfolio_data.drop(columns=['Max Value'])

    return portfolio_data

def determine_position(drawdown_speed):
    if -0.01<=drawdown_speed <=-0.007:
        return 1
    elif -0.1 < drawdown_speed < -0.01:
         return 1
    else:
        return 1


def plot_etfs_combined(df, common_time_period=True):
    """
    Plot ETFs price curves, allowing for selection between all available time periods and common time period.

    Parameters:
    - df: DataFrame containing ETFs prices.
    - common_time_period: bool, if True, plot prices during the common time period of all ETFs;
                          otherwise, plot prices for all available time periods with distinct starting points.
    """
    plt.figure(figsize=(16, 9))

    # Using a broad range of distinct colors for better differentiation
    colors = itertools.cycle(
        ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan'])

    if common_time_period:
        # Find the common start date (latest first_valid_index among ETFs)
        start_date = df.apply(lambda x: x.first_valid_index()).max()
        df_filtered = df.loc[start_date:]
        title_suffix = ' (Common Time Period)'
    else:
        df_filtered = df
        title_suffix = ' (All Time Periods)'

    # Plotting each ETF
    for column in df_filtered.columns:
        if common_time_period:
            # Normalize prices relative to the common start date
            normalized_prices = df_filtered[column] / df_filtered.loc[start_date][column]
        else:
            # Normalize prices relative to each ETF's start date
            start_date = df_filtered[column].first_valid_index()
            if start_date is not None:  # Ensure there is at least one non-NaN value
                normalized_prices = df_filtered[column].fillna(method='ffill') / df_filtered.loc[start_date][column]
        plt.plot(normalized_prices.index, normalized_prices, label=column, color=next(colors))

    plt.title(f'ETFs Close Price Over Time{title_suffix}')
    plt.xlabel('Date')
    plt.ylabel('Normalized Price (Relative to Start)')
    plt.legend()
    plt.grid(True)
    plt.show()


# Example usage:
# plot_etfs_combined(etfs_close_price, common_time_period=True)  # For common time period
# plot_etfs_combined(etfs_close_price, common_time_period=False) # For all available time periods


def plot_etfs_with_hover(df, common_time_period=True):
    """
    Plot ETFs price curves with hover functionality using Plotly, showing date and data on hover.

    Parameters:
    - df: DataFrame containing ETFs prices.
    - common_time_period: bool, if True, plot prices during the common time period of all ETFs;
                          otherwise, plot prices for all available time periods with distinct starting points.
    """
    if common_time_period:
        start_date = df.apply(lambda x: x.first_valid_index()).max()
        df_filtered = df.loc[start_date:]
    else:
        df_filtered = df

    # Normalize prices relative to the start date for each ETF
    normalized_df = df_filtered.divide(df_filtered.iloc[0])

    # Creating the figure
    fig = go.Figure()

    # Adding each ETF as a trace
    for column in normalized_df.columns:
        fig.add_trace(go.Scatter(x=normalized_df.index, y=normalized_df[column], mode='lines', name=column))

    # Updating layout for better readability
    fig.update_layout(
        title='ETFs Close Price Over Time' + (' (Common Time Period)' if common_time_period else ' (All Time Periods)'),
        xaxis_title='Date',
        yaxis_title='Normalized Price',
        hovermode='x unified')  # Unified hover mode for better comparison

    fig.show()


# Displaying the plot with hover functionality for all available time periods



def save_pkl(obj,name):
    with open(name, 'wb') as file:
        pickle.dump(obj, file)

def load_pkl(a):
    with open(a, 'rb') as file:
        obj = pickle.load(file)
    return obj




if __name__ == '__main__':
    # zz=ak.get_us_stock_name()
    # ndaq_etf= ak.stock_us_daily(symbol='QQQ',adjust="qfq")
    # german_etf = ak.stock_us_daily(symbol='EWG', adjust="qfq")
    # n225_etf = ak.stock_us_daily(symbol='EWJ', adjust="qfq")
    # eng_etf = ak.stock_us_daily(symbol='EWU', adjust="qfq")
    # cyb_etf = ak.fund_etf_hist_em(symbol='159915', adjust='qfq')
    # hs300_etf = ak.fund_etf_hist_em(symbol='510300', adjust='qfq')
    # gold_etf = ak.fund_etf_hist_em(symbol='518880', adjust='qfq')

    cyb_etf = ak.fund_etf_hist_em(symbol='159915', adjust='hfq')
    hs300_etf= ak.fund_etf_hist_em(symbol='510300', adjust='hfq')
    ndaq_etf= ak.fund_etf_hist_em(symbol='513100', adjust='hfq')
    gold_etf= ak.fund_etf_hist_em(symbol='518880', adjust='hfq')
    german_etf=ak.fund_etf_hist_em(symbol='513030', adjust='hfq')
    zhongzheng1000_etf=ak.fund_etf_hist_em(symbol='512100', adjust='hfq')
    zhongzheng500_etf = ak.fund_etf_hist_em(symbol='510500', adjust='hfq')
    hongli_etf=ak.fund_etf_hist_em(symbol='510880', adjust='hfq')
    sp_etf=ak.fund_etf_hist_em(symbol='513500', adjust='hfq')
    energy_etf=ak.fund_etf_hist_em(symbol='159930', adjust='hfq')
    doubai_etf = ak.fund_etf_hist_em(symbol='159985', adjust='hfq')
    # # dividend_etf = ak.stock_zh_index_daily_em(symbol='sh000013')
    #
    # # cyb_etf = ak.stock_zh_index_daily_em(symbol='sz399006')
    # # hs300_etf = ak.stock_zh_index_daily_em(symbol='sh000300')
    #
    # cyb_etf = ak.fund_etf_hist_em(symbol='159915', adjust='qfq')
    # hs300_etf = ak.stock_zh_index_daily_em(symbol='sh000300')
    # ndaq_etf=pd.read_csv('IXIC.csv')
    # gold_etf = pd.read_csv('GLD.csv')
    # german_etf = pd.read_csv('dax.csv')
    n225_etf=pd.read_csv('N225.csv')
    # cyb_etf = ak.stock_zh_index_daily_em(symbol='sz399006')

    # hs300_etf= ak.fund_etf_hist_em(symbol='510300', adjust='hfq')
    # ndaq_etf= ak.fund_etf_hist_em(symbol='513100', adjust='hfq')
    # gold_etf= ak.fund_etf_hist_em(symbol='518880', adjust='hfq')
    # german_etf=ak.fund_etf_hist_em(symbol='513030', adjust='hfq')
    # cyb_etf = ak.fund_etf_hist_em(symbol='159915', adjust='qfq')


    # eng_etf=pd.read_csv('ISF_L.csv')
    # dividend_etf = ak.stock_zh_index_daily_em(symbol='sh000013')

    stock_collection={1:hs300_etf,2:ndaq_etf,3:gold_etf,4:cyb_etf,5:german_etf}
    stock_name={1:'hs300_etf',2:'ndaq_etf',3:'gold_etf',4:'cyb_etf',5:'german_etf'}
    etfs=rename_columns(stock_collection)
    # etfs[3]=etfs[3].shift(1).dropna()
    # etfs[3].loc[:,'open']=etfs[3].loc[:,'close']


    # 假设cyb_etf、hs300_etf、ndaq_etf、gold_etf是四个pandas dataframe表格


    # 计算二十日收益率
    for etf in etfs.values():
        etf['return_20'] = etf['close'].pct_change(periods=10)
        etf['average_5']=etf['close'].rolling(window=3,center=True).mean()
        # etf['average_return_20']=(etf['close']-etf['close'].shift(21))/etf['close'].shift(21)
        etf['average_return_20']=(etf['close'].rolling(window=3).mean()-(etf['average_5']).shift(22))/(etf['average_5']).shift(22)


        etf['ROC_5'] = etf['close'].pct_change(periods=21)
        etf['ROC_21'] = etf['close'].pct_change(periods=21)
        etf['ROC_40'] = etf['close'].pct_change(periods=21)
        etf['Log_Returns'] = etf['close'] / etf['close'].shift(1)
        etf['Lagged_Log_Returns'] = etf['Log_Returns']

    res_g30_1000= {}
    res_portfoli_30_1000= {}

    zz=load_pkl('res_g_321_0_200.pickle')
    window_size=321
    iii=21
    etf['ROC_21'] = etf['close'].pct_change(periods=iii)
    res_coe = []
    for etf in etfs.values():
        coe_dict={}
        coefficients = []
        intercepts = []

        for start in range(0, len(etf) - window_size + 1):
            end = start + window_size
            # Prepare data and drop rows with NaN in either column
            temp_df = etf[['ROC_21', 'Lagged_Log_Returns']].iloc[start:end].dropna()
            X = temp_df[['ROC_21']]
            y = temp_df['Lagged_Log_Returns']
            if len(X) > 0 and len(y) > 0:
                model = LinearRegression()
                model.fit(X, y)
                date = max(X.index)
                coe_dict[date] = model.coef_
            coefficients.append(model.coef_)
            intercepts.append(model.intercept_)
        coe_df = pd.DataFrame(coe_dict)
        coe_df.rename(index={0: 'ROC_21'}, inplace=True)
        roc = etf[['ROC_21']]
        df1 = pd.DataFrame(roc)
        df2 = pd.DataFrame(coe_df)

        # 检查DataFrame的维度
        print("df1维度:", df1.shape)
        print("df2维度:", df2.shape)
        save_pkl(etfs,'etfs.pickle')
        # 如果df2的维度不匹配，需要转置
        if df1.shape[1] != df2.shape[0]:
            df2 = df2.T
            print("调整df2维度后:", df2.shape)

        # 进行矩阵乘法
        try:
            result = df1.dot(df2)
            print("结果DataFrame:")
            print(result)
        except ValueError as e:
            print("Error:", e)
        # score=coe_df.dot(etf_da)
        common_indices = result.index.intersection(result.columns)

        # 提取对应的元素
        extracted_elements = {idx: result.at[idx, idx] for idx in common_indices}
        res_coe.append(extracted_elements)


    holding_df = pd.DataFrame(
        res_coe).T
    holding_df.columns = stock_name.values()
    holding_df = holding_df.dropna()
    #
    # # 合并四个表格
    # holding_df = pd.concat(etfs, axis=1, join='inner')
    # holding_df=holding_df.filter(regex='average_return_20')
    # holding_df.columns=stock_name.values()
    # holding_df=holding_df.dropna()

    stock_percent_realtime = holding_df.eq(holding_df.max(axis=1), axis=0).astype(float).shift(
        1).dropna().sort_index()

    # hs300_etf = pd.read_csv('ASHR.csv')
    # ndaq_etf=pd.read_csv('QQQ.csv')
    # gold_etf = pd.read_csv('GLD.csv')
    # german_etf = pd.read_csv('EWG.csv')
    # n225_etf=pd.read_csv('EWJ.csv')
    # hs300_etf= ak.fund_etf_hist_em(symbol='510300', adjust='hfq')
    # ndaq_etf= pd.read_csv('QQQ.csv')
    # gold_etf= gold_etf = pd.read_csv('GLD.csv')
    # german_etf=pd.read_csv('EWG.csv')
    # n225_etf = pd.read_csv('EWJ.csv')
    # cyb_etf = ak.fund_etf_hist_em(symbol='159915', adjust='qfq')
    # stock_collection = {1: hs300_etf, 2: ndaq_etf, 3: gold_etf, 4: german_etf, 5: n225_etf,6:cyb_etf}
    # stock_name = {1: 'hs300_etf', 2: 'ndaq_etf', 3: 'gold_etf', 4: 'german_etf', 5: 'n225_etf',6:'cyb_etf'}
    # etfs = rename_columns(stock_collection)

    open_price = pd.concat(etfs, axis=1, join='inner').filter(regex='open').sort_index()
    sell_price = pd.concat(etfs, axis=1, join='inner').filter(regex='open').sort_index()
    sell_price.columns = stock_name.values()
    close_price = pd.concat(etfs, axis=1, join='inner').filter(regex='close').sort_index()
    close_price.columns = stock_name.values()
    buy_price = pd.concat(etfs, axis=1, join='inner').filter(regex='close').sort_index()
    buy_price.columns = stock_name.values()

    index_intersection = buy_price.index.intersection(stock_percent_realtime.index)
    stock_percent_realtime = stock_percent_realtime.reindex(index_intersection)
    sell_price = sell_price.reindex(index_intersection)
    buy_price = buy_price.reindex(index_intersection)

    close_price_toplt = pd.concat(etfs, axis=1, join='outer').filter(regex='close').sort_index()
    close_price_toplt.columns = stock_name.values()
    # plot_etfs_combined(close_price_toplt,common_time_period=True)
    plot_etfs_with_hover(close_price_toplt, common_time_period=False)
    start_date = pd.to_datetime('2019-4-26')
    end_date = pd.to_datetime('2023-11-24')

    initial_capital = 100000000
    cash = initial_capital
    slippage = 0  # 0.5%
    commission_rate = 0  # 0.1%
    min_shares = 100

    datas = [stock_percent_realtime, sell_price, buy_price]
    for i in datas:
        i = i[start_date:end_date]

    date_index = stock_percent_realtime.index
    etf_shares = np.zeros((len(stock_percent_realtime), len(stock_percent_realtime.columns)))
    sell_price = np.array(sell_price.loc[stock_percent_realtime.index, :])
    close_price = np.array(buy_price.loc[stock_percent_realtime.index, :])
    buy_price = np.array(buy_price.loc[stock_percent_realtime.index, :])
    stock_percent_realtime_np = np.array(stock_percent_realtime)

    # Using the function in the main code
    etf_shares, cash, commission = execute_trades(stock_percent_realtime_np, etf_shares, cash, initial_capital,
                                                  sell_price, close_price, buy_price,
                                                  commission_rate, slippage, min_shares)

    values_part = etf_shares * close_price

    portfolio_value = (etf_shares * close_price).sum(axis=1) + cash
    portfolio_value_df = pd.DataFrame(portfolio_value, index=date_index)
    portfolio_value_df = calculate_drawdown_details(portfolio_value_df[0])
    sharp=calculate_sharpe_ratio(portfolio_value_df[0],0.0225)
    res_g30_1000[iii]=sharp
    res_portfoli_30_1000=portfolio_value_df[0]


    plt.plot(portfolio_value_df[0])
    plt.show()


    portfolio_value=pd.DataFrame(portfolio_value,index=date_index)
    maxdrawdown=calculate_max_drawdown_details(portfolio_value)
    annualize=calculate_annualized_return(portfolio_value)
    second_drawdown=calculate_second_largest_drawdown(portfolio_value)
    print('年化收益:',annualize)
    print('最大回撤:', maxdrawdown)
    print('第二大回撤:', second_drawdown)
l





