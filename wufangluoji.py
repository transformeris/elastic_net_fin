from collections import deque
import pandas as pd
import math
data = pd.read_excel('鳌峰拓扑.xlsx')
# device_data = [
#     ('49812', '刀闸', '49811,4981B0,4981,220kV2M'),
#     ('49811', '刀闸', '49812,4981B0,4981,220kV1M'),
#     ('4981B0', '接地刀闸、地桩', '49812,49811,4981'),
#     ('4981', '断路器', '49812,49811,49814,4981B0,4981C0'),
#     ('4981C0', '接地刀闸、地桩', '4981,49814'),
#     ('49814', '刀闸', '498140,4981C0'),
#     ('498140', '接地刀闸、地桩', '49814')
# ]


def analyze_connections(device_data_df):
    connections = {}
    for index, row in device_data_df.iterrows():
        device_id, device_type, connected_devices = row
        connected_devices_list = str(connected_devices).split(',')
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
            else:
                connections[connected_device]['connected_devices'].append(str(device_id))
    return connections

z=analyze_connections(data)
# def analyze_connections(device_data):
#     connections = {}
#     for device_id, device_type, connected_devices in device_data:
#         connected_devices_list = connected_devices.split(',')
#         connections[device_id] = {
#             'type': device_type,
#             'connected_devices': connected_devices_list
#         }
#         for connected_device in connected_devices_list:
#             if connected_device not in connections:
#                 connections[connected_device] = {
#                     'type': None,
#                     'connected_devices': [device_id]
#                 }
#             else:
#                 connections[connected_device]['connected_devices'].append(device_id)
#     return connections


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


def find_paths_to_specific_device_type_bfs(connections, start_device, target_device_type, excluded_device_type=None):
    def get_neighbors(current_device, path):
        neighbors = []
        for device in connections[current_device]['connected_devices']:
            if device not in path:
                if excluded_device_type and connections[device][
                    'type'] == excluded_device_type and device != start_device:
                    continue
                neighbors.append(device)
        return neighbors

    paths = []
    visited_paths = set()
    queue = deque([[start_device]])

    while queue:
        path = queue.popleft()
        current_device = path[-1]

        if (tuple(path) not in visited_paths):
            visited_paths.add(tuple(path))
            if connections[current_device]['type'] == target_device_type and current_device != start_device:
                paths.append(path)
            else:
                for neighbor in get_neighbors(current_device, path):
                    new_path = path + [neighbor]
                    queue.append(new_path)

    return paths


def find_shortest_path_to_specific_device_type_bfs(connections, start_device, target_device_type,
                                                   excluded_device_type=None):
    def get_neighbors(current_device, path):
        neighbors = []
        for device in connections[current_device]['connected_devices']:
            if device not in path:
                if connections[device]['type'] == excluded_device_type or target_device_type == excluded_device_type:
                    neighbors.append(device)
                elif excluded_device_type and connections[device]['type'] == excluded_device_type and (
                        device != start_device or device != path[-1]):
                    continue
                neighbors.append(device)
        return neighbors

    queue = deque([[start_device]])

    while queue:
        path = queue.popleft()
        current_device = path[-1]

        if connections[current_device]['type'] == target_device_type and current_device != start_device:
            return path
        else:
            for neighbor in get_neighbors(current_device, path):
                new_path = path + [neighbor]
                queue.append(new_path)

    return None

# def find_shortest_paths_to_specific_device_type_bfs(connections, start_device, target_device_type,
#                                                     excluded_device_type=None):
#     def get_neighbors(current_device, path):
#         neighbors = []
#         for device in connections[current_device]['connected_devices']:
#             if device not in path:
#                 if excluded_device_type and connections[device][
#                     'type'] == excluded_device_type and device != start_device:
#                     continue
#                 neighbors.append(device)
#         return neighbors
#
#     shortest_paths = {}
#     visited = set()
#     queue = deque([[start_device]])
#
#     while queue:
#         path = queue.popleft()
#         current_device = path[-1]
#
#         if current_device not in visited:
#             visited.add(current_device)
#
#             if connections[current_device]['type'] == target_device_type and current_device != start_device:
#                 if current_device not in shortest_paths or len(path) < len(shortest_paths[current_device]):
#                     shortest_paths[current_device] = path
#
#             for neighbor in get_neighbors(current_device, path):
#                 new_path = path + [neighbor]
#                 queue.append(new_path)
#
#     return shortest_paths




