# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
import path.utils as path_utils

def get_segment_path(path) :
    segment_path = zip(path[:-1], path[1:])
    return segment_path

#def get_segment_path(path) :
#    segment_path = []
#    for i in range(0, len(path) - 1):
#        segment_path.append((path[i], path[i+1]))
#    return segment_path

def reduce_segment_path(segment_path) :
    path = [source_name for source_name, des_name in segment_path]
    path.append(segment_path[-1][1])
    return path

#nest_path = ['A', 'B', 'C', 'D']
#real_path_map = {('B', 'C') : ['B', 'E', 'F', 'C'],
#            ('B', 'E') : ['B', 'G', 'E']}
def elim_nest_path(nest_path, real_path_map) :
    if not (type(nest_path) is list and type(real_path_map) is dict) :
        return nest_path
    nest_segment_path = zip(nest_path[:-1], nest_path[1:])
    nest_segment_path = [
        real_path_map[source_name, des_name] \
        if (source_name, des_name) in real_path_map else [source_name, des_name]
        for (source_name, des_name) in nest_segment_path
    ]
    last_node_name = nest_segment_path[-1][-1]
    nest_segment_path = [
        one_path[:-1]
        for one_path in nest_segment_path
    ]
    path = path_utils.flatten_list(nest_segment_path)
    path.append(last_node_name)
    return path
    
def build_gpath_list(path_list, group_path_count) :
    group_path_list = []
    path_count = len(path_list)
    if group_path_count > len(path_list) :
        return group_path_list   
    stack = list(range(0, group_path_count))
    first = stack[:]
    last = range(path_count - group_path_count, path_count)
    pos = group_path_count - 1
    lastm = group_path_count - 1
    group_path_list.append(path_list[0 : group_path_count])
    while True :
        if stack[pos] < last[pos]:
            stack[pos] = int(stack[pos])+1
            temp = stack[pos]
            pos = pos + 1
            if pos <= lastm :
                stack[pos] = temp
        else :
            pos = pos - 1
            if pos < 0 :
                break
        if pos > lastm :
            group_path_list.append([path_list[x] for x in stack])
            pos = lastm
    return group_path_list