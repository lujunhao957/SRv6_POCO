# -*- coding: utf-8 -*-
import os
import sys
import json

import feature.qoe.model_loader
import feature.qoe.qoe_calc

_DEFAULT_SUFFIX_STR = '.json'

def load_all_qoe_model(qoe_dir) :
    qoe_dir = str(qoe_dir)
    fname_list = os.listdir(qoe_dir)
    qoe_service_model_map = {}
    for filename in fname_list :
        if filename.endswith(_DEFAULT_SUFFIX_STR) :
            filename = os.path.join(qoe_dir, filename)
            qoe_model = feature.qoe.model_loader.load_qoe_model(filename)
            if qoe_model :
                service_type = feature.qoe.model_loader.get_qoe_service_type(qoe_model)
                qoe_service_model_map[service_type] = qoe_model
    return qoe_service_model_map

def is_qoe_model_supported(qoe_service_model_map, service_type) :
    if not type(qoe_service_model_map) is dict :
        return False
    if service_type in qoe_service_model_map :
        return True
    return False

def get_qoe_model(qoe_service_model_map, service_type) :
    qoe_model = qoe_service_model_map[service_type]
    return qoe_model

def calculate_all_vpaths_qoe(vpath_qos_data, qoe_model, qoe_indicator_name = '') :
    vpath_indicator_data = feature.qoe.qoe_calc.qoe_indicator_cal(vpath_qos_data.copy(), qoe_model)
    qoe_model_indicator_name = feature.qoe.model_loader.get_qoe_indicator_name(qoe_model)
    if qoe_indicator_name :
        if qoe_model_indicator_name in vpath_indicator_data.columns :
            vpath_indicator_data[qoe_indicator_name] = vpath_indicator_data[qoe_model_indicator_name]
    return vpath_indicator_data