def find_shortest_paths_to_specific_device_type_bfs(connections, start_device, target_device_type,
                                                    excluded_device_type=None):
    def get_neighbors(current_device, path):
        neighbors = []
        for device in connections[current_device]['connected_devices']:
            if device not in path:
                if connections[device]['type'] == excluded_device_type and target_device_type == excluded_device_type:
                    neighbors.append(device)
                    flag = 0
                elif excluded_device_type and connections[device]['type'] == excluded_device_type and (
                        device != start_device or device != path[-1]):
                    continue
                neighbors.append(device)
        return neighbors

    shortest_paths = {}
    visited = set()
    queue = deque([[start_device]])

    while queue:
        path = queue.popleft()
        current_device = path[-1]

        if current_device not in visited:
            visited.add(current_device)

            if connections[current_device]['type'] == target_device_type and current_device != start_device:
                if current_device not in shortest_paths or len(path) < len(shortest_paths[current_device]):
                    shortest_paths[current_device] = path

            for neighbor in get_neighbors(current_device, path):
                new_path = path + [neighbor]
                queue.append(new_path)

    return shortest_paths


# 示例：从设备4981查找到所有类型为"接地刀闸、地桩"的设备的路径，同时避开类型为"刀闸"的设备
# paths = find_shortest_paths_to_specific_device_type_bfs(connections, '49812', '接地刀闸、地桩', '刀闸')


def daozhahe(connections):
    res = {}
    for i, j in connections.items():
        res0=[]
        if j['type'] == '刀闸':
            for ii in connections.keys():
                if connections[ii]['type'] == '接地刀闸、地桩':
                    path = find_shortest_connection_path(connections, i, ii)
                    type_recoder = []
                    if path!=None:
                        for t in path:
                            type_recoder.append(connections[t]['type'])
                        zhaozhashu=type_recoder.count('刀闸')
                        if zhaozhashu==1:
                            res0.append(ii)
            res[i]=res0
    return res
def jiedizhaozhahe(connections):
    res = {}
    for i, j in connections.items():
        res0=[]
        if j['type'] == '接地刀闸、地桩':
            for ii in connections.keys():
                if connections[ii]['type'] == '刀闸':
                    path = find_shortest_connection_path(connections, i, ii)
                    type_recoder = []
                    if path:
                        for t in path:
                            type_recoder.append(connections[t]['type'])
                        zhaozhashu=type_recoder.count('刀闸')
                        if zhaozhashu==1:
                            res0.append(ii)
            res[i]=res0
    return res


if __name__=='__main__':
    print('hello')

    # data = pd.read_excel('鳌峰拓扑.xlsx')
    # connections = analyze_connections(data)
    # connections.pop('nan')
    # # connections = {key: connections[key] for key in connections if key!='nan'}
    # res = daozhahe(connections)
    # print(res)
    # res1 = jiedizhaozhahe(connections)
    # print(res1)
    # find_shortest_connection_path(connections, '221甲00', '49811')
    # res = find_shortest_paths_to_specific_device_type_bfs(connections, '49812', '接地刀闸、地桩', '刀闸')
    # print(res)


# res=daozhahe(connections)
# connections = analyze_connections(data)
# k = list(connections.keys())
# for i, j in connections.items():
#
#     if j['type'] == '刀闸':
#         res0 = []
#
#         for ii in k:
#             n = 0
#
#
#             if connections[ii]['type'] == '接地刀闸、地桩':
#                 path = find_shortest_connection_path(connections, i, ii)
#
#                 if path:
#
#                     for pp in path:
#
#                         if connections[pp]['type'] == '刀闸':
#                             n += 1
#                     if n == 1:
#                         res0.append(path[-1])
#                     else:
#                         n = 0
#             if connections[ii]['type'] == '断路器':
#                 path = find_shortest_connection_path(connections, i, ii)
#
#                 if path:
#
#                     for pp in path:
#
#                         if connections[pp]['type'] == '刀闸':
#                             n += 1
#                     if n == 1:
#                         res0.append(path[-1])
#                     else:
#                         n = 0
#
#         res[i] = res0


