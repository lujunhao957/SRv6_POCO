# -*- coding: utf-8 -*-
import importlib
import pandas as pd

import database.db_loader as db_loader
import utils.datetime_utils as datetime_utils

import application.data.statement.filter_topo_sql as filter_topo_sql
import application.data.mdata_loader as app_data_loader

################################################################################
#本程序的作用：为程序初始化配置项，调用相应函数实现
#    1. 需要额外防止污染主程序的命名空间
#    2. 整个程序额外包装API，更加便于更换实现，降低与其他模块的耦合
#        比方说，需要增加新功能，而便于改动其他模块/或者直接实现新模块
#        每个函数保证相应的功能正常即可，甚至不关心实现形式与数据结构
#    3.控制整个程序调用，且易于测试，方便直接调试

################################################################################
#以下函数完成的功能为，POCO以及监控平台的拓扑数据读取，以及向标准数据结构的转换
#强业务相关函数，不关心细节实现

################################################################################
#网络拓扑数据的读取

def get_pocomputing_host_data(pocomputing_conn) :
    pd_poco_host_data = app_data_loader.load_pd_poco_host_data(pocomputing_conn)
    return pd_poco_host_data

def get_pocomputing_topo_data(pocomputing_conn) :
    pd_poco_topo_data = app_data_loader.load_pd_poco_topo_data(pocomputing_conn)
    return pd_poco_topo_data

def get_vlink_filter_topo_data(pocomputing_conn, tablename) :
    tablename = str(tablename)
    if not app_data_loader.is_table_exist(tablename, pocomputing_conn) :
        return pd.DataFrame()
    sql_str = filter_topo_sql.pd_vlink_filter_topology_stmt(tablename)
    pd_filter_topo_data = db_loader.read_pddata_by_sql(sql_str, pocomputing_conn)
    if pd_filter_topo_data.empty :
        print ("basic_database : load from basic database fail")
        return pd.DataFrame()
    pd_filter_topo_data.reset_index(inplace = True)
    if 'index' in pd_filter_topo_data.columns :
        pd_filter_topo_data.drop('index', inplace=True, axis=1)
    return pd_filter_topo_data