# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

################################################################################
#提供一些基本的数据处理函数

#计算pandas.Series中，value值对应的分位点位置
#    data：一列数据，类型为pd.Series
#    value：数据取值
#return：dt_str类型数据
def value_to_percentile(data, value) :
    if data.empty or data.isnull().sum() == data.shape[0]:
        return 1.0
    if value > data.max() :
        return 1.0
    elif value < data.min() :
        return 0.0
    #pandas库计入空值
    vleft = data[data <= value].max()
    vleft_c = data[data <= value].count()
    total_c = data.count()
    
    pr = 0.0
    if abs(vleft - value) <= 1e-3 :
        if total_c == 1 :
            pr = 0.5
        else :
            pr = 1.0 * (vleft_c - 1) / (total_c - 1)
    else :
        vright = data[data >= value].min()
        pr = 1.0 * (vleft_c - 1) / (total_c - 1) + 1.0 * (value - vleft) / (1.0 * (vright - vleft) * (total_c - 1))
    pr = pr
    return pr