# def daozhaputongfen(connections: object) -> object:
#     # Initialize the result dictionary
#     res = {}
#
#     # Get a list of connection keys
#
#     k = list(connections.keys())
#
#     # Iterate through the connections
#     for i, j in connections.items():
#
#         # Check if the connection type is '刀闸'
#         if j['type'] == '刀闸':
#             # Initialize a list to store the results for this connection
#             res0 = []
#
#             # Iterate through the connection keys
#             for ii in k:
#                 # Initialize a counter for the number of '刀闸' connections
#                 n = 0
#                 # Check if the connection type is '接地刀闸、地桩'
#                 if connections[ii]['type'] == '接地刀闸、地桩':
#                     # Find the shortest connection path between the two points
#                     path = find_shortest_connection_path(connections, i, ii)
#
#                     # If a path exists
#                     if path:
#                         # Iterate through the path
#                         for pp in path:
#                             # If the connection type is '刀闸', increment the counter
#                             if connections[pp]['type'] == '刀闸':
#                                 n += 1
#
#                         # If the counter is 1, add the last element of the path to the result list
#                         if n == 1:
#                             res0.append(path[-1])
#                         else:
#                             n = 0
#
#                 # Check if the connection type is '断路器'
#                 if connections[ii]['type'] == '断路器':
#                     # Find the shortest connection path between the two points
#                     path = find_shortest_connection_path(connections, i, ii)
#
#                     # If a path exists
#                     if path:
#                         # Iterate through the path
#                         for pp in path:
#                             # If the connection type is '刀闸', increment the counter
#                             if connections[pp]['type'] == '刀闸':
#                                 n += 1
#
#                         # If the counter is 1, add the last element of the path to the result list
#                         if n == 1:
#                             res0.append(path[-1])
#                         else:
#                             n = 0
#
#             # Add the result list to the result dictionary for this connection
#             res[i] = res0
#
#     # Return the result dictionary
#     return res
#
#
# res={}
# for i,j in connections.items():
#     if j['type']=='接地刀闸、地桩':
#         n=0
#         res0=[]
#         for ii in connections.keys():
#             if connections[ii]['type']=='刀闸':
#                 path=find_shortest_connection_path(connections,i,ii)
#
#                 if path:
#                     if ii == '49811':
#                         print(path)
#                     for pp in path:
#                         # If the connection type is '刀闸', increment the counter
#                         if connections[pp]['type'] == '刀闸':
#                             n += 1
#
#                     # If the counter is 1, add the last element of the path to the result list
#                     if n == 1:
#                         if pp=='49811':
#                             print(path)
#                         res0.append(path[-1])
#                     else:
#                         n = 0
#             res[i]=res0
# 00000000000000000000000


# res=[]
# for i in connections.keys():
#     for ii in connections.keys():
#         res.append([i,ii])

#
#
# for i, path in enumerate(paths, start=1):
#     print(f"路径 {i}: {' -> '.join(path)}")
#
# path = find_shortest_connection_path(connections, '49812', '4981B0')
# if path:
#     print(f"设备连接路径为：{' -> '.join(path)}")
# else:
#     print("未找到连接路径。")


