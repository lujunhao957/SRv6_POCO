# -*- coding: utf-8 -*-
import os
import sys

def gpath_list_damage_filter(group_path_list, max_damage = 1.0) :
    if len(group_path_list) == 0 :
        return []
    path_list_map = [(path_list, path_list_damage_cal(path_list)) for path_list in group_path_list]
    path_list_map = filter(lambda x : x[1] <= max_damage, path_list_map)
    group_path_list = [path_list_kv[0] for path_list_kv in path_list_map]
    return group_path_list


def path_list_damage_cal(path_list) :
    segment_path_map = {}

    temp_path_list=[]

    for path_info in path_list:
        temp_path_list.append(path_info.get_path())

    for path in temp_path_list :
        i = 0
        path_hop = len(path) - 1
        while i < path_hop:            
            s_path = path[i]; d_path = path[i + 1]            
            if (path[i], path[i + 1]) in segment_path_map :
                segment_path_map[s_path, d_path] = segment_path_map[s_path, d_path] + 1.0
            else :
                segment_path_map[s_path, d_path] = 1.0
            i = i + 1
    return 1.0 * max(segment_path_map.values()) / len(path_list)
