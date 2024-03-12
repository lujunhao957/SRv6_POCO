# -*- coding: utf-8 -*-
import sys

import database.db_conn as database_connecter

from constant import DB_MAX_RERTY_COUNT

def get_data_conn_with_retry(db_conf) :
    conn = database_connecter.get_data_conn_with_retry(db_conf, DB_MAX_RERTY_COUNT)
    return conn
    
def database_conn_close(conn) :
    try :
        if conn :
            database_connecter.connection_close(conn)
        return True
    except :
        return False