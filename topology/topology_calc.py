# -*- coding: utf-8 -*-
import pandas as pd
import networkx as nx
from itertools import combinations
import application.demand.demand_parser as pocomputing_demand_parser


################################################################################
# 基于构造的拓扑数据，计算相应的拓扑及其特征
###topo_graph；networkx模块提供的拓扑数据结构，便于计算各种数据
#    类型为networkx.classes.graph.Graph/networkx.classes.graph.DiGraph
#
# 未来目标：将两种拓扑结构统一为一种，这块涉及的业务流程相对多，计划后一个版本消除

# 计算从入口节点，到出口节点中，所有满足需求的虚拟专线集
#    topo_graph_nx；网络拓扑信息，类型为topo_graph_nx
#    source_name：虚拟专线入口节点名，类型为str，例如'BJ_OVS'
#    des_name：虚拟专线出口节点名，类型为str，例如'SH_OVS'
#    max_hop：最大路由条数，防止虚拟专线过多造成计算压力
#    max_path：最大虚拟专线数量，防止过多虚拟专线，造成计算应用卡死
# return：满足要求的虚拟专线集合，类型为List<List<str>>。每个元素为list<str>形式的虚拟专线
#    例如：[['BJ_OVS', 'SH_OVS'],   #虚拟专线1
#        ['BJ_OVS', 'SZ_OVS', 'SH_OVS']，#虚拟专线1，即虚拟专线按先后顺序依次经过
#        #BJ_OVS, SZ_OVS，SH_OVS三个节点
#        ['BJ_OVS', 'SZ_OVS', 'SH_OVS']]
def build_all_simple_paths(topo_graph, source_name, des_name, max_hop=5, max_path=100001):
    path_list = []
    if max_hop < 2:
        return path_list
    for i in range(2, max_hop + 1):
        tmp_path_list = list(nx.all_simple_paths(topo_graph, source_name, des_name, i))
        if i > 2 and len(tmp_path_list) > max_path:
            break
        else:
            path_list = tmp_path_list
    return path_list


def get_connected_component_count(topo_graph):
    count_num = len(list(nx.connected_components(topo_graph)))
    return count_num


# 求解拓扑结果中所有节点对之间的最短路径及其对应的qoe指标
def all_shortest_path_cal(topo_graph, qoe_data, demand):
    shortest_path_map = {}
    for key in list(combinations(topo_graph.nodes(), 2)):
        best = -1
        shortest_path_map[str(key)] = {}
        for path in build_all_simple_paths(topo_graph, key[0], key[1], pocomputing_demand_parser.get_max_hop(demand)):
            if not ' '.join(path) in qoe_data.index:
                continue
            cur = qoe_data.loc[' '.join(path), pocomputing_demand_parser.get_qoe_indicator_name(demand)]
            if cur > best:
                best = cur
                shortest_path_map[str(key)]['shortest_path'] = path
                shortest_path_map[str(key)]['value'] = best
    return shortest_path_map


# 点破坏度
def point_destructive_degree_cal(topo_graph, shortest_path_map):
    point_destructive_degree_map = {}
    total = len(list(combinations(topo_graph.nodes(), 2)))
    for value in shortest_path_map.values():
        for node in value['shortest_path']:
            if node in point_destructive_degree_map:
                point_destructive_degree_map[node] = point_destructive_degree_map[node] + 1
            else:
                point_destructive_degree_map[node] = 1
    for k, v in point_destructive_degree_map.items():
        point_destructive_degree_map[k] = 1.0 * v / total
    return point_destructive_degree_map


# 边破坏度
def edge_destructive_degree_cal(topo_graph, shortest_path_map):
    edge_destructive_degree_map = {}
    total = len(list(combinations(topo_graph.nodes(), 2)))
    for value in shortest_path_map.values():
        for i in range(0, len(value['shortest_path']) - 1):
            key1 = (value['shortest_path'][i], value['shortest_path'][i + 1])
            key2 = (value['shortest_path'][i + 1], value['shortest_path'][i])
            if key1 in edge_destructive_degree_map:
                edge_destructive_degree_map[key1] = edge_destructive_degree_map[key1] + 1
            elif key2 in edge_destructive_degree_map:
                edge_destructive_degree_map[key2] = edge_destructive_degree_map[key2] + 1
            else:
                edge_destructive_degree_map[key1] = 1
    for node1, node2 in list(combinations(topo_graph.nodes(), 2)):
        if (node1, node2) not in edge_destructive_degree_map and (node2, node1) not in edge_destructive_degree_map:
            edge_destructive_degree_map[(node1, node2)] = 0
    for k, v in edge_destructive_degree_map.items():
        edge_destructive_degree_map[k] = 1.0 * v / total
    return edge_destructive_degree_map


# 紧密中心性
def closeness_centrality_cal(topo_graph, qoe_data, demand):
    data = pd.DataFrame(columns = ['node_name', 'closeness_centrality'])
    for node in topo_graph.nodes():
        cur = 0
        for des in topo_graph.nodes():
            path = ' '.join([node, des])
            if des != node and path in qoe_data.index:
                cur += qoe_data.loc[path, pocomputing_demand_parser.get_qoe_indicator_name(demand)]
        data = data.append(pd.DataFrame({'node_name':str(node), 'closeness_centrality':cur},index = [0]),ignore_index=True)
        # cur = 0
        # for key in shortest_path_map:
        #     if node in key:
        #         cur += 1 / shortest_path_map[key]['value']
    data.set_index('node_name', inplace=True)
    return data
