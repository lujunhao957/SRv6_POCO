# -*- coding: utf-8 -*-
import pandas as pd
import application.topology.topology_utils as topology_utils

################################################################################
#从POCOMPUTING数据库得到的网络拓扑数据解析工具
#解析得到的结果：节点集，拓扑图，以及节点ID映射集
#
###pd_poco_host_data，类型为pandas.DataFrame()
#其数据列名包括：
#    node_id：即pocomputing中节点的ID，类型为int。例如：12
#    node_name：即pocomputing中节点的名称，类型为str。例如：Digital_Ocean_Amsterdam
#    latitude：即节点所在的纬度(float)
#    longitude：即节点所在的经度(float)
#    poco_id：即在POCO中的ID信息，用于将求解POCO不同ID之间的路径问题，以Pocomputing
#    内部ID的形式进行，以对整个系统解耦
#
###pd_poco_topo_data，从Pocomputing数据库中读取得到的网络拓扑，类型为pandas.DataFrame()  
#其数据列名包括：
#    node_id：即pocomputing中节点的ID，类型为int。例如：12
#    node_name：即pocomputing中节点的名称，类型为str。例如：Digital_Ocean_Amsterdam
#    neighbor_id：即pocomputing中当前节点的邻居ID，类型为str，以'|'分割。例如：
#        13|14|15|16|17|18|23|45|46
#    neighbor_name，即neighbor_id中ID全部按顺序转换为name。类型为str，以'|'分割。例如：
#        Digital_Ocean_Frankfurt|Digital_Ocean_London|...|Tietong_156-ovs
#    timestamp：即更新时间戳
#
###topo_graph：网络中拓扑信息，类型为networkx
#

#从POCOMPUTING数据表中，提取网络节点名称集合
#    pd_poco_host_data，类型为pandas.DataFrame()
#return：网络中节点集合，类型为List<str>，例如['BJ_OVS', ..., 'SH_OVS']
#    类型为host_list
def parse_pocomputing_host_list(pd_poco_host_data) :
    host_list = list(pd_poco_host_data.node_name.unique())
    return host_list

#从POCOMPUTING数据表中，提取网络节点名称集合
#    pd_poco_host_data，类型为pandas.DataFrame()
#return：Pocomputing中，Pocomputing ID(int)与节点名(str)映射Dict
#    类型为Dict，例如{1:'BJ_OVS'}
def parse_pocomputing_idname_map(pd_poco_host_data) :
    node_info = pd_poco_host_data.copy()
    id_name_map = {node_id : node_name for node_id , node_name in zip(node_info.node_id, node_info.node_name)}
    return id_name_map

#从POCOMPUTING数据表中，提取网络节点名称集合
#    pd_poco_host_data，类型为pandas.DataFrame()
#return：Pocomputing中，节点名(str)与Pocomputing ID(int)映射Dict
#    类型为Dict，例如{'BJ_OVS':1}
def parse_pocomputing_nameid_map(pd_poco_host_data) :
    node_info = pd_poco_host_data.copy()
    name_id_map = {node_name : node_id for node_id , node_name in zip(node_info.node_id, node_info.node_name)}
    return name_id_map

#从POCOMPUTING数据表中，提取网络节点名称集合
#    pd_poco_host_data，类型为pandas.DataFrame()
#return：Pocomputing中，Poco ID(int,如PMS/PMA ID)与节点名(str)映射Dict
#    类型为Dict，例如{1:'BJ_OVS'}
def parse_poco_idname_map(pd_poco_host_data) :
    node_info = pd_poco_host_data.copy()
    node_info = node_info.dropna(subset=["poco_id"])
    id_name_map = {int(poco_id) : node_name for poco_id , node_name in zip(node_info.poco_id, node_info.node_name)}
    #id_name_map.pop(None)
    return id_name_map

#从POCOMPUTING数据表中，提取网络节点名称集合
#    pd_poco_host_data，类型为pandas.DataFrame()
#return：Pocomputing中，节点名(str)与Poco ID(int,如PMS/PMA ID)映射Dict
#    类型为Dict，例如{1:'BJ_OVS'}
def parse_poco_nameid_map(pd_poco_host_data) :
    node_info = pd_poco_host_data.copy()
    node_info = node_info.dropna(subset=["poco_id"])
    name_id_map = {node_name : int(poco_id) for poco_id , node_name in zip(node_info.poco_id, node_info.node_name)}
    return name_id_map

#从POCOMPUTING数据表中，提取网络节点拓扑信息
#    pd_poco_host_data，类型为pandas.DataFrame()
#return：网络中拓扑信息，类型为Map<str, List<str>>
#类型为topo_graph，例如:
#    topo_graph = {
#        'BJ_OVS' : ['SH_OVS', 'SZ_OVS'],
#        'SH_OVS' : ['BJ_OVS', 'SZ_OVS'],
#        'SZ_OVS' : ['BJ_OVS', 'SH_OVS']
#    }
#    每对KV为节点与邻居节点名集合
def parse_pocomputing_topo_graph(pd_poco_topo_data) :
    pd_poco_topo_data = pd_poco_topo_data.copy().set_index('node_id')
    if pd_poco_topo_data.empty :
        print ("basic_database : load from basic database fail")
        return pd.DataFrame()
    name_id_map = {node_id : node_name for node_id, node_name in zip(pd_poco_topo_data.index, pd_poco_topo_data.node_name)}
    topo_graph_dict = {node_name : map(lambda neighbor_name : name_id_map[int(neighbor_name)], neighbor_name_list.split('|')) \
                  for node_name, neighbor_name_list in zip(pd_poco_topo_data.node_name, pd_poco_topo_data.neighbor_id)}
    topo_graph = topology_utils.build_topo_graph_by_graph_dict(topo_graph_dict, bi = True)
    return topo_graph