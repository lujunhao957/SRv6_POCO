# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import numeral_calc

def vpath_ping_feature_cal(path_data, packet_size, probe_cycle, stats_cycle, percentile) :
    ping_vpath_info = {}
    if path_data.empty or not type(percentile) is dict:
        return {}
    packet_size = str(packet_size)
    probe_method = 'ping' + packet_size
    if not probe_method in probe_cycle or not probe_method in stats_cycle:
        return {}
    probe_cycle = probe_cycle[probe_method]
    stats_cycle = stats_cycle[probe_method]
    if 'rta' in path_data.columns and not 'jitter' in path_data.columns :
        path_data['jitter'] = path_data['rta'].diff().abs()
    for qos_name in ['rta', 'jitter', 'packet_loss'] :
        if qos_name in path_data.columns :
            qos_stats_cycle = probe_cycle
            if qos_name in stats_cycle :
                qos_stats_cycle = stats_cycle[qos_name]
            elif qos_name == 'jitter' and 'rta' in stats_cycle :
                qos_stats_cycle = stats_cycle['rta']
            qos_data = path_data[qos_name].values
            qos_data_count = min(qos_data.shape[0], int(qos_stats_cycle / probe_cycle))
            qos_data = qos_data[-1 * qos_data_count:]
            #问题的关键之一：是否能将计算的特征参数化(还有就是加速的问题)
            ping_vpath_info['null_ratio_' + str(qos_name) + '_' + packet_size] = numeral_calc.np_null_ratio_cal(qos_data)
            if 'percentile4' in percentile.keys() :
                percentile4 = float(percentile['percentile4'])
                ping_vpath_info['percentile4_' + str(qos_name) + '_' + packet_size] = numeral_calc.np_percentile(qos_data, percentile4)
            ping_vpath_info['median_' + str(qos_name) + '_' + packet_size] = numeral_calc.np_median(qos_data)
            ping_vpath_info['mean_' + str(qos_name) + '_' + packet_size] = numeral_calc.np_mean(qos_data)
            ping_vpath_info['latest_' + str(qos_name) + '_' + packet_size] = numeral_calc.np_last_notnull(qos_data, 5)
    return ping_vpath_info

def vpath_ping64_feature_cal(path_data, probe_cycle, stats_cycle, percentile) :
    ping64_vpath_info = vpath_ping_feature_cal(path_data, 64, probe_cycle, stats_cycle, percentile)
    return ping64_vpath_info

def vpath_ping1024_feature_cal(path_data, probe_cycle, stats_cycle, percentile) :
    ping1024_vpath_info = vpath_ping_feature_cal(path_data, 1024, probe_cycle, stats_cycle, percentile)
    return ping1024_vpath_info

def vpath_bandwidth_feature_cal(path_data, probe_cycle) :
    bandwidth_vpath_info = {}
    if path_data.empty:
        return {}
    path_data_len = path_data.shape[0] + 1
    probe_method = 'bandwidth'
    probe_cycle = probe_cycle[probe_method]
    for qos_name in ['bandwidth'] :
        if qos_name == 'bandwidth' and 'bandwidth' in path_data.columns :
            qos_data = path_data[qos_name].values
            bandwidth_vpath_info['latest_bandwidth'] = numeral_calc.np_last_notnull(qos_data, 5)
    return bandwidth_vpath_info

#data_dict = {'ping64' : pd.DataFrame(), 'ping1024' : pd.DataFrame(), 'bandwidth' : pd.DataFrame()}
def one_vpath_feature_cal(data_dict, probe_cycle, stats_cycle, percentile) :
    path_info = {}
    if not data_dict or not type(data_dict) is dict:
        return {}
    for probe_method in data_dict.keys() :
        if probe_method == 'ping64' :
            path_info.update(vpath_ping64_feature_cal(data_dict[probe_method], probe_cycle, stats_cycle, percentile))
        elif probe_method == 'ping1024' :
            path_info.update(vpath_ping1024_feature_cal(data_dict[probe_method], probe_cycle, stats_cycle, percentile))
        elif probe_method == 'bandwidth' :
            path_info.update(vpath_bandwidth_feature_cal(data_dict[probe_method], probe_cycle))
        else :
            continue
    return path_info