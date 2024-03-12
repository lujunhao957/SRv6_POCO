# -*- coding: utf-8 -*-
import sys
import json
import time

import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

#为模块引入全局常量


#将pd.DataFrame()类型数据，写入相应的数据库表中
#    data：数据集，类型为pd.DataFrame()
#    tablename：即数据库中表名
#    conn：数据库句柄，由db_conn.get_data_conn_orm函数得到
#    if_exists：数据表存在的策略，'replace'代表替换，'append'代表追加，'fail'代表无操作
def import_pddata_to_db(data, tablename, conn, if_exists = 'replace') :
    i = 1
    while i <= 5 :
        try :
            pd.io.sql.to_sql(data, str(tablename), con = conn, if_exists = if_exists)
            return True
        except :
            i = i + 1
            print ('import data to database fail')
    return False