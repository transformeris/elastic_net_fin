import akshare as ak
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pickle
import pandas as pd
import matplotlib.font_manager as fm
from docx import Document
from docx.shared import Inches
import math
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from docx import Document
bond_cov_comparison_df = ak.bond_cov_comparison()
print(bond_cov_comparison_df)

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        f.close()


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def plot_stock_trend(data, date_obj, stock_name):
    fig, ax = plt.subplots()
    data.plot(y='收盘', ax=ax)

    # 标记特定日期
    ax.axvline(date_obj, color='red', linestyle='--', lw=2)
    font = fm.FontProperties(fname='C:\Windows\Fonts/msyh.ttc')

    # 设置标题和标签
    plt.legend(prop=font)
    plt.title(f"Stock Trend for {stock_name}", fontproperties=font)
    plt.xlabel("Date")
    plt.ylabel("Closing Price")

    # 优化日期显示格式
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()

    # 保存图像
    plt.savefig(f"{stock_name}_trend.png",dpi=300)
    plt.close(fig)



def plot_cumulative_return(data):

    plt.figure(figsize=(10, 6))
    font = fm.FontProperties(fname='C:\Windows\Fonts/msyh.ttc')
    plt.plot(data['cumulative_return'], label='策略累计收益')
    plt.plot(data['benchmark_cumulative_return'], label='基准累计收益')
    plt.legend(prop=font)
    plt.title('策略与基准累计收益', fontproperties=font)
    plt.savefig('cumulative_return.png', dpi=300)
# stock_hist=ak.stock_zh_a_hist(stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20170301", end_date='20210907', adjust=""))
# res=[]
# for i in bond_cov_comparison_df.iterrows():
#     res1=[]
#     print(i)
#     date_obj = datetime.strptime(str(i[1]['申购日期']), '%Y%m%d')
#
#     # 添加一个月
#     new_date_obj = date_obj + relativedelta(months=1)
#     start=date_obj - relativedelta(months=1)
#     # 将新日期对象转换回字符串
#     new_date_str = new_date_obj.strftime('%Y%m%d')
#     start_date_str = start.strftime('%Y%m%d')
#
#     stock_hist = ak.stock_zh_a_hist(symbol=str(i[1]['正股代码']), period="daily", start_date=start_date_str,
#                                               end_date=new_date_str, adjust="hfq")
#     res.append([i,stock_hist])
# save_obj(res,'kezhuanzhai')
res=load_obj('kezhuanzhai')
zz=[]
doc = Document()
for i in res:
    data=i[1]
    stock_name = i[0][1]['转债名称']  # 假设 res 中包含股票名称
    date_obj=datetime.strptime(str(i[0][1]['申购日期']), '%Y%m%d')
    start = date_obj - relativedelta(days=3)
    end=date_obj + relativedelta(days=3)
    new_date_str = end.strftime('%Y%m%d')
    start_date_str = start.strftime('%Y%m%d')

    data.set_index(pd.to_datetime(data.loc[:, '日期']), inplace=True)

    try:
        print(stock_name)
        zhangfu=(data.loc[end,'收盘']-data.loc[date_obj,'收盘'])/data.loc[date_obj,'收盘']
        zz.append(zhangfu)
        plot_stock_trend(data,date_obj,stock_name)
        doc.add_picture(f"{stock_name}_trend.png")
        doc.add_page_break()  # 添加分页符

    except:
        pass
doc.save('D:\python金融分析报告汇总/可转债.docx')