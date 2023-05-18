import pandas as pd

# 读取Excel表格
data = pd.read_excel('D:\onedrive\文档\WXWork Files\File/2023-05/马坦全.xlsx')

# 按照间隔进行分组
groups = data.groupby('操作任务')
contains_keyword = groups.filter(lambda x: x['操作步骤'].str.contains('标示牌').any())
contains_keyword.sort_index(inplace=True)