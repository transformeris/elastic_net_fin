# import json
#
# obj = json.load(open('110kV端芬站_可见光_电容器巡视航线.json', 'r', encoding='utf-8'))  # 注意，这里是文件的形式，不能直接放一个文件名的字符串
# file = open('110kV端芬站_可见光_电容器巡视航线.json', 'r', encoding='utf-8')  # 注意，这里是文件的形式，不能直接放一个文件名的字符串
# obj = json.loads(file.readline())
#
# open('110kV端芬站_可见光_电容器巡视航线.json', 'r', encoding='utf-8')
# json.loads(open('110kV端芬站_可见光_电容器巡视航线.json', 'r', encoding='utf-8'))
# import json
#
# # 读取JSON文件
# with open('110kV端芬站_可见光_电容器巡视航线.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
# with open('110kV金鸡站_红外_电容电抗航线.json', 'r', encoding='utf-8') as f:
#     data2 = json.load(f)
import json

# import chardet
#
# with open('D:\onedrive\文档\WXWork Files\File/2023-05/110kV建陶站_可见光_电容电抗航线.uavx', 'rb') as f:
#     data = f.read()
#     encoding = chardet.detect(data)['encoding']
#     data = data.decode(encoding)
# aa=read_uavx_file('D:\onedrive\文档\WXWork Files\File/2023-05/110kV建陶站_可见光_电容电抗航线.uavx')
import struct

data = b'0\x00#\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00V\xb7{E\x00\x08\x00\x08\x00\x14\x04\x03KP'

numbers = struct.unpack('2i', data[:8])
spaces = struct.unpack('10s', data[8:18])[0].decode('utf-8')