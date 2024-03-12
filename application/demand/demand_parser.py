# -*- coding: utf-8 -*-
import json
import copy
import topology.topology_handler as topology_handler


def get_source_name(pocomputing_demand, poco_idname_map):
    source_id = pocomputing_demand['source_node']
    if source_id in poco_idname_map:
        source_name = poco_idname_map[source_id]
        return source_name


def get_des_name(pocomputing_demand, poco_idname_map):
    des_id = pocomputing_demand['dest_node']
    if des_id in poco_idname_map:
        des_name = poco_idname_map[des_id]
        return des_name


def get_path_count(pocomputing_demand):
    path_count = pocomputing_demand['path_count']
    return path_count


def get_max_hop(pocomputing_demand):
    max_hop = pocomputing_demand['max_hop']
    return max_hop

def get_source_id(pocomputing_demand):
    source_node = pocomputing_demand['source_node']
    return source_node

def get_des_id(pocomputing_demand):
    dest_node = pocomputing_demand['dest_node']
    return dest_node

def get_webrtc_quality(pocomputing_demand):
    webrtc_quality = pocomputing_demand['webrtc_quality']
    return webrtc_quality


def get_max_damage(pocomputing_demand):
    max_damage = pocomputing_demand['max_damage']
    return max_damage


def get_sort_indicator_name(pocomputing_demand):
    indicator_name = pocomputing_demand['sort_by']
    return indicator_name


def get_percentile(pocomputing_demand):
    percentile = pocomputing_demand['options']['addition']['percentile']
    return percentile


def get_demand_type(pocomputing_demand):
    demand_type = pocomputing_demand['demand_type']
    return demand_type


def get_sort_acecnding(pocomputing_demand):
    ascending = pocomputing_demand['ascending']
    return ascending


def get_qos_demand(pocomputing_demand):
    qos_demand = pocomputing_demand['qos_demand']
    return qos_demand


def get_qos_deviation(pocomputing_demand):
    qos_deviation = pocomputing_demand['options']['qos'].copy()
    qos_deviation = {qos_name: qos_option['deviation'] \
                     for qos_name, qos_option in qos_deviation.items() \
                     if (type(qos_option) is dict) and 'deviation' in qos_option}
    return qos_deviation


def get_ping_packet_size(pocomputing_demand):
    packet_size = pocomputing_demand['options']['qos']['packet_size']
    return packet_size


def get_poco_demand_topo_graph(pocomputing_demand, poco_idname_map):
    demand_type = pocomputing_demand['demand_type']
    try:
        if demand_type in ['backbone']:
            user_side_links = pocomputing_demand['topology_info']['user_side_links']
            edge_list = [(poco_idname_map[link[0]], poco_idname_map[link[1]]) \
                         for link in user_side_links if type(link) is list and len(link) == 2]
            topo_graph = topology_handler.build_topo_graph_from_edges(edge_list, bi=True)
            return topo_graph
        elif demand_type in ['user']:
            user_side_links = pocomputing_demand['topology_info']['user_side_links']
            edge_list = [(poco_idname_map[link[0]], poco_idname_map[link[1]]) \
                         for link in user_side_links if type(link) is list and len(link) == 2]
            if 'backbone_side_links' in pocomputing_demand['topology_info']:
                # backbone_side_links = pocomputing_demand['topology_info']['backbone_side_links']
                # backbone_side_links = [link[0] for link in backbone_side_links
                # if type(link) is list and len(link) == 2]
                # edge_list.extend([(poco_idname_map[link[0]], poco_idname_map[link[1]]) \
                #                   for link in backbone_side_links if type(link) is list and len(link) == 2])
                #  fxbing update
                # 处理逻辑见下面get_real_path_map中的注释
                backbone_side_links = pocomputing_demand['topology_info']['backbone_side_links']
                user_side_links = pocomputing_demand['topology_info']['user_side_links']
                real_node_map = {}
                for backbone_link in backbone_side_links:
                    if len(backbone_link[1]):
                        real_node_map[poco_idname_map[backbone_link[1][0][0]] + ":" + backbone_link[0]] = \
                            backbone_link[1][0][0]
                        real_node_map[poco_idname_map[backbone_link[1][0][1]] + ":" + backbone_link[0]] = \
                            backbone_link[1][0][1]
                for k, v in real_node_map.items():
                    for user_link in user_side_links:
                        if len(user_link) == 2:
                            if user_link[0] == v and user_link[1] not in real_node_map.values():
                                edge_list.extend([(k, poco_idname_map[user_link[1]])])
                            if user_link[1] == v and user_link[0] not in real_node_map.values():
                                edge_list.extend([(poco_idname_map[user_link[0]], k)])
                for backbone_link in backbone_side_links:
                    if not len(backbone_link[1]):
                        continue
                    edge_list.extend([(str(poco_idname_map[link[0]]) + ":" + backbone_link[0],
                                       str(poco_idname_map[link[1]]) + ":" + backbone_link[0])
                                      for link in backbone_link[1] if type(link) is list and len(link) == 2])
                # print "get_poco_demand_topo_graph拓扑图:"
                # print edge_list
            topo_graph = topology_handler.build_topo_graph_from_edges(edge_list, bi=True)
            return topo_graph
    except:
        return None


