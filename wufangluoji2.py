from collections import deque
import pandas as pd
import math
from collections import OrderedDict
def analyze_connections(device_data_df):
    connections={}
    device_all=[]
    for index, row in device_data_df.iterrows():
        device_id, device_type, connected_devices = row
        device_all.append(str(device_id))
        connected_devices_list = str(connected_devices).split('。')
        for i in connected_devices_list:
            device_all.append(str(i))
    device_all=list(set(device_all))
    for index, row in device_data_df.iterrows():

        device_id, device_type, connected_devices = row
        connected_devices_list = str(connected_devices).split('。')
        connections[str(device_id)] = {
            'type': device_type,
            'connected_devices': connected_devices_list
        }
        for connected_device in connected_devices_list:
            if connected_device not in connections:

                connections[connected_device] = {
                    'type': None,
                    'connected_devices': [str(device_id)]
                }
    for id in device_all:
        if id not in connections:
            connections[id]={
                'type':None,
                'connected_devices':[]
            }
    for i,j in connections.items():
        for k in j['connected_devices']:
            if i not in connections[k]['connected_devices']:
                connections[k]['connected_devices'].append(i)
            elif k not in connections[i]['connected_devices']:
                connections[i]['connected_devices'].append(k)
    for i,j in connections.items():
        my_list=j['connected_devices']
        my_list = [i for i in my_list if i != 'nan']
        connections[i]['connected_devices']=list(set(my_list))
    connections.pop('nan')
    return connections


def find_shortest_connection_path(connections, start_device, end_device):
    queue = deque([[start_device]])
    visited = set([start_device])

    while queue:
        path = queue.popleft()
        current_device = path[-1]

        if current_device == end_device:
            return path

        if current_device not in connections:
            continue

        for device in connections[current_device]['connected_devices']:
            if device not in visited:
                visited.add(device)
                new_path = path + [device]
                queue.append(new_path)

    return None
def find_path_bfs(device_dict, start, end, via_device):
    queue = deque([[start]])
    visited = set([start])

    while queue:
        path = queue.popleft()
        current_device = path[-1]

        if current_device == end and via_device in path:
            return path

        for device in device_dict[current_device]['connected_devices']:
            if device not in visited:
                visited.add(device)
                new_path = list(path)
                new_path.append(device)
                queue.append(new_path)

    return None
def find_path(device_dict, start, end, via_device, path=None):
    if path is None:
        path = []

    path = path + [start]
    if start == end:
        return path

    if start not in device_dict:
        return None

    for device in device_dict[start]['connected_devices']:
        if device not in path:
            if via_device in path or device == via_device:
                new_path = find_path(device_dict, device, end, via_device, path)
                if new_path:
                    return new_path

    return None
def bfs_path_with_required_devices(device_dict, start, end, required_devices):
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        current_device, path = queue.popleft()
        if current_device not in visited:
            visited.add(current_device)
            connected_devices = device_dict[current_device]['connected_devices']

            for device in connected_devices:
                if device == end and all(req_device in path for req_device in required_devices):
                    return path + [device]
                elif device not in visited:
                    queue.append((device, path + [device]))

    return None

def 与刀闸相连的地刀(connections):
    res = {}
    for i, j in connections.items():
        res0 = []
        if j['type'] == '刀闸':
            for ii in connections.keys():
                if connections[ii]['type'] == '接地刀闸、地桩':
                    path = find_shortest_connection_path(connections, i, ii)
                    type_recoder = []
                    if path:
                        for t in path:
                            type_recoder.append(connections[t]['type'])
                        zhaozhashu = type_recoder.count('刀闸')
                        if zhaozhashu == 1:
                            res0.append(ii)
            res[i] = res0
    return res

def 与地刀相连的刀闸(connections):
    res = {}
    for i, j in connections.items():
        res0 = []
        if j['type'] == '接地刀闸、地桩':
            for ii in connections.keys():
                if connections[ii]['type'] == '刀闸':
                    path = find_shortest_connection_path(connections, i, ii)
                    type_recoder = []
                    if path:
                        for t in path:
                            type_recoder.append(connections[t]['type'])
                        zhaozhashu = type_recoder.count('刀闸')
                        if zhaozhashu == 1:
                            res0.append(ii)
            res[i] = res0
    return res

def 与刀闸相连的断路器(connections):
    res = {}
    for i, j in connections.items():
        res0 = []
        if j['type'] == '刀闸':
            for ii in connections.keys():
                if connections[ii]['type'] == '断路器':
                    path = find_shortest_connection_path(connections, i, ii)
                    type_recoder = []
                    if path:
                        for t in path:
                            type_recoder.append(connections[t]['type'])
                        zhaozhashu = type_recoder.count('刀闸')
                        if zhaozhashu == 1:
                            res0.append(ii)
            res[i] = res0
    return res
def 与刀闸直接相连的刀闸(connections):
    res = {}
    for i, j in connections.items():
        res0 = []
        if j['type'] == '刀闸':
            for ii in connections.keys():
                if connections[ii]['type'] == '刀闸':
                    if ii in connections[i]['connected_devices']:
                        res0.append(ii)
            res[i] = res0
    return res

