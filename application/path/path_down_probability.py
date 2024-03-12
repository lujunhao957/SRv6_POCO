# -*- coding: utf-8 -*-
import path.path_down_probability as path_down_probability


# 单条虚拟专线中断的概率
def single_path_down_probability(link_down_data, path):
    return path_down_probability.single_path_down_probability(link_down_data, path)


# 一组虚拟专线中断的概率
def path_group_down_probability(link_down_data, path_link_map, path_group):
    return path_down_probability.path_group_down_probability(link_down_data, path_link_map, path_group)


# 所有虚拟专线同时中断的概率
# def all_path_down_probability(link_down_data, all_paths, path_link_map, target):
    # return path_down_probability.all_path_down_probability(link_down_data, all_paths, path_link_map, target)
def all_path_down_probability(all_paths, paths_data, demand):
    return path_down_probability.all_path_down_probability(all_paths, paths_data, demand)
