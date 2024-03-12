# -*- coding: utf-8 -*-
import sys
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


################################################################################
#基于数据库连接，SQL语句等信息，读取与写入相关数据
#注意不要混用(读取用作写入，写入用作读取)，否则会出现性能降低，且存在报错可能
#所以引入了两种数据库IO

#传入数据库连接信息，获取数据库读取句柄
#    dbconf：即数据库连接信息，结构为Dict
#    { 'ipaddr': 数据库IP地址,
#     'port': 数据库端口号,
#     'username': 数据库用户名,
#     'passwd': 数据库密码,
#     'database': 数据库名}
#return：构造生成的表名
def get_data_conn(db_conf) :
    conn = mysql.connector.connect(host = db_conf['ipaddr'], port = db_conf['port'], user = db_conf['username'], \
                           passwd = db_conf['passwd'], db = db_conf['database'])
    return conn

#传入数据库连接信息，获取数据库写入句柄
#    dbconf：即数据库连接信息，结构为Dict
#    { 'ipaddr': 数据库IP地址,
#     'port': 数据库端口号,
#     'username': 数据库用户名,
#     'passwd': 数据库密码,
#     'database': 数据库名}
#return：构造生成的表名
#BUG：关闭连接的问题，等待程序退出后自动关闭是一种做法，但是有没有更好的做法呢？
def get_data_conn_orm(db_conf):
    # conn = create_engine('mysql+mysqldb://' + db_conf['username'] + ':' + db_conf['passwd'] + '@' + db_conf['ipaddr']\
    #                      + ':' + str(db_conf['port']) + '/' + db_conf['database'] + '?charset=' , pool_pre_ping=True)
    cnx = mysql.connector.connect(user='root', password='203club',
                                  host='47.95.13.35', database='poco')
    return cnx

#连接至相应的数据库(用于读取Pandas数据)
#    dbconf：即数据库连接信息，结构为Dict
#        { 'ipaddr': 数据库IP地址,
#         'port': 数据库端口号,
#         'username': 数据库用户名,
#         'passwd': 数据库密码,
#         'database': 数据库名}
#    retry_count：重试次数
#return：构造生成的表名
def get_data_conn_with_retry(db_conf) :
    i = 0
    while i <= 5 :
        try :
            conn = get_data_conn(db_conf)
            return conn
        except :
            print ("cannot connect to database")
        i = i + 1
    if i == 5 :
        return None

#关闭相应的数据库连接，编写程序注意读写冲突
#    conn：数据库连接，由get_data_conn/get_data_conn_with_retry获得
#return：None
def connection_close(conn) :
    if conn :
        conn.close()
        
def connection_orm_close(conn) :
    if conn :
        conn.dispose()