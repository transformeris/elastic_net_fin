import requests
import re
from multiprocessing import Pool
import json
import csv
import pandas as pd
import os
import time

url = 'https://www.eastmoney.com/'
response = requests.get(url).text
pat = re.compile('var.*?{pages:(\d+),data:.*?')
page_all = re.search(pat, response)
'''
# 确定页数
pat = re.compile('var.*?{pages:(\d+),data:.*?')
page_all = re.search(pat, response)
# print(page_all.group(1))  # ok
# 提取出list，可以使用json.dumps和json.loads
pattern = re.compile('var.*?data: (.*)}', re.S)
items = re.search(pattern, response)
# 等价于
# items = re.findall(pattern,response)
# print(items[0])
data = items.group(1)
data = json.loads(data)
'''