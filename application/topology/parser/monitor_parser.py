# -*- coding: utf-8 -*-
import pandas as pd
import topology.topology_handler as topology_handler

################################################################################
#从测量平台得到的网络拓扑数据解析工具
#解析得到的结果：节点集，拓扑图，以及节点ID映射集
#
####pd_monitor_topo_data，类型为pandas.DataFrame()
#列名包括：
#    source_name,以及des_name两项

#从QoS指标数据中，提取网络节点名称集合
#    pd_monitor_topo_data，类型为pandas.DataFrame()
#return：网络中节点集合，类型为List<str>，例如['BJ_OVS', ..., 'SH_OVS']
#    类型为host_list
def parse_monitor_host_list(pd_monitor_topo_data) :
    source_set = set(pd_monitor_topo_data.source_name.unique())
    des_set = set(pd_monitor_topo_data.des_name.unique())
    host_list = list(source_set.intersection(des_set))
    return host_list

#从QoS指标数据中，提取网络拓扑
#    pd_monitor_topo_data，类型为pandas.DataFrame()
#return：网络中拓扑信息，类型为networkx
#类型为topo_graph
def parse_monitor_topo_graph(pd_monitor_topo_data) :
    pd_monitor_topo_data = pd_monitor_topo_data.copy()
    pd_monitor_topo_data.set_index('source_name', inplace = True)
    pd_monitor_topo_data = pd_monitor_topo_data.des_name
    pedge_set = set(); nedge_set = set()
    for source_name, des_name in pd_monitor_topo_data.iteritems() :
        pedge_set.add((source_name, des_name))
        nedge_set.add((des_name, source_name))
    bi_edge_list = list(pedge_set.intersection(nedge_set))
    topo_graph = topology_handler.build_topo_graph_from_edges(bi_edge_list, bi = True)
    return topo_graph