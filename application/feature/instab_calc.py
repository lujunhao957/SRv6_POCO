# -*- coding: utf-8 -*-
import os
import sys
import json
import pandas as pd

import path.path_format
import path.path_calc

import feature.instab.model_loader
import feature.instab.fakedata_gen
import feature.instab.online_instab_calc
import feature.instab.offline_instab_calc
import feature.instab.instab_calc

_DEFAULT_SUFFIX_STR = '.json'

def load_all_instab_model(instab_dir) :
    instab_dir = str(instab_dir)
    fname_list = os.listdir(instab_dir)
    instab_service_model_map = {}
    for filename in fname_list :
        if filename.endswith(_DEFAULT_SUFFIX_STR) :
            filename = os.path.join(instab_dir, filename)
            instab_model = feature.instab.model_loader.load_instab_model(filename)
            if instab_model :
                service_type = feature.instab.model_loader.get_instab_service_type(instab_model)
                instab_service_model_map[service_type] = instab_model
    return instab_service_model_map

def is_instab_model_supported(instab_service_model_map, service_type) :
    if not type(instab_service_model_map) is dict :
        return False
    if service_type in instab_service_model_map :
        return True
    return False

def get_instab_model(instab_service_model_map, service_type) :
    instab_model = instab_service_model_map[service_type]
    return instab_model

def load_vlink_offline_instab_data(topo_graph) :
    offline_instab_data = feature.instab.fakedata_gen.fake_offline_instab_gene(topo_graph)
    return offline_instab_data

def calculate_all_vpaths_online_instab_basic(vpath_feature_data, instab_model) :
    online_instab = feature.instab.online_instab_calc.online_instability_cal(vpath_feature_data, instab_model)
    return online_instab

def calculate_all_vpath_offline_instab_basic(vlink_offline_instab_data, vpath_list, instab_model) :
    offline_instab = feature.instab.offline_instab_calc.offline_instability_cal(vlink_offline_instab_data, vpath_list, instab_model)
    return offline_instab

def calculate_all_vpaths_online_instab_nest(vpath_feature_data, instab_model) :
    online_instab = feature.instab.online_instab_calc.online_instability_cal(vpath_feature_data, instab_model)
    return online_instab

def calculate_all_vpaths_offline_instab_nest(vlink_offline_instab_data, vpath_list, real_path_map, instab_model) :
    real_vpath_list = [path.path_calc.elim_nest_path(vpath, real_path_map) for vpath in vpath_list]
    real_origin_vpath_map = {
        path.path_format.format_path(real_path) : path.path_format.format_path(nest_path)
        for real_path, nest_path in zip(real_vpath_list, vpath_list)
    }
    offline_instab = feature.instab.offline_instab_calc.offline_instability_cal(vlink_offline_instab_data, real_vpath_list, instab_model)
    new_offline_instab = [
        {'virtual_path' : nest_vpath_str, 'offline_stability' : offline_instab[real_vpath_str]}
        for real_vpath_str, nest_vpath_str in real_origin_vpath_map.items()
    ]
    new_offline_instab = pd.DataFrame(new_offline_instab)
    new_offline_instab.set_index('virtual_path', inplace = True)
    offline_instab_data = new_offline_instab['offline_stability']
    return offline_instab_data

def calculate_all_vpaths_instab_data(vpath_online_instab_data, vpath_offline_instab_data, instab_model) :
    instab_data = feature.instab.instab_calc.vpaths_instability_cal(vpath_online_instab_data, vpath_offline_instab_data, instab_model)
    return instab_data

def set_instability_data(vpath_indicator_data, vpath_instab_data) :
    vpath_instab_data.name = 'instability'
    vpath_instab_data = pd.DataFrame(vpath_instab_data)
    vpath_indicator_data = pd.merge(vpath_indicator_data, vpath_instab_data, how = 'left', left_index = True, right_index = True)
    #vpath_indicator_data['instability'] = vpath_instab_data
    #vpath_indicator_data['instability'] = 1.0
    return vpath_indicator_data