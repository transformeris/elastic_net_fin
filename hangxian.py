import json

obj = json.load(open('110kV端芬站_可见光_电容器巡视航线.json', 'r', encoding='utf-8'))  # 注意，这里是文件的形式，不能直接放一个文件名的字符串
file = open('110kV端芬站_可见光_电容器巡视航线.json', 'r', encoding='utf-8')  # 注意，这里是文件的形式，不能直接放一个文件名的字符串
obj = json.loads(file.readline())

open('110kV端芬站_可见光_电容器巡视航线.json', 'r', encoding='utf-8')
json.loads(open('110kV端芬站_可见光_电容器巡视航线.json', 'r', encoding='utf-8'))