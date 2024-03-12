# -*- coding: utf-8 -*-
import pandas as pd
import networkx as nx

################################################################################
#构造程序中拓扑数据结构：topo_graph
###topo_graph；networkx模块提供的拓扑数据结构，便于计算各种数据
#    类型为networkx.classes.graph.Graph/networkx.classes.graph.DiGraph
#

def build_topo_graph_from_edges(edge_list, bi = True) :
    topo_graph = None
    if type(edge_list) is list :
        edge_list = [(edge[0], edge[1]) for edge in edge_list if len(edge) == 2]
    if bi == True :
        topo_graph = nx.Graph()
        redge_list = set([(edge_2, edge_1) for edge_1, edge_2 in set(edge_list)])
        nedge_list = redge_list.intersection(set(edge_list))
        topo_graph.add_edges_from(list(nedge_list))
    else :
        topo_graph = nx.DiGraph()
        topo_graph.add_edges_from(edge_list)
    return topo_graph

def is_node_in_graph(topo_graph, node) :
    is_in = topo_graph.has_node(node)
    return is_in

def is_edge_in_graph(topo_graph, edge) :
    if not type(edge) is list and not type(edge) is tuple:
        return False
    if not len(edge) == 2 :
        return False
    is_in = topo_graph.has_edge(edge[0], edge[1])
    return is_in

def is_path_in_graph(topo_graph, path) :
    if not type(path) is list :
        return False
    if len(path) < 2 :
        return False
    segment_path = zip(path[:-1], path[1:])
    is_in_list = map(is_edge_in_graph, [topo_graph] * len(segment_path), segment_path)
    is_in = (len(is_in_list) == sum(is_in_list))
    return is_in

def get_edges_from_topo_graph(topo_graph) :
    edge_list = list(topo_graph.edges)
    if not topo_graph.is_directed() :
        redge_list = [(edge[1], edge[0]) for edge in edge_list]
        edge_list.extend(redge_list)
    return edge_list

def get_nodes_from_topo_graph(topo_graph) :
    node_list = list(topo_graph.nodes)
    return node_list

def get_neighbors_from_topo_graph(topo_graph, source_name) :
    des_list = list(topo_graph.neighbors(source_name))
    return des_list

def print_edges_in_topo_graph(topo_graph) :
    for source_name in topo_graph.nodes :
        neighbors = topo_graph.neighbors(source_name)
        for des_name in neighbors :
            print (str(source_name) + ' ' + str(des_name))

def topo_graph_join(topo_graph_1, topo_graph_2, bi = True) :
    topo_graph = None
    if bi == True :
        topo_graph = nx.Graph()
    else :
        topo_graph = nx.DiGraph()
    edge_list = set(get_edges_from_topo_graph(topo_graph_1))
    edge_list = edge_list.intersection(set(get_edges_from_topo_graph(topo_graph_2)))
    edge_list = list(edge_list)
    topo_graph.add_edges_from(edge_list)
    return topo_graph

def topo_graph_list_join(topo_graph_list, bi = True) :
    i = 1
    if len(topo_graph_list) == 0 or not type(topo_graph_list) == type([]):
        return {}
    tmp_topo_graph = topo_graph_list[0]
    while i < len(topo_graph_list) :
        tmp_topo_graph = topo_graph_join(tmp_topo_graph, topo_graph_list[i], bi)
        i = i + 1
    topo_graph = tmp_topo_graph
    return topo_graph