# device_data = [
#     ('49812', '刀闸', '49811,4981B0,4981,220kV2M'),
#     ('49811', '刀闸', '49812,4981B0,4981,220kV1M'),
#     ('4981B0', '接地刀闸、地桩', '49812,49811,4981'),
#     ('4981', '断路器', '49812,49811,49814,4981B0,4981C0'),
#     ('4981C0', '接地刀闸、地桩', '4981,49814'),
#     ('49814', '刀闸', '498140,4981C0'),
#     ('498140', '接地刀闸、地桩', '49814')
# ]
#
# def analyze_connections(device_data):
#     connections = {}
#     for device_id, device_type, connected_devices in device_data:
#         connections[device_id] = {
#             'type': device_type,
#             'connected_devices': connected_devices.split(',')
#         }
#
#     return connections
#
# def find_shortest_connection_path(connections, start_device, end_device):
#     def dfs(path, visited):
#         current_device = path[-1]
#         visited.add(current_device)
#
#         if current_device == end_device:
#             return path
#
#         if current_device not in connections:
#             return None
#
#         for device in connections[current_device]['connected_devices']:
#             if device not in visited:
#                 new_path = dfs(path + [device], visited)
#                 if new_path:
#                     return new_path
#
#         return None
#
#     return dfs([start_device], set())
#
#
# connections = analyze_connections(device_data)
# path = find_shortest_connection_path(connections, '4981', '220kV1M')
# if path:
#     print(f"设备连接路径为：{' -> '.join(path)}")
# else:
#     print("未找到连接路径。")
#
#
# # # 数据
# # data = [
# #     ('49812', '刀闸', ['49811', '4981B0', '4981', '220kV2M']),
# #     ('49811', '刀闸', ['49812', '4981B0', '4981', '220kV1M']),
# #     ('4981B0', '接地刀闸、地桩', ['49812', '49811', '4981']),
# #     ('4981', '断路器', ['49812', '49811', '49814', '4981B0', '4981C0']),
# #     ('4981C0', '接地刀闸、地桩', ['4981', '49814']),
# #     ('49814', '刀闸', ['498140', '4981C0']),
# #     ('498140', '接地刀闸、地桩', ['49814']),
# #     ('220kV2M', '母线', ['49812']),
# #     ('220kV1M', '母线', ['49811'])
# # ]
# #
# # # 转换数据结构
# # devices = {device_id: {'type': device_type, 'connections': connected_devices} for
# #            device_id, device_type, connected_devices in data}
# #
# #
# # # 定义搜索函数
# # def search(device_id, avoid_type, target_type):
# #     device = devices[device_id]
# #     device_type = device['type']
# #     connections = device['connections']
# #
# #     result = []
# #     for neighbor_id in connections:
# #         neighbor = devices[neighbor_id]
# #         if neighbor['type'] != avoid_type:
# #             for target_id in neighbor['connections']:
# #                 target = devices[target_id]
# #                 if target['type'] == target_type and target_id != device_id:
# #                     result.append((device_id, target_id))
# #     return result
# #
# #
# # # 指定设备搜索任务
# # specified_device = '49814'
# # task_1 = search(specified_device, '刀闸', '接地刀闸、地桩')
# # task_2 = search(specified_device, '刀闸', '刀闸')
# # task_3 = search(specified_device, '刀闸', '断路器')
# #
# # print("任务1结果：", task_1)
# # print("任务2结果：", task_2)
# # print("任务3结果：", task_3)
# #
# # # import networkx as nx
# # #
# # # # 数据
# # # data = [
# # #     ('49812', '刀闸', ['49811', '4981B0', '4981', '220kV2M']),
# # #     ('49811', '刀闸', ['49812', '4981B0', '4981', '220kV1M']),
# # #     ('4981B0', '接地刀闸、地桩', ['49812', '49811', '4981']),
# # #     ('4981', '断路器', ['49812', '49811', '49814', '4981B0', '4981C0']),
# # #     ('4981C0', '接地刀闸、地桩', ['4981', '49814']),
# # #     ('49814', '刀闸', ['498140', '4981C0']),
# # #     ('498140', '接地刀闸、地桩', ['49814']),
# # #     ('220kV2M', '母线', ['49812']),
# # #     ('220kV1M', '母线', ['49811'])
# # # ]
# # #
# # # # 创建一个空的图
# # # G = nx.Graph()
# # #
# # # # 添加设备和连接
# # # for device_id, device_type, connected_devices in data:
# # #     G.add_node(device_id, type=device_type)  # 确保正确设置 'type' 属性
# # #     for connected_device in connected_devices:
# # #         G.add_edge(device_id, connected_device)
# # #
# # #
# # # # 定义搜索函数
# # # def search(device_id, avoid_type, target_type):
# # #     result = []
# # #     device_type = G.nodes[device_id]['type']
# # #
# # #     for neighbor in G.neighbors(device_id):
# # #         if G.nodes[neighbor]['type'] != avoid_type:
# # #             for target in G.neighbors(neighbor):
# # #                 if G.nodes[target]['type'] == target_type and target != device_id:
# # #                     result.append((device_id, target))
# # #     return result
# # #
# # #
# # # # 指定设备搜索任务
# # # specified_device = '49814'
# # # task_1 = search(specified_device, '刀闸', '接地刀闸、地桩')
# # # task_2 = search(specified_device, '刀闸', '刀闸')
# # # task_3 = search(specified_device, '刀闸', '断路器')
# # #
# # # print("任务1结果：", task_1)
# # # print("任务2结果：", task_2)
# # # print("任务3结果：", task_3)
# paths = find_shortest_paths_to_specific_device_type_bfs(connections, '4981B0', '刀闸', excluded_device_type='刀闸')