# def get_poco_overlay_topo_graph(pocomputing_demand, poco_idname_map):
#     demand_type = pocomputing_demand['demand_type']
#     try:
#         if demand_type in ['backbone']:
#             user_side_links = pocomputing_demand['topology_info']['user_side_links']
#             edge_list = [(poco_idname_map[link[0]], poco_idname_map[link[1]]) \
#                          for link in user_side_links if type(link) is list and len(link) == 2]
#             topo_graph = topology_handler.build_topo_graph_from_edges(edge_list, bi=True)
#             return topo_graph
#         elif demand_type in ['user']:
#             user_side_links = pocomputing_demand['topology_info']['user_side_links']
#             edge_list = [(poco_idname_map[link[0]], poco_idname_map[link[1]]) \
#                          for link in user_side_links if type(link) is list and len(link) == 2]
#             if 'backbone_side_links' in pocomputing_demand['topology_info']:
#                 tmp_list = []
#                 backbone_side_links = pocomputing_demand['topology_info']['backbone_side_links']
#                 backbone_side_links = [zip(link[1][:-1], link[1][1:]) for link in backbone_side_links \
#                                       if type(link) is list and len(link) == 2]
#                 map(lambda vlink_list: tmp_list.extend(vlink_list), backbone_side_links)
#                 tmp_list = [list(vlink) for vlink in tmp_list]
#                 backbone_side_links = tmp_list
#                 edge_list.extend([(poco_idname_map[link[0]], poco_idname_map[link[1]]) \
#                                   for link in backbone_side_links if type(link) is list and len(link) == 2])
#             topo_graph = topology_handler.build_topo_graph_from_edges(edge_list, bi=True)
#             return topo_graph
#     except Exception, e:
#         print "get_poco_overlay_topo_graph ERROR："
#         print e.args
#         return None
#  fxbing update
def get_poco_overlay_topo_graph(pocomputing_demand, poco_idname_map):
    demand_type = pocomputing_demand['demand_type']
    try:
        if demand_type in ['backbone']:
            user_side_links = pocomputing_demand['topology_info']['user_side_links']
            edge_list = [(poco_idname_map[link[0]], poco_idname_map[link[1]]) \
                         for link in user_side_links if type(link) is list and len(link) == 2]
            topo_graph = topology_handler.build_topo_graph_from_edges(edge_list, bi=True)
            return topo_graph
        elif demand_type in ['user']:
            user_side_links = pocomputing_demand['topology_info']['user_side_links']
            print (user_side_links)
            print (poco_idname_map)
            edge_list = [(poco_idname_map[link[0]], poco_idname_map[link[1]]) \
                         for link in user_side_links if type(link) is list and len(link) == 2]
            if 'backbone_side_links' in pocomputing_demand['topology_info']:
                # 处理逻辑见下面get_real_path_map中的注释
                backbone_side_links = pocomputing_demand['topology_info']['backbone_side_links']
                user_side_links = pocomputing_demand['topology_info']['user_side_links']
                real_node_map = {}
                for backbone_link in  backbone_side_links:
                    if len(backbone_link[1]):
                        real_node_map[poco_idname_map[backbone_link[1][0][0]] + ":" + backbone_link[0]] = \
                        backbone_link[1][0][0]
                        real_node_map[poco_idname_map[backbone_link[1][0][1]] + ":" + backbone_link[0]] = \
                        backbone_link[1][0][1]
                for k, v in real_node_map.items():
                    for user_link in user_side_links:
                        if len(user_link) == 2:
                            if user_link[0] == v and user_link[1] not in real_node_map.values():
                                edge_list.extend([(k, poco_idname_map[user_link[1]])])
                            if user_link[1] == v and user_link[0] not in real_node_map.values():
                                edge_list.extend([(poco_idname_map[user_link[0]], k)])
                for backbone_link in backbone_side_links:
                    if not len(backbone_link[1]):
                        continue
                    edge_list.extend([(str(poco_idname_map[link[0]]) + ":" + backbone_link[0],
                                      str(poco_idname_map[link[1]]) + ":" + backbone_link[0])
                                     for link in backbone_link[1] if type(link) is list and len(link) == 2])
                # print "get_poco_overlay_topo_graph拓扑图:"
                # print edge_list
            topo_graph = topology_handler.build_topo_graph_from_edges(edge_list, bi=True)
            return topo_graph
    except Exception as e:

        return None

