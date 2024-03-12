# -*- coding: utf-8 -*-
import sys

def pd_vlink_filter_topology_stmt(tablename) :
    sql_stmt = "select * from {}".format(str(tablename))
    return sql_stmt