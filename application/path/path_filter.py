# -*- coding: utf-8 -*-
import sys

import feature.feature_handler as feature_handler
import path.path_format as path_format
import path.path_filter as path_filter
import path.path_calc as path_calc
import path.path_damage as path_damage

def filter_substandard_vlinks(vlink_qos_data, qos_demand) :
    fqos_demand = {qos_name : qos_value for qos_name, qos_value in qos_demand.items() \
                  if qos_name in ['rta', 'packet_loss', 'bandwidth']}
    qos_data = path_filter.multi_indicator_filter(vlink_qos_data, fqos_demand)
    vlink_list = feature_handler.select_vpaths_from_feature_data(qos_data)
    return vlink_list

def filter_substandard_vpaths(vpath_qos_data, qos_demand) :
    qos_data = path_filter.multi_indicator_filter(vpath_qos_data, qos_demand)
    vpath_list = feature_handler.select_vpaths_from_feature_data(qos_data)
    return vpath_list

def filter_substandard_vpath_groups(vpath_list, path_count, max_damage) :
    group_vpath_list = path_calc.build_gpath_list(vpath_list, path_count)
    path_damage.gpath_list_damage_filter(group_vpath_list, max_damage)
    return group_vpath_list