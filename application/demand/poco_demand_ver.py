# -*- coding: utf-8 -*-
import json

from numpy import unicode

_POCO_DEMAND_TYPE_LIST = ['backbone', 'user']
_POCO_DEMAND_QOS_LIST = ['rta', 'packetLoss', 'jitter', 'bandwidth']
_BOOLEAN_SET = set(['true', 'false', 'True', 'False'])


def is_poco_demand_vaild(poco_demand):
    if not type(poco_demand) is dict:    return False
    necessary_key = set(['demandInfo'])
    if necessary_key - set(poco_demand.keys()):    return False

    # 检查demandInfo字段
    demand_info = poco_demand['demandInfo']
    if not type(demand_info) is dict:    return False
    necessary_key = set(['source_node', 'dest_node', 'webrtc_quality', 'path_count','max_hop','max_damage'])
    if necessary_key - set(demand_info.keys()):    return False
    source_id = demand_info['source_node']
    des_id = demand_info['dest_node']
    if not (is_int(source_id) and is_int(des_id)):    return False
    webrtc_quality = demand_info['webrtc_quality']
    if is_webrtc_quality_vaild(webrtc_quality)!=True:
        return False
    if 'path_count' in demand_info:
        pathCount = demand_info['path_count']
        if not is_int(pathCount):    return False
    if 'max_hop' in demand_info:
        maxHop = demand_info['max_hop']
        if not is_int(maxHop):    return False
    if 'max_damage' in demand_info:
        maxDamage = demand_info['max_damage']
    return True

def is_webrtc_quality_vaild(webrtc_quality):
    necessary_key = set(['resolution', 'fps', 'buffer_duration', 'buffer_duration_probability', 'continuous_playback_duration', 'continuous_playback_duration_probability'])
    if necessary_key - set(webrtc_quality.keys()):    return False
    return True

def is_vpath_vaild(vpath_str):
    if not (type(vpath_str) is str or type(vpath_str) is unicode):
        return False
    vpath_str_list = vpath_str.split('-')
    if len(vpath_str_list) < 2:
        return False
    true_count = sum([is_int(node) for node in vpath_str_list])
    is_vaild = (true_count == len(vpath_str_list))
    return is_vaild


def is_vlink_vaild(vlink_str):
    if not (type(vlink_str) is str or type(vlink_str) is unicode):
        return False
    vlink_str_list = vlink_str.split('-')
    if not len(vlink_str_list) == 2:
        return False
    is_vaild = (is_int(vlink_str_list[0]) and is_int(vlink_str_list[1]))
    return is_vaild


def is_percentile_vaild(percentile):
    if not len(percentile) == 4:
        return False
    true_count = sum([is_float(num) for num in percentile])
    is_vaild = (true_count == 4)
    return is_vaild


def is_int(s):
    s = str(s)
    if s.isdigit():
        return True
    return False


def is_bool(s):
    s = str(s)
    if s in _BOOLEAN_SET:
        return True
    return False


def is_float(s):
    s = str(s)
    if s.count('.') == 0:
        if s.isdigit():
            return True
        else:
            return False
    elif s.count('.') == 1:  # 判断小数点个数
        sl = s.split('.')  # 按照小数点进行分割
        left = sl[0]  # 小数点前面的
        right = sl[1]  # 小数点后面的
        if left.startswith('-') and left.count('-') == 1 and right.isdigit():
            lleft = left.split('-')[1]  # 按照-分割，然后取负号后面的数字
            if lleft.isdigit():
                return True
        elif left.isdigit() and right.isdigit():
            # 判断是否为正小数
            return True
    return False


def is_str(s):
    if type(s) is str or type(s) is unicode:
        return True
    return False
