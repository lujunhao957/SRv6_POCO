# -*- coding: utf-8 -*-
import re
import sys


def format_path(path, sep=' '):
    path_str = ''
    for segment_path in path:
        path_str = path_str + str(segment_path) + str(sep)
    path_str = path_str[:-1].strip()
    return path_str


def remove_str_prefix(string, prefix):
    if string[0: len(prefix)] == prefix:
        return string[len(prefix):]
    return string


def split_path(path_str, sep=' '):
    return str(path_str).split(str(sep))


def format_path_list(path_list):
    format_path_list = map(lambda path: format_path(path), path_list)
    return format_path_list


def split_path_list(path_list):
    split_path_list = map(lambda path: split_path(path), path_list)
    return split_path_list


def format_gpath_list(group_path_list):
    fmt_gpath_list = map(lambda group_path: [format_path(path) for path in group_path], group_path_list)
    return fmt_gpath_list


def split_gpath_list(group_path_list):
    spt_gpath_list = map(lambda group_path: [split_path(path) for path in group_path], group_path_list)
    return spt_gpath_list


# 从计算得到的特征数据中，读取可用虚拟专线
# def get_path_list_from_df(feature_data) :
#    if feature_data.empty :
#        return []
#    return split_path_list(list(feature_data.index))

# def format_vpathcal_result(group_path, node_id_mapping):
#     if not group_path:
#         return ''
#     format_func = lambda path_list: reduce(lambda x, y: str(x) + ' ' + str(y),
#                                            [node_id_mapping[poco_id] for poco_id in path_list])
#     tmp_path_list = map(format_func, group_path)
#     format_func = lambda path_str_list: reduce(lambda x, y: str(x) + '|' + str(y), path_str_list)
#     result_path_str = format_func(tmp_path_list)
#     return result_path_str
#  fxbing update
def format_vpathcal_result(group_path, node_id_mapping):
    if not group_path:
        return ''
    result = []
    for path in group_path:
        demand_id = []
        for i in range(1, len(path)):
            if str(path[i - 1]).find(":") != -1 and str(path[i]).find(":") != -1 and \
                    str(path[i - 1]).split(":")[1] == str(path[i]).split(":")[1]:
                demand_id.append(str(path[i - 1]).split(":")[1])
        s = ""
        for node_name in path:
            node_id = node_id_mapping[str(node_name).split(":")[0]]
            s = s + " " + str(node_id)
        # 如果虚拟专线中复用骨干虚拟专线（一个或多个），则在demandId中列出所有复用的骨干虚拟专线
        # 如果没有复用，返回空
        # cur = {"link": s.strip(), "demandId": demand_id if len(demand_id) else None} tfh修改
        cur = {"link": s.strip(), "backboneDemandIdList": demand_id if len(demand_id) else None}
        result.append(cur)
    return result
