# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


_DEFAULT_DEVIATION = 1.0

path_qos_map={}

def get_qos_parameter(path):
    if path in path_qos_map:
        return path_qos_map[path]
    else:
        multi_vpath_qos_cal()
    return True


def multi_vpath_qos_cal(basic_feature_data) :
    qos_data_list = []
    _qos_list = ['rta', 'packet_loss', 'jitter']
    for qos_type in _qos_list :
        if qos_type == 'rta' :
            qos_data_list.append(multi_vpath_rta_cal(basic_feature_data))
        elif qos_type == 'packet_loss' :
            qos_data_list.append(multi_vpath_packet_loss_cal(basic_feature_data))
        elif qos_type == 'jitter' :
            qos_data_list.append(multi_vpath_jitter_cal(basic_feature_data))
    qos_data = pd.concat(qos_data_list, axis = 1)
    qos_data.dropna(inplace = True)
    return qos_data

def multi_vpath_rta_cal(basic_feature_data, packet_size, deviation) :
    if not packet_size == 64 and not packet_size == 1024 :
        return pd.DataFrame()
    if not type(deviation) is int and not type(deviation) is float:
        return pd.DataFrame()
    if deviation < 0 :    deviation = 0.0
    elif deviation > 1 :    deviation = 1.0
    qos_dict = {}
    if deviation <= 1e-3 :
        #问题的关键之一：变量名有时候是列名，也就意味着引入字符串，代码可读性下降(没办法的事情，先蒙老师)
        if 'latest_rta_' + str(packet_size) in basic_feature_data.columns :
            qos_dict.update({'rta' : basic_feature_data['latest_rta_' + str(packet_size)]})
        return pd.DataFrame(qos_dict)
    elif deviation >= 1.0 - 1e-3 :
        if 'mean_rta_' + str(packet_size) in basic_feature_data.columns :
            qos_dict.update({'rta' : basic_feature_data['mean_rta_' + str(packet_size)]})
    else :
        if 'latest_rta_' + str(packet_size) in basic_feature_data.columns and \
            'mean_rta_' + str(packet_size) in basic_feature_data.columns :
            qos_dict.update({'rta' : (1.0 - deviation) * basic_feature_data['mean_rta_' + str(packet_size)] + \
                        1.0 * deviation * basic_feature_data['latest_rta_' + str(packet_size)]})
    if not qos_dict :    
        empty_data = pd.DataFrame({'vitrual_path':[], 'rta':[]})
        empty_data.set_index('vitrual_path', inplace=True)
        return empty_data
    else :    
        return pd.DataFrame(qos_dict)
    
def multi_vpath_packet_loss_cal(basic_feature_data, packet_size, deviation) :

    if deviation < 0 :    deviation = 0.0
    elif deviation > 1 :    deviation = 1.0
    qos_dict = {}
    if deviation <= 1e-3 :
        if 'latest_packet_loss_' + str(packet_size) in basic_feature_data.columns :
            qos_dict.update({'packet_loss' : basic_feature_data['latest_packet_loss_' + str(packet_size)]})
        return pd.DataFrame(qos_dict)
    elif deviation >= 1.0 - 1e-3 :
        if 'mean_packet_loss_' + str(packet_size) in basic_feature_data.columns :
            qos_dict.update({'packet_loss' : basic_feature_data['mean_packet_loss_' + str(packet_size)]})
    else :
        if 'latest_packet_loss_' + str(packet_size) in basic_feature_data.columns and \
            'mean_packet_loss_' + str(packet_size) in basic_feature_data.columns :
            qos_dict.update({'packet_loss' : (1.0 - deviation) * basic_feature_data['mean_packet_loss_' + str(packet_size)] + \
                        1.0 * deviation * basic_feature_data['latest_packet_loss_' + str(packet_size)]})
    if not qos_dict :    
        empty_data = pd.DataFrame({'vitrual_path':[], 'packet_loss':[]})
        empty_data.set_index('vitrual_path', inplace=True)
        return empty_data
    else :
        return pd.DataFrame(qos_dict)
    
def multi_vpath_jitter_cal(basic_feature_data, packet_size, deviation) :
    if not packet_size == 64 and not packet_size == 1024 :
        return pd.DataFrame()
    if not type(deviation) is int and not type(deviation) is float:
        return pd.DataFrame()
    if deviation < 0 :    deviation = 0.0
    elif deviation > 1 :    deviation = 1.0
    qos_dict = {}
    if deviation <= 1e-3 :
        if 'latest_jitter_' + str(packet_size) in basic_feature_data.columns :
            qos_dict.update({'jitter' : basic_feature_data['latest_jitter_' + str(packet_size)]})
        return pd.DataFrame(qos_dict)
    elif deviation >= 1.0 - 1e-3 :
        if 'mean_jitter_' + str(packet_size) in basic_feature_data.columns :
            qos_dict.update({'jitter' : basic_feature_data['mean_jitter_' + str(packet_size)]})
    else :
        if 'latest_jitter_' + str(packet_size) in basic_feature_data.columns and \
            'mean_jitter_' + str(packet_size) in basic_feature_data.columns :
            qos_dict.update({'jitter' : (1.0 - deviation) * basic_feature_data['mean_jitter_' + str(packet_size)] + \
                        1.0 * deviation * basic_feature_data['latest_jitter_' + str(packet_size)]})
    if not qos_dict :    
        empty_data = pd.DataFrame({'vitrual_path':[], 'jitter':[]})
        empty_data.set_index('vitrual_path', inplace=True)
        return empty_data
    else :   
        return pd.DataFrame(qos_dict)
