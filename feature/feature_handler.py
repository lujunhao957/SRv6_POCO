# -*- coding: utf-8 -*-
import pandas as pd
import path.path_format

def select_vpaths_from_feature_data(feature_data) :
    if feature_data.empty :
        return []
    vpath_list = path.path_format.split_path_list(list(feature_data.index))
    return vpath_list

def select_feature_data_by_vlink(feature_data, vpath_list) :
    if feature_data.empty :
        return pd.DataFrame()
    fvpath_list = path.path_format.format_path_list(vpath_list)
    feature_data = feature_data.loc[fvpath_list]
    return feature_data

def select_feature_data_by_topk(feature_data, topk) :
    if type(topk) == int :
        feature_data = feature_data.head(topk)
        return feature_data
    return pd.DataFrame()

def sort_feature_data_by_key(feature_data, sort_by, ascending = False) :
    if sort_by in feature_data.columns :
        feature_data = feature_data.sort_values(sort_by, ascending = not ascending)
        return feature_data
    return pd.DataFrame()