# def get_real_path_map(pocomputing_demand, poco_idname_map) :
#     demand_type = pocomputing_demand['demand_type']
#     if not demand_type in ['user'] or not 'backbone_side_links' in pocomputing_demand['topology_info'] :
#         return []
#     backbone_side_links = pocomputing_demand['topology_info']['backbone_side_links']
#     def one_backbone_link_parser(backbone_link_item) :
#         try :
#             vpath = backbone_link_item[0][:]
#             vlink = backbone_link_item[1][:]
#             if len(vpath) < 2 or len(vlink) < 2 :
#                 return []
#             vpath = map(lambda node_id : poco_idname_map[node_id], vpath)
#             vlink = map(lambda node_id : poco_idname_map[node_id], vlink)
#             return [vpath, vlink]
#         except :
#             return []
#     real_path_kv = map(one_backbone_link_parser, backbone_side_links)
#     real_path_map = {(one_kv[0][0], one_kv[0][1]) : one_kv[1] \
#                          for one_kv in real_path_kv \
#                          if (len(one_kv) == 2)}
#     return real_path_map

#  fxbing update


def get_real_path_map(pocomputing_demand, poco_idname_map):
    demand_type = pocomputing_demand['demand_type']
    if not demand_type in ['user'] or not 'backbone_side_links' in pocomputing_demand['topology_info']:
        return []
    # 原拓扑为：a-b-c-d，其中b-c为骨干虚拟专线，将其映射为：
    # a-b-c-d
    # \    /
    #  b1-c1
    # 其中b-c为没有虚拟专线的虚拟链路，b1-c1为骨干虚拟专线数据
    backbone_side_links = pocomputing_demand['topology_info']['backbone_side_links']
    user_side_links = pocomputing_demand['topology_info']['user_side_links']
    #  backbone_side_links 的格式为 [[u'999', [[15, 13], [13, 15]]]]
    #  同一个需求中的两条链路的节点相同，所以只要根据backbone_link[1][0]来获取real_node_map就可以
    real_node_map = {}
    for backbone_link in backbone_side_links:
        if len(backbone_link[1]):
            real_node_map[poco_idname_map[backbone_link[1][0][0]] + ":" + backbone_link[0]] = backbone_link[1][0][0]
            real_node_map[poco_idname_map[backbone_link[1][0][1]] + ":" + backbone_link[0]] = backbone_link[1][0][1]
    # 获得{(a, b1):(a, b), (c1, d):(c, d)}映射关系
    tmp_map = {}
    for k, v in real_node_map.items():
        for user_link in user_side_links:
            if len(user_link) == 2:
                if user_link[0] == v and user_link[1] not in real_node_map.values():
                    tmp_map[(k, poco_idname_map[user_link[1]])] = (user_link[0], user_link[1])
                if user_link[1] == v and user_link[0] not in real_node_map.values():
                    tmp_map[(poco_idname_map[user_link[0]], k)] = (user_link[0], user_link[1])
    # 获得{(b1, c1):(b, c)}映射关系
    real_path_map = {}
    for backbone_link in backbone_side_links:
        demand_id = backbone_link[0]
        if not len(backbone_link[1]):
            continue
        for link in backbone_link[1]:
            real_path_map[(poco_idname_map[link[0]] + ":" + demand_id, poco_idname_map[link[1]] + ":" + demand_id)] =  \
                (link[0], link[1])
    # 组合
    real_path_map.update(tmp_map)
    return real_path_map


def is_damage_calculated(pocomputing_demand):
    if not 'topology_demand' in pocomputing_demand:
        return False
    topology_demand = pocomputing_demand['topology_demand']
    if not ('damage' in topology_demand and 'max' in topology_demand['damage']):
        return False
    max_damage = topology_demand['damage']['max']
    if not (type(max_damage) is int or type(max_damage) is float):
        return False
    if abs(max_damage - 1.0) <= 1e-4:
        return False
    return True


def get_max_damage(pocomputing_demand):
    if not is_damage_calculated(pocomputing_demand):
        return 1.0
    topology_demand = pocomputing_demand['topology_demand']
    max_damage = 1.0 * topology_demand['damage']['max']
    return max_damage


def is_instab_caculated(pocomputing_demand):
    if 'options' in pocomputing_demand and 'instability' in pocomputing_demand['options']:
        return True
    return False


def is_qoe_calculated(pocomputing_demand):
    if 'options' in pocomputing_demand and 'qoe' in pocomputing_demand['options']:
        return True
    return False


def get_demand_type(pocomputing_demand):
    demand_type = pocomputing_demand['demand_type']
    return demand_type


def get_instab_service_type(pocomputing_demand):
    service_type = pocomputing_demand['options']['instability']['service_type']
    return service_type


def get_qoe_service_type(pocomputing_demand):
    service_type = pocomputing_demand['options']['qoe']['service_type']
    return service_type


def get_qoe_indicator_name(pocomputing_demand):
    indicator_name = pocomputing_demand['options']['qoe']['indicator_name']
    return indicator_name