def 刀闸倒母(connections):
    res = {}
    other_daozha=与刀闸直接相连的刀闸(connections)
    muxianchedaozha= {}
    for i,j in other_daozha.items():
        if j!=[]:
            muxianchedaozha[i]=j[0]
    lujin=[['220kV1M','20122','20121','2012','220kV2M'],['220kV5M','20562','20561','2056','220kV6M']]
    suolianmuxian={}
    for i in muxianchedaozha.keys():
        for ii in connections[i]['connected_devices']:
            if connections[ii]['type']=='母线':
                suolianmuxian[i]=ii
    for i in muxianchedaozha.keys():
        for ii in lujin:
            if suolianmuxian[i] in ii and suolianmuxian[muxianchedaozha[i]] in ii:
                res[i]=ii[1:-1]
    return res
def 断路器_分合无逻辑(connections):
    res = {}
    for i, j in connections.items():
        res0 = []
        if j['type'] == '断路器':
            res[i] = res0
    return res
def dict_to_string(input_dict):
    key = list(input_dict.keys())[0]
    values = input_dict[key]
    output_string = key + '合:'

    for value in values:
        output_string += value + '=0,'

    return output_string[:-1]

def generate_output_string(input_dict, equal_value):
    output_string = ""
    for key, value in input_dict.items():
        for inner_key, inner_value in value.items():
            output_string += f"{key}{inner_key}："
            output_string += "，".join([f"{item}={equal_value}" for item in inner_value])
            output_string += "\n"
    return output_string

def generate_output_string2(input_dict,connections):
    output_string = ""
    for key, value in input_dict.items():
        for inner_key, inner_value in value.items():
            if connections[key]['type']=='刀闸' and inner_key=='分1':
                equal_value='0'
            elif connections[key]['type']=='刀闸' and inner_key=='合1':
                equal_value='0'
            elif connections[key]['type']=='刀闸' and inner_key=='分2':
                equal_value = '1'
            elif connections[key]['type'] == '刀闸' and inner_key == '合2':
                equal_value = '1'
            elif connections[key]['type']=='刀闸' and inner_key=='分':
                equal_value = '0'
            elif connections[key]['type'] == '刀闸' and inner_key == '合':
                equal_value = '0'
            elif connections[key]['type']=='接地刀闸、地桩' and inner_key=='合':
                equal_value = '0'
            elif connections[key]['type'] == '断路器':
                equal_value = ' '
            output_string += f"{key}{inner_key}："
            output_string += "，".join([f"{item}={equal_value}" for item in inner_value])
            output_string += "\n"
    return output_string



if __name__=="__main__":
    data = pd.read_excel('鳌峰拓扑.xlsx')
    connections = analyze_connections(data)
    # zz=find_shortest_connection_path(z,'49811','220kV2M')
    didao_daozha=与刀闸相连的地刀(connections)
    daozha_didao=与地刀相连的刀闸(connections)
    daozha_daozha=与刀闸直接相连的刀闸(connections)
    duanluqi_daozha=与刀闸相连的断路器(connections)
    daozha_daomu=刀闸倒母(connections)
    duanluqi=断路器_分合无逻辑(connections)
    ##220kV刀闸分逻辑（普通）#
    res0 = {}
    for i, j in daozha_daozha.items():
        res0[i] = daozha_daozha[i] + duanluqi_daozha[i]
    ##220kV刀闸合逻辑（普通）#
    res1 = {}
    for i, j in daozha_daozha.items():
        res1[i] = daozha_daozha[i] + duanluqi_daozha[i]+didao_daozha[i]

    res={}
    for i, j in daozha_daozha.items():
        res__ = {}
        res__['分1']=res0[i]
        res__['合1']=res1[i]
        # res[i]=res__
    ##220kV母线侧刀闸分/合逻辑（倒闸）#
    res6 = {}
    for i, j in daozha_daozha.items():
        if j!=[]:

            res6[i] = daozha_daomu[i] +daozha_daozha[i]
            res__['分2'] = res6[i]
            res__['合2'] = res6[i]
        res[i] = res__

    ##地刀分逻辑#
    res1=与地刀相连的刀闸(connections)
    ##地刀合逻辑#
    pass

    ##断路器分合逻辑#
    pass

    zzz=dict_to_string(res1)
    zzzzzzzzzz=generate_output_string(res, '0')

    res={}
    for i,j in daozha_daozha.items():
        if j!=[]:
            res0={}
            res0['分1']=daozha_daozha[i] + duanluqi_daozha[i]
            res0['合1']=daozha_daozha[i] + duanluqi_daozha[i]+didao_daozha[i]
            res0['分2']=daozha_daomu[i] +daozha_daozha[i]
            res0['合2']=daozha_daomu[i] +daozha_daozha[i]
            res[i]=res0
    for i,j in daozha_didao.items():
        if j!=[]:
            res0={}
            res0['分']=[]
            res0['合']=daozha_didao[i]
            res[i]=res0

    for i,j in duanluqi.items():
        res0={}
        res0['分']=[]
        res0['合']=[]
        res[i]=res0

    for i,j in didao_daozha.items():
        if i not in res.keys():
            res0={}
            res0['分']=duanluqi_daozha[i]
            res0['合']=duanluqi_daozha[i]+didao_daozha[i]
            res[i]=res0
    res = OrderedDict(sorted(res.items()))

    zzz=generate_output_string2(res,connections)




