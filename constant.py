# -*- coding: utf-8 -*-

#时间常量
SECONDS_PER_DAY = 86400
SECONDS_PER_HOUR = 3600
SECONDS_PER_MINUTE = 60

#时间戳范围
MIN_TIMESTAMP = 0
MAX_TIMESTAMP = 4102416000

#时区，正8表示东八区
TIME_ZONE = 8

#可选nagios或falcon，否则程序出错
OPS_SYSTEM_TYPE = 'FALCON'
#OPS_SYSTEM_TYPE = 'NAGIOS'

#QoS数据库编码格式
QOS_DB_CHARSET = 'utf8'

#数据库最大尝试连接次数
DB_MAX_RERTY_COUNT = 5

#程序的工作目录
WORK_DIR = '/root/deploy/cloud/VirtualPathComputation/'

#程序配置文件目录(相对于工作目录)
CONF_DIR = './config/config.conf'
