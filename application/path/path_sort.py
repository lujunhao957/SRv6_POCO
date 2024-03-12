# -*- coding: utf-8 -*-
import sys
import feature.feature_handler
import path.path_calc as path_calc
import path.path_sort as path_sort
import path.path_damage as path_damage

import application.path.path_filter as path_filter

_INIT_VPATH_COUNT = 20

def calculate_optimal_vpaths_damage(vpath_indicator_data, vpath_list, sort_by, path_count, ascending, max_damage) :
    if vpath_indicator_data.empty or not type(vpath_list) is list :
        return []
    if len(vpath_list) == 0 or not sort_by in vpath_indicator_data.columns :
        return []
    vpath_indicator_data = feature.feature_handler.select_feature_data_by_vlink(vpath_indicator_data, vpath_list)
    vpath_indicator_data = feature.feature_handler.sort_feature_data_by_key(vpath_indicator_data, sort_by, ascending)
    topk_list = range(_INIT_VPATH_COUNT, len(vpath_list), max(len(vpath_list) / 5, 1))
    topk_list.append(len(vpath_list))
    for topk in topk_list :
        tvpath_indicator_data = feature.feature_handler.select_feature_data_by_topk(vpath_indicator_data, topk)
        tvpath_list = feature.feature_handler.select_vpaths_from_feature_data(tvpath_indicator_data)
        group_vpath_list = path_filter.filter_substandard_vpath_groups(tvpath_list, path_count, max_damage)
        final_vpath_list = path_sort.gpath_list_sort(group_vpath_list, sort_by, vpath_indicator_data,\
                     ascending = ascending)
        if len(final_vpath_list) == path_count :
            return final_vpath_list
        if topk == len(vpath_list) and len(final_vpath_list) == 0 :
            group_vpath_list = path_calc.build_gpath_list(vpath_list, path_count)
            group_vpath_list = path_damage.gpath_list_min_damage_path_cal(group_vpath_list)
            final_vpath_list = path_sort.gpath_list_sort(group_vpath_list, sort_by, vpath_indicator_data,\
                         ascending = ascending)
            return final_vpath_list
    return []

def calculate_optimal_vpaths_basic(vpath_indicator_data, vpath_list, sort_by, path_count, ascending) :
    vpath_indicator_data = feature.feature_handler.select_feature_data_by_vlink(vpath_indicator_data, vpath_list)
    final_path_list = path_sort.path_list_sort(vpath_indicator_data, sort_by, ascending = ascending)
    final_path_list = path_sort.get_optimal_path_list(final_path_list, path_count)
    return final_path_list


def webrtc_quality_gpath_list_sort():
    return None