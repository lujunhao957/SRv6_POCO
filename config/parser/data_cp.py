# -*- coding: utf-8 -*-
import os
import sys
import errno
from configparser import ConfigParser

#程序的环境变量，子目录测试用
#sys.path.append("..")
#sys.path.append("../..")

#为模块引入全局常量


#import config_loader
import config.config as config

################################################################################
#解析conf_loader中的配置文件项，cp即configParser(数据库)
#这里的conf_loader为config.init_conf与config.refresh的返回值
#考虑到Python动态语言特性，故标出返回值的取值类型

#返回数据库配置项，可以直接传入database.db_conn函数中,格式如下：
#    dbconf：即数据库连接信息，结构为Dict
#    { 'ipaddr': 数据库IP地址,
#     'port': 数据库端口号,
#     'username': 数据库用户名,
#     'passwd': 数据库密码,
#     'database': 数据库名}

#检查Section pocomputing_database是否存在
#    conf_loader：配置文件加载器
#return：True为存在，反之为不存在
def is_pococomputing_available(conf_loader) :
    pocomputing_conf_sct = config.conf_getsection(conf_loader, 'pocomputing_database')
    if not pocomputing_conf_sct :
        print ("config : init section [poco_computing_databasmonitorplatforme] fail")
        return False
    return True

#检查Section monitor_database是否存在
#    conf_loader：配置文件加载器
#return：True为存在，反之为不存在
def is_monitor_available(conf_loader) :
    monitor_conf_sct = config.conf_getsection(conf_loader, 'monitor_data_api')
    if not monitor_conf_sct :
        print ("config : init section [monitor_database] fail")
        return False
    return True

#解析pocomputing自身的数据库db
#    conf_loader：配置文件加载器
#return：dbconf
def get_pocomputing_db_conf(conf_loader) :
    pocomputing_conf_sct = config.conf_getsection(conf_loader, 'pocomputing_database')
    pocomputing_dbconf = {}
    if not pocomputing_conf_sct :
        print ("config : init section [pocomputing_database] fail")
        return pocomputing_dbconf
    try :
        pocomputing_dbconf = {
            'username' : config.conf_get_mainstr(pocomputing_conf_sct, 'pocomputing_username'),
            'passwd' : config.conf_get_mainstr(pocomputing_conf_sct, 'pocomputing_passwd'),
            'ipaddr' : config.conf_get_mainstr(pocomputing_conf_sct, 'pocomputing_ipaddr'),
            'port' : config.conf_getint(pocomputing_conf_sct, 'pocomputing_port', 3306),
            'database' : config.conf_get_mainstr(pocomputing_conf_sct, 'pocomputing_database')
        }
    except :
        print ("config : load database information from config file fail")
        return {}
    return pocomputing_dbconf

#解析监控平台(Nagios/Open-Falcon)的数据库db
#    conf_loader：配置文件加载器
#return：dbconf
def get_monitor_api_conf(conf_loader) :
    monitor_conf_sct = config.conf_getsection(conf_loader, 'monitor_data_api')
    if not monitor_conf_sct :
        print ("config : init section [monitor_data_api] fail")
        return ''
    try :
        ipaddr = config.conf_get_mainstr(monitor_conf_sct, 'monitor_ipaddr')
        port = config.conf_getint(monitor_conf_sct, 'monitor_port', 9966)
        return str(ipaddr) + ':' + str(port)
    except :
        print ("config : load database information from config file fail")
        return ''
