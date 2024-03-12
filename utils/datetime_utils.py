# -*- coding: utf-8 -*-
import time
import datetime
import pandas as pd
import numpy as np

################################################################################
#此py设计目的为，防止程序调用原生库而遇到不可预料的后果
#本模块涉及几种数据类型，这里均使用名称区分
#    timestamp：时间戳，类型为int，例如1546866444
#    dt：日期，类型为datetime.datetime，例如 2019-01-07 21:07:24.000000
#    dt_str：日期，即将datetime.datetime强制转换为str类型，例如字符串'2019-01-07 21:07:24.000000'
#    day_str；即最小单位为天的日期，类型为str，例如字符串'20190107'
#    pandas_timestamp：时间戳，即pandas函数库所支持的时间戳

#获取当前时间戳，仅取时间戳整数部分
#return：返回当前时间戳，类型为整形(int)
def timestamp_now() :
    timestamp = int(time.time()) #- 20 * SECONDS_PER_DAY
    return timestamp

#将类型dt转换为dt_str类型
#    dt：日期
#    fmt：日期格式类型
#return：dt_str类型数据
def datetime_to_str(dt, fmt = '%Y-%m-%d %H:%M:%S.%f%z') :
    dt_str = datetime.datetime.strftime(dt, '%Y-%m-%d %H:%M:%S.%f%z')
    return dt_str

#将类型dt_str转换为timestamp类型
#    dt_str：日期字符串
#    fmt：日期格式类型
#return：dt_str类型数据
def datetime_to_timestamp(dt_str, fmt = '%Y-%m-%d %H:%M:%S') :
    #去掉毫秒时间戳，将dt_str转义为date
    dt_str = str(dt_str).split('.')[0]
    return int(time.mktime(datetime.datetime.strptime(str(dt_str), fmt).timetuple()))

#将类型timestamp转换为dt类型
#    timestamp：时间戳
#return：dt类型数据
def timestamp_to_datetime(timestamp) :
    dt = datetime.datetime.fromtimestamp(int(timestamp))
    return dt

#将类型timestamp转换为pandas_timestamp类型
#引入时区的目的，在于规避pandas自身配置时区默认为0区的问题
#    timestamp：时间戳
#return：pandas_timestamp类型数据
def pd_timestamp(timestamp, time_zone) :
    pandas_timestamp = pd.Timestamp(timestamp, unit = 's') + pd.Timedelta(hours = time_zone)
    return pandas_timestamp

#将类型dt转换为day_str类型，即提取年月日字符串
#    dt：日期
#    fmt：日期格式类型
#return：dt_str类型数据
def datetime_to_daystr(dt, fmt = '%Y%m%d') :
    datetime_str = datetime.datetime.strftime(dt, fmt)
    return datetime_str

#将类型day_str转换为timestamp类型，即提取年月日字符串
#    day_str：年月日日期字符串
#    fmt：日期格式类型
#return：timestamp类型数据
def daystr_to_timestamp(day_str, fmt = '%Y%m%d') :
    timestamp = datetime_to_timestamp(datetime.datetime.strptime(day_str, fmt))
    return timestamp