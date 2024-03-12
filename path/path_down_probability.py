# -*- coding: utf-8 -*-
from itertools import combinations
import pandas as pd
import sys
sys.path.append("..")


# 单条虚拟专线中断的概率
def single_path_down_probability(link_down_data, path):
    ans = 1
    for i in range(0, len(path) - 1):
        ans *= (1 - link_down_data[(path[i], path[i + 1])])
    return 1 - ans


# 一组虚拟专线中断的概率
def path_group_down_probability(link_down_data, path_link_map, path_group, target):
    ans = 0
    for i in range(1, len(path_group) + 1):
        tmp = 0
        for muti_path in list(combinations(path_group, i)):
            cur = path_group_up_probability(link_down_data, path_link_map, muti_path, target)
            if cur is False:
                return False
            tmp += cur
        ans += pow(-1, i + 1) * tmp
    return 1 - ans


def path_group_up_probability(link_down_data, path_link_map, path_group, target):
    link_set = path_group_link_set(path_group, path_link_map)
    ans = 1
    for link in link_set:
        if link in link_down_data:
            ans *= (1 - link_down_data[link])
    if target is not None and (1 - ans) <= target:
        return False
    return ans


def path_group_link_set(path_group, path_link_map):
    link_set = set()
    for path in path_group:
        for link in path_link_map[str(path)]:
            link_set.add(link)
    return link_set


# 所有虚拟专线同时中断的概率
# def all_path_down_probability(link_down_data, all_paths, path_link_map, target):
#     # 分组
#     path_groups = path_grouping(all_paths, path_link_map)
#     # 计算
#     ans = 1
#     for path_group in path_groups:
#         cur = path_group_down_probability(link_down_data, path_link_map, path_group, target)
#         if cur is False:
#             return False
#         ans *= cur
#     return ans
def all_path_down_probability(all_paths, paths_data, demand):
    def f(packet_loss, rta):
        return 0 if ((packet_loss > demand['qos_demand']['packet_loss']['max']) | (rta > demand['qos_demand']['rta']['max'])) else 1
    tmp_data = pd.DataFrame()
    for path in all_paths:
        path_data = paths_data[str(path)]
        if 'is_ok' in tmp_data.columns:
            tmp_data['tmp'] = path_data.apply(lambda row: f(row['packet_loss'], row['rta']), axis=1)
            tmp_data['is_ok'] = tmp_data['is_ok'] + tmp_data['tmp']
        else:
            tmp_data['is_ok'] = path_data.apply(lambda row: f(row['packet_loss'], row['rta']), axis=1)
    current = tmp_data[tmp_data['is_ok'] == 0].shape[0]
    original = tmp_data.shape[0]
    return 1.0 * current / original


#  最多n条同时失效概率
def n_path_down_probability(all_paths, paths_data, demand, n):
    def f(packet_loss, rta):
        return 0 if ((packet_loss > demand['qos_demand']['packet_loss']['max']) | (rta > demand['qos_demand']['rta']['max'])) else 1
    tmp_data = pd.DataFrame()
    for path in all_paths:
        path_data = paths_data[str(path)]
        if 'is_ok' in tmp_data.columns:
            tmp_data['tmp'] = path_data.apply(lambda row: f(row['packet_loss'], row['rta']), axis=1)
            tmp_data['is_ok'] = tmp_data['is_ok'] + tmp_data['tmp']
        else:
            tmp_data['is_ok'] = path_data.apply(lambda row: f(row['packet_loss'], row['rta']), axis=1)
    current = tmp_data[tmp_data['is_ok'] >= len(all_paths) - n].shape[0]
    original = tmp_data.shape[0]
    return 1 - 1.0 * current / original

# 根据是否重叠对虚拟专线进行分组
def path_grouping(all_paths, path_link_map):
    group_tag_map = {}  # <路径，路径标志（其他路径或该路径本身）>
    for path in all_paths:
        group_tag_map[str(path)] = str(path)
    for i in range(1, len(all_paths)):
        for j in range(0, i):
            if group_tag_map[str(all_paths[i])] != group_tag_map[str(all_paths[j])] and \
                    (path_link_map[str(all_paths[i])] & path_link_map[str(all_paths[j])]):
                for k in range(0, i):
                    if group_tag_map[str(all_paths[k])] == group_tag_map[str(all_paths[j])]:
                        group_tag_map[str(all_paths[k])] = str(all_paths[i])
                group_tag_map[str(all_paths[j])] = str(all_paths[i])
    path_groups = {}  # <路径标志，该标志对应的路径的列表>
    for k, v in group_tag_map.items():
        if v not in path_groups:
            path_groups[v] = set()
        path_groups[v].add(str(k))
    return path_groups.values()
