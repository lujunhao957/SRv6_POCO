# -*- coding: utf-8 -*-
import importlib
import constant
import config.config as config
from configparser import ConfigParser


################################################################################
# 本程序的作用：为程序初始化配置项，调用相应函数实现
#    1. 需要额外防止污染主程序的命名空间
#    2. 整个程序额外包装API，更加便于更换实现，降低与其他模块的耦合
#        比方说，需要增加新功能，而便于改动其他模块/或者直接实现新模块
#        每个函数保证相应的功能正常即可，甚至不关心实现形式与数据结构
#    3.控制整个程序调用，且易于测试，方便直接调试

################################################################################
# 以下函数完成的功能为，基本配置项读取

def init_conf_loader():
    conf_loader = config.init_conf()
    return conf_loader


def get_current_time_zone():
    return constant.TIME_ZONE


def get_cpu_core_size(conf_loader):
    application_conf_parser = importlib.import_module("config.parser.application_cp")
    if not application_conf_parser.is_common_config_available(conf_loader):
        print 'load from config file fail'
    cpu_core_size = application_conf_parser.get_cpu_core_size(conf_loader)
    return cpu_core_size


def get_data_cache_dir(conf_loader):
    application_conf_parser = importlib.import_module("config.parser.application_cp")
    if not application_conf_parser.is_common_config_available(conf_loader):
        print 'load from config file fail'
    data_cache_dir = application_conf_parser.get_data_cache_dir(conf_loader)
    return data_cache_dir


def get_log_dir(conf_loader):
    application_conf_parser = importlib.import_module("config.parser.application_cp")
    if not application_conf_parser.is_common_config_available(conf_loader):
        print 'load from config file fail'
    log_dir = application_conf_parser.get_log_dir(conf_loader)
    return log_dir


def get_ops_system(conf_loader):
    ops_system_str = constant.OPS_SYSTEM_TYPE
    return ops_system_str


def get_monitor_socket(conf_loader):
    data_conf_parser = importlib.import_module("config.parser.data_cp")
    if not data_conf_parser.is_monitor_available(conf_loader):
        print 'load from config file fail'
    monitor_socket = data_conf_parser.get_monitor_api_conf(conf_loader)
    return monitor_socket


def get_pocomputing_dbconf(conf_loader):
    data_conf_parser = importlib.import_module("config.parser.data_cp")
    if not data_conf_parser.is_pococomputing_available(conf_loader):
        print 'load from config file fail'
    pocomputing_db_conf = data_conf_parser.get_pocomputing_db_conf(conf_loader)
    return pocomputing_db_conf


def get_probe_cycle(conf_loader):
    cycle_conf_parser = importlib.import_module("config.parser.cycle_cp")
    if not cycle_conf_parser.is_monitor_config_available(conf_loader):
        print 'load from config file fail'
    probe_cycle = cycle_conf_parser.get_probe_cycle(conf_loader)
    return probe_cycle


def get_probe_cycle_offset(conf_loader):
    cycle_conf_parser = importlib.import_module("config.parser.cycle_cp")
    if not cycle_conf_parser.is_monitor_config_available(conf_loader):
        print 'load from config file fail'
    probe_cycle_offset = cycle_conf_parser.get_probe_cycle_offset(conf_loader)
    return probe_cycle_offset


def get_stats_cycle(conf_loader):
    cycle_conf_parser = importlib.import_module("config.parser.cycle_cp")
    if not cycle_conf_parser.is_monitor_config_available(conf_loader):
        print 'load from config file fail'
    stats_cycle = cycle_conf_parser.get_stats_cycle(conf_loader)
    return stats_cycle


def get_offline_model_dir(conf_loader):
    application_conf_parser = importlib.import_module("config.parser.application_cp")
    if not application_conf_parser.is_pocomputing_config_available(conf_loader):
        print 'load from config file fail'
    offline_model_dir = application_conf_parser.get_offline_model_dir(conf_loader)
    return offline_model_dir


def get_qoe_model_dir(conf_loader):
    application_conf_parser = importlib.import_module("config.parser.application_cp")
    if not application_conf_parser.is_pocomputing_config_available(conf_loader):
        print 'load from config file fail'
    qoe_model_dir = application_conf_parser.get_qoe_model_dir(conf_loader)
    return qoe_model_dir


def get_instab_model_dir(conf_loader):
    application_conf_parser = importlib.import_module("config.parser.application_cp")
    if not application_conf_parser.is_pocomputing_config_available(conf_loader):
        print 'load from config file fail'
    instab_model_dir = application_conf_parser.get_instab_model_dir(conf_loader)
    return instab_model_dir


def get_topology_model_dir(conf_loader):
    application_conf_parser = importlib.import_module("config.parser.application_cp")
    if not application_conf_parser.is_pocomputing_config_available(conf_loader):
        print 'load from config file fail'
    topology_model_dir = application_conf_parser.get_topology_model_dir(conf_loader)
    return topology_model_dir
