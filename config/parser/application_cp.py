# -*- coding: utf-8 -*-
import os
import sys
import errno
from configparser import ConfigParser

# 程序的环境变量，子目录测试用
# sys.path.append("..")
# sys.path.append("../..")

# 为模块引入全局常量
from constant import WORK_DIR

# import config_loader
import config.config as config


################################################################################
# 解析conf_loader中的配置文件项，cp即configParser
# 这里的conf_loader为config.init_conf与config.refresh的返回值
# 考虑到Python动态语言特性，故标出返回值的取值类型

# 检查Section common_config是否存在
#    conf_loader：配置文件加载器
# return：True为存在，反之为不存在
def is_common_config_available(conf_loader):
    common_conf_sct = config.conf_getsection(conf_loader, 'common_config')
    if not common_conf_sct:
        return False
    return True


# 检查Section pocomputing_config是否存在
#    conf_loader：配置文件加载器
# return：True为存在，反之为不存在
def is_pocomputing_config_available(conf_loader):
    pocomputing_conf_sct = config.conf_getsection(conf_loader, 'pocomputing_config')
    if not pocomputing_conf_sct:
        return False
    return True


# 获取网络监控平台的种类(已废弃)
#    conf_loader：配置文件加载器
# return：常规情况为NAGIOS或FALCON，类型为str
def get_net_monitor_platform(conf_loader):
    common_conf_sct = config.conf_getsection(conf_loader, 'common_config')
    if not common_conf_sct:

        return ''
    net_monitor_platform = config.conf_getstr(common_conf_sct, 'net_monitor_platform', 'FALCON')
    return net_monitor_platform


# 获取数据缓存目录
#    conf_loader：配置文件加载器
# return：数据缓存目录，类型为str
def get_data_cache_dir(conf_loader):
    common_conf_sct = config.conf_getsection(conf_loader, 'common_config')
    if not common_conf_sct:

        return ''
    data_cache_dir = config.conf_getstr(common_conf_sct, 'data_cache_dir', './data_cache/')
    if not data_cache_dir.startswith('/'):
        data_cache_dir = os.path.join(WORK_DIR, data_cache_dir)
    return data_cache_dir


# 获取日志缓存目录
#    conf_loader：配置文件加载器
# return：日志缓存目录，类型为str
def get_log_dir(conf_loader):
    common_conf_sct = config.conf_getsection(conf_loader, 'common_config')
    if not common_conf_sct:

        return ''
    log_dir = config.conf_getstr(common_conf_sct, 'log_dir', './log/')
    if not log_dir.startswith('/'):
        log_dir = os.path.join(WORK_DIR, log_dir)
    return log_dir


# 获取计算虚拟专线特征阶段，最大使用的CPU核心数
#    conf_loader：配置文件加载器
# return：最大使用的CPU核心数，类型为int
def get_cpu_core_size(conf_loader):
    common_conf_sct = config.conf_getsection(conf_loader, 'common_config')
    if not common_conf_sct:

        return 0
    cpu_core_size = config.conf_getint(common_conf_sct, 'cpu_core_size', 4)
    return cpu_core_size


# 获取设置的当前时区(已废弃)
#    conf_loader：配置文件加载器
# return：当前时区，类型为int，东八区则取8
def get_time_zone(conf_loader):
    common_conf_sct = config.conf_getsection(conf_loader, 'common_config')
    if not common_conf_sct:

        return 8
    time_zone = config.conf_getint(common_conf_sct, 'time_zone', 8)
    return time_zone


# 获取离线链路筛选文件目录，模型文件以.json结尾
def get_offline_model_dir(conf_loader):
    pocomputing_conf_sct = config.conf_getsection(conf_loader, 'pocomputing_config')
    if not pocomputing_conf_sct:

        return ''
    offline_model_dir = config.conf_getstr(pocomputing_conf_sct, 'offline_model_dir', './models/offline_models/')
    if not offline_model_dir.startswith('/'):
        offline_model_dir = os.path.join(WORK_DIR, offline_model_dir)
    return offline_model_dir


# 获取QoE文件目录，模型文件以.json结尾
def get_qoe_model_dir(conf_loader):
    pocomputing_conf_sct = config.conf_getsection(conf_loader, 'pocomputing_config')
    if not pocomputing_conf_sct:

        return ''
    qoe_model_dir = config.conf_getstr(pocomputing_conf_sct, 'qoe_model_dir', './models/qoe_models/')
    if not qoe_model_dir.startswith('/'):
        qoe_model_dir = os.path.join(WORK_DIR, qoe_model_dir)
    return qoe_model_dir


# 获取instab文件目录，模型文件以.json结尾
def get_instab_model_dir(conf_loader):
    pocomputing_conf_sct = config.conf_getsection(conf_loader, 'pocomputing_config')
    if not pocomputing_conf_sct:

        return ''
    instab_model_dir = config.conf_getstr(pocomputing_conf_sct, 'instab_model_dir', './models/instab_models/')
    if not instab_model_dir.startswith('/'):
        instab_model_dir = os.path.join(WORK_DIR, instab_model_dir)
    return instab_model_dir


# 获取topology文件目录，模型文件以.json结尾
def get_topology_model_dir(conf_loader):
    pocomputing_conf_sct = config.conf_getsection(conf_loader, 'pocomputing_config')
    if not pocomputing_conf_sct:

        return ''
    topology_model_dir = config.conf_getstr(pocomputing_conf_sct, 'topology_calc_conf_dir', './models/topology_calc/')
    if not topology_model_dir.startswith('/'):
        topology_model_dir = os.path.join(WORK_DIR, topology_model_dir)
    return topology_model_dir
