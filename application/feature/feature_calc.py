# -*- coding: utf-8 -*-
import sys
import pandas as pd
import feature.basic.multi_path_calc

# def calculate_all_vlinks_feature(format_data_set_map, vlink_list, probe_cycle, stats_cycle, percentile) :
#     feature_data_list = []
#     for probe_method , sub_format_data_set in format_data_set_map.items() :
#         sub_feature_data = feature.basic.multi_path_calc.multi_vpath_feature_cal\
#                      (sub_format_data_set, vlink_list, probe_cycle, stats_cycle, percentile)
#         feature_data_list.append(sub_feature_data)
#     if feature_data_list :
#         vlink_feature_data = pd.concat(feature_data_list, axis = 1)
#         vlink_feature_data = feature.basic.multi_path_calc.verify_feature_data_completeness(\
#                       vlink_feature_data, 0.5)
#         return vlink_feature_data
#     else :
#         return pd.DataFrame()


def calculate_all_vlinks_feature(format_data_set_map, vlink_list, probe_cycle, stats_cycle, percentile) :
    vlink_feature_data = pd.DataFrame()
    for probe_method , sub_format_data_set in format_data_set_map.items() :
        sub_feature_data = feature.basic.multi_path_calc.multi_vpath_feature_cal\
                     (sub_format_data_set, vlink_list, probe_cycle, stats_cycle, percentile)
        vlink_feature_data = pd.concat([sub_feature_data, vlink_feature_data], axis=1)
    vlink_feature_data = feature.basic.multi_path_calc.verify_feature_data_completeness(\
                  vlink_feature_data, 0.5)
    return vlink_feature_data

def calculate_all_vpaths_feature(format_data_set_map, vpath_list, probe_cycle, stats_cycle, percentile) :
    feature_data_list = []
    for probe_method , sub_format_data_set in format_data_set_map.items() :
        sub_feature_data = feature.basic.multi_path_calc.multi_vpath_feature_cal\
                     (sub_format_data_set, vpath_list, probe_cycle, stats_cycle, percentile)
        feature_data_list.append(sub_feature_data)
    if feature_data_list :
        vpath_feature_data = pd.concat(feature_data_list, axis = 1)
        return vpath_feature_data
    else :
        return pd.DataFrame()