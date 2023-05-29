import pandas as pd
import re
# 读取Excel表格
data = pd.read_excel('D:\onedrive\文档\WXWork Files\File/2023-05/圣堂全.xlsx')

# 按照间隔进行分组
groups = data.groupby('操作任务')
contains_keyword = groups.filter(lambda x: x['操作步骤'].str.contains('标示牌').any())
contains_keyword.sort_index(inplace=True)
contains_keyword = contains_keyword[~contains_keyword['操作任务'].str.contains('热备用转检修|检修转热备用|运行转检修|检修转运行')]
pattern = r'将(.*?)由.+'
# match = re.match(pattern, text)
contains_keyword['设备名称'] = contains_keyword['操作任务'].apply(lambda x: re.findall(pattern, x)[0])
groups2 = contains_keyword.groupby('设备名称')
for name, group in groups2:
    filename = 'D:\OneDrive_7x541z\OneDrive - 7x541z\桌面\新建文件夹/' + name + '.xlsx'
    group_df = pd.DataFrame(group, columns=['操作任务', '操作顺序','操作步骤']).sort_index()
    group_df.to_excel(filename, index=False)