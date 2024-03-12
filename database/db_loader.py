# -*- coding: utf-8 -*-
import sys
import json
import time

import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


################################################################################
#将数据读取为pandas DataFrame格式

#基于数据库SQL语句与连接句柄，读取数据库
#    sql_stmt：SQL字符串
#    conn：数据库读取句柄，由conn.get_data_conn得到
#return：返回读取到的数据，格式为DataFrame；若失败则返回空数据
def read_pddata_by_sql(sql_stmt, conn) :
    i = 1
    data = pd.DataFrame()
    while i <= 5 :
        try:
            data = pd.io.sql.read_sql(sql_stmt, conn)
        except :
            i = i + 1
            print ('[database] read from database error')
            continue
        break
    return data