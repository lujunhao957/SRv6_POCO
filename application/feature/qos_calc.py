# -*- coding: utf-8 -*-
import sys

import pandas as pd
import feature.qos.qos_calc

def calculate_all_vlinks_qos(vlink_feature_data, qos_deviation, ping_packet_size = 64) :
    qos_data = feature.qos.qos_calc.multi_vpath_qos_cal(vlink_feature_data, qos_deviation, ping_packet_size)
    return qos_data


def calculate_all_vpaths_qos(vpath_feature_data, qos_deviation, ping_packet_size = 64) :
    qos_data = feature.qos.qos_calc.multi_vpath_qos_cal(vpath_feature_data, qos_deviation, ping_packet_size)
    return qos_data