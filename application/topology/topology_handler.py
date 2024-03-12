# -*- coding: utf-8 -*-
import sys
import topology.topology_handler


def build_graph_by_vlinks(vlink_list, bi=True):
    topo_graph = topology.topology_handler.build_topo_graph_from_edges(vlink_list, bi=True)
    return topo_graph


def build_all_vlinks(topo_graph):
    vlink_list = topology.topology_handler.get_edges_from_topo_graph(topo_graph)
    return vlink_list


def build_all_simple_vpaths(topo_graph, source_name, des_name, max_hop=5, max_path=10000000000001):
    if not (topology.topology_handler.is_node_in_graph(topo_graph, source_name) and \
            topology.topology_handler.is_node_in_graph(topo_graph, des_name)):
        return []
    path_list = topology.topology_calc.build_all_simple_paths(topo_graph, source_name, des_name, max_hop, max_path)
    return path_list


def topo_graph_list_join(topo_graph_list, bi=True):
    ntopo_graph = topology.topology_handler.topo_graph_list_join(topo_graph_list, bi=bi)
    return ntopo_graph

