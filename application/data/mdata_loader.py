# -*- coding: utf-8 -*-
import gc
import os
import sys
import copy
import json
import time
import datetime
import numpy as np
import pandas as pd

#程序的环境变量，子目录测试用
#sys.path.append("..")
#sys.path.append("../..")


#引入SQL构建功能
import database.db_loader as db_loader
import application.data.statement.mdata_sql as sql_stmt

################################################################################
#读取Pocomputing数据库中关键数据

#判断对应表名在数据库中是否存在
#    tablename：需要判断的数据库表名
#return：若为True，则数据库表存在，否则数据库表不存在
def is_table_exist(tablename, conn) :
    data = db_loader.read_pddata_by_sql(sql_stmt.is_empty_table_stmt(str(tablename)), conn)
    if data.empty :
        return False
    return True

#读取Pocomputing数据库中，所有节点信息数据
#return：相应的pandas.DataFrame()数据，对应topology模块中，pd_poco_host_data格式
#DataFrame中列名包括：
#node_id：即pocomputing中节点的ID，类型为int。例如：12
#node_name：即pocomputing中节点的名称，类型为str。例如：Digital_Ocean_Amsterdam
#latitude：即节点所在的纬度(float)
#longitude：即节点所在的经度(float)
#poco_id：即在POCO中的ID信息，用于将求解POCO不同ID之间的路径问题，以Pocomputing
#    内部ID的形式进行，以对整个系统解耦
#timestamp：即更新时间戳
def load_pd_poco_host_data(conn) :
    sql_str = sql_stmt.pd_poco_host_data_stmt()
    pd_poco_host_data = db_loader.read_pddata_by_sql(sql_str, conn)
    if pd_poco_host_data.empty :
        print ("basic_database : load from basic database fail")
        return pd.DataFrame()
    return pd_poco_host_data

#读取Pocomputing数据库中，整张网络拓扑信息数据
#return：相应的pandas.DataFrame()数据，对应topology模块中，pd_poco_topo_data格式
#DataFrame中列名包括：
#node_id：即pocomputing中节点的ID，类型为int。例如：12
#node_name：即pocomputing中节点的名称，类型为str。例如：Digital_Ocean_Amsterdam
#neighbor_id：即pocomputing中当前节点的邻居ID，类型为str，以'|'分割。例如：
#    13|14|15|16|17|18|23|45|46
#neighbor_name，即neighbor_id中ID全部按顺序转换为name。类型为str，以'|'分割。例如：
#    Digital_Ocean_Frankfurt|Digital_Ocean_London|...|Tietong_156-ovs
#timestamp：即更新时间戳
def load_pd_poco_topo_data(conn) :
    sql_str = sql_stmt.pd_poco_topo_data_stmt()
    pd_poco_topo_data = db_loader.read_pddata_by_sql(sql_str, conn)
    if pd_poco_topo_data.empty :
        print ("basic_database : load from basic database fail")
        return pd.DataFrame()
    pd_poco_topo_data.reset_index(inplace = True)
    if 'index' in pd_poco_topo_data.columns :
        pd_poco_topo_data.drop('index', inplace=True, axis=1)
    return pd_poco_topo_data