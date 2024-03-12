# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

def np_null_ratio_cal(qos_data) :
    if not type(qos_data) == np.ndarray :
        return 1.0
    qos_data = qos_data.copy()
    qos_null_count = qos_data[np.isnan(qos_data)].shape[0]
    qos_count = qos_data.shape[0]
    qos_count = qos_count if not qos_count == 0 else 1
    qos_null_ratio = float(qos_null_count) / qos_count
    return qos_null_ratio

def np_mean(qos_data) :
    if not type(qos_data) == np.ndarray:
        return None
    mean_value = float(np.nanmean(qos_data))
    return mean_value

def np_median(qos_data) :
    if not type(qos_data) == np.ndarray:
        return None
    median_value = float(np.nanmedian(qos_data))
    return median_value

def np_mean_by_fillna(qos_data, fill_value) :
    if not type(qos_data) == np.ndarray :
        return 1.0
    qos_data = qos_data.copy()
    qos_data[np.isnan(qos_data)] = fill_value
    mean_value = float(np.nanmean(qos_data))
    return mean_value

def np_percentile(qos_data, p = 0.5) :
    if not type(qos_data) == np.ndarray :
        return None
    percentile_value = np.nanpercentile(qos_data, 100.0 * p)
    return float(percentile_value)

def np_last_notnull(qos_data, redunt = 5) :
    if not type(qos_data) == np.ndarray :
        return None  
    qos_count = qos_data.shape[0]
    if qos_count <= 0 :
        return None
    else :
        qos_data = qos_data[-1 * min([qos_count, redunt]):]
        qos_data = qos_data[~np.isnan(qos_data)]
        if qos_data.shape[0] == 0 :
            return None
        return float(qos_data[-1])