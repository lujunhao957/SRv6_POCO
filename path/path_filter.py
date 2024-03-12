# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd

_indicator_nlist = ['rta', 'packet_loss', 'jitter', 'bandwidth']
_instruction_nlist = ['min', 'max']

def one_indicator_filter(feature_data, indicator_name, indicator_filter_cond) :
    if indicator_name not in feature_data.columns and not indicator_name in _indicator_nlist:
        return feature_data
    if not type(indicator_filter_cond) is dict :
        return feature_data
    for instru in indicator_filter_cond.keys() :
        if not instru in _instruction_nlist :
            continue
        if not type(indicator_filter_cond[instru]) is int and not type(indicator_filter_cond[instru]) is float :
            continue
        threhold = indicator_filter_cond[instru]
        if instru == 'max' :
            feature_data = feature_data[feature_data[indicator_name] <= threhold]
        elif instru == 'min' :
            feature_data = feature_data[feature_data[indicator_name] >= threhold]
        else :
            continue
    return feature_data

def multi_indicator_filter(feature_data, filter_demand) :
    if not type(filter_demand) is dict :
        return feature_data
    for indicator_name in filter_demand.keys() :
        indicator_filter_cond = filter_demand[indicator_name]
        feature_data = one_indicator_filter(feature_data, indicator_name, indicator_filter_cond)
    return feature_data