# -*- coding: utf-8 -*-
import topology.topology_calc as topology_calc


def all_shortest_path_cal(topo_graph, qoe_data, demand):
    return topology_calc.all_shortest_path_cal(topo_graph, qoe_data, demand)


def point_destructive_degree_cal(topo_graph, shortest_path_map):
    return topology_calc.point_destructive_degree_cal(topo_graph, shortest_path_map)


def edge_destructive_degree_cal(topo_graph, shortest_path_map):
    return topology_calc.edge_destructive_degree_cal(topo_graph, shortest_path_map)


def closeness_centrality_cal(topo_graph, qoe_data, demand):
    return topology_calc.closeness_centrality_cal(topo_graph, qoe_data, demand)
