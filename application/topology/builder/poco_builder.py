# -*- coding: utf-8 -*-
import pandas as pd
import utils.datetime_utils as datetime_utils
import application.topology.topology_utils as topology_utils

#基于已有的网络节点信息，以及网络拓扑结构，构造相应的数据库表结构
#    topo_graph：网络中拓扑信息，类型为networkx
#    每对KV为节点与邻居节点名集合
#    pd_poco_host_data，类型为pandas.DataFrame()
#return：与Pocomputing数据库中的网络拓扑表结构类似，类型为pandas.DataFrame()  
#    类型为pd_poco_topo_data
def build_poco_topo_data(topo_graph, pd_poco_host_data) :
    pd_poco_host_data = pd_poco_host_data.copy()
    topo_graph_dict = topology_utils.build_topo_graph_dict(topo_graph)
    pd_poco_topo_data = [({'node_id' : node_id, 'node_name' : node_name}) for node_id, node_name in \
                        zip(pd_poco_host_data.node_id, pd_poco_host_data.node_name) if node_name in topo_graph_dict.keys()]
    name_id_mapping = {node_name : node_id for node_name, node_id in zip(pd_poco_host_data.node_name, pd_poco_host_data.node_id)}
    id_name_mapping = {node_id : node_name for node_name, node_id in zip(pd_poco_host_data.node_name, pd_poco_host_data.node_id)}
    timestamp = datetime_utils.timestamp_now()
    def transfer_node_to_row(cur_nodeline) :
        node_name = cur_nodeline['node_name']
        neighbor_name_list = topo_graph_dict[node_name]
        neighbor_name_list = filter(lambda node_name : node_name in name_id_mapping, neighbor_name_list)
        neighbor_id_list = map(lambda node_name : name_id_mapping[node_name], neighbor_name_list)
        neighbor_id_list.sort()
        neighbor_name_list = map(lambda node_id : id_name_mapping[node_id], neighbor_id_list)
        neighbor_name_str = ''
        neighbor_id_str = ''
        for neighbor_name in neighbor_name_list :
            neighbor_name_str = neighbor_name_str + str(neighbor_name) + '|'
        neighbor_name_str = neighbor_name_str[:-1]
        for neighbor_id in neighbor_id_list :
            neighbor_id_str = neighbor_id_str + str(neighbor_id) + '|'
        neighbor_id_str = neighbor_id_str[:-1]
        cur_nodeline.update({'neighbor_id' : neighbor_id_str, 'neighbor_name' : neighbor_name_str, 'timestamp' : timestamp})
        return cur_nodeline
    pd_poco_topo_data = map(lambda cur_info : transfer_node_to_row(cur_info), pd_poco_topo_data)
    pd_poco_topo_data = pd.DataFrame(pd_poco_topo_data)
    pd_poco_topo_data = pd_poco_topo_data[['node_id', 'node_name', 'neighbor_id', 'neighbor_name', 'timestamp']]
    pd_poco_topo_data.set_index('node_id', inplace = True)
    return pd_poco_topo_data