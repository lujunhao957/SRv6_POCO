# -*- coding: utf-8 -*-
import importlib
import pandas as pd

import constant
import database.db_loader as db_loader
import topology.topology_handler as topology_handler
import feature.instab.offline_instab_init as offline_instab_init

import application.data.statement.instab_sql as instab_sql
import application.data.mdata_loader as app_data_loader

def is_instab_table_vaild(pocomputing_conn, tablename) :
    tablename = str(tablename)
    if app_data_loader.is_table_exist(tablename, pocomputing_conn) :
        return True
    return False

def get_allzero_vlink_offline_instab_data(topo_graph) :
    vlink_list = topology_handler.get_edges_from_topo_graph(poco_overlay_topo_graph)
    vlink_offline_instab_data = offline_instab_init.init_offline_instab_data(vlink_list, instab_model)
    return vlink_offline_instab_data

def get_vlink_offline_instab_data(pocomputing_conn, tablename) :
    tablename = str(tablename)
    if not app_data_loader.is_table_exist(tablename, pocomputing_conn) :
        return pd.DataFrame()
    sql_str = instab_sql.pd_vlink_offline_instab_stmt(tablename)
    pd_instab_topo_data = db_loader.read_pddata_by_sql(sql_str, pocomputing_conn)
    pd_instab_topo_data.index.name = 'index'
    pd_instab_topo_data.set_index(['source_name', 'des_name'], inplace = True)
    if 'id' in pd_instab_topo_data.columns :
        pd_instab_topo_data.drop('id', axis = 1, inplace = True)
    if 'index' in pd_instab_topo_data.columns :
        pd_instab_topo_data.drop('id', axis = 1, inplace = True)
    return pd_instab_topo_data