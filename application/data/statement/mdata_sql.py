# -*- coding: utf-8 -*-
import sys

################################################################################
#基于现有Pocomputing数据库表，读取相应的基础数据

#生成读取Pocomputing数据库中，所有节点信息的语句
#return：相应SQL语句
def pd_poco_host_data_stmt() :
    sql_stmt = "select * from node_info"
    return sql_stmt

#生成读取Pocomputing数据库中，整张网络拓扑信息的SQL语句
#return：相应SQL语句
def pd_poco_topo_data_stmt() :
    sql_stmt = "select * from neighbor_info"
    return sql_stmt

def is_empty_table_stmt(tablename) :
    sql_str = "select table_name from information_schema.TABLES where table_name = " + \
           "'{}'".format(str(tablename))
    return sql_str
