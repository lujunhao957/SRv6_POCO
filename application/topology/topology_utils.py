# -*- coding: utf-8 -*-
import sys
import topology.topology_handler as topology_handler

def build_topo_graph_dict(topo_graph) :
    topo_graph_dict = {}
    node_list = topology_handler.get_nodes_from_topo_graph(topo_graph)
    for source_name in node_list :
        neighbor_list = topology_handler.get_neighbors_from_topo_graph(topo_graph, source_name)
        topo_graph_dict[source_name] = neighbor_list
    return topo_graph_dict

def build_topo_graph_by_graph_dict(topo_graph_dict, bi = True) : 
    edge_list = []
    for source_name in topo_graph_dict :
        if not type(topo_graph_dict[source_name]) is type([]) :
            continue
        edge_list.extend([(str(source_name), str(des_name)) \
                           for des_name in topo_graph_dict[source_name]])
    topo_graph = topology_handler.build_topo_graph_from_edges(edge_list, bi = bi)
    return topo_graph