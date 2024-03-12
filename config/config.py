# -*- coding: utf-8 -*-
import os
import errno
from configparser import ConfigParser

#为模块引入全局常量
from constant import WORK_DIR
from constant import CONF_DIR

################################################################################
#提供一些配置文件读取的基本函数，使用开源模块ConfigParser
#
#定义conf_loader，作为配置文件管理。设计同相应的配置文件
#
#配置文件格式如下所示：
#[section 1]
#key1 = value1
#...
#keyn = valuen
#[section 2]
#key1 = value1
#...
#keyn = valuen
#...
#[section n]
#key1 = value1
#...
#keyn = valuen
#即每个section都对应一组键值对

#初始化配置文件
#    filename：配置文件名(包含目录)
#return：config_loader
def init_conf(filename = (WORK_DIR + CONF_DIR)) :
    config_filename = filename
    #print config_filename
    conf_loader = ConfigParser()
    conf_loader.read(config_filename)
    return conf_loader

#重新加载配置文件
#    filename：配置文件名(包含目录)
#return：config_loader
def refresh_conf(filename = (WORK_DIR + CONF_DIR)) :
    return init_conf(filename)

#获取配置文件中的section
#    config_loader：配置管理
#    key：section相应的Key名，类型为str
#return：config_loader
def conf_getsection(conf_loader, key) :
    if key in conf_loader :
        return conf_loader[key]
    print ("config : section " + str(key)  + " not found")
    return {}

#获取配置文件中某一section的配置项
#    conf_section：section，由conf_getsection函数获得
#    key：键，类型为str
#    default：若不包含相应key，则取相应默认值
#return：配置项的值，类型为str
def conf_getstr(conf_section, key, default = "") :
    if key in conf_section :
        return str(conf_section[key])
    print ("config: " + str(key) + " not found")
    return str(default)

#获取配置文件中某一section的配置项，若获取失败，则直接报错
#    conf_section：section，由conf_getsection函数获得
#    key：键，类型为str
#return：config_loader
def conf_get_mainstr(conf_section, key) :
    if key in conf_section :
        return str(conf_section[key])
    print ("config: " + str(key) + " not found" )
    raise ValueError

#获取配置文件中某一section的配置项，值的类型为int
#    conf_section：section，由conf_getsection函数获得
#    key：键，类型为str
#    default：若不包含相应key，则取相应默认值
#return：配置项的值，类型为int
def conf_getint(conf_section, key, default = 0) :
    if not type(default) is float and not type(default) is int :
        return 0
    value = default
    if not key in conf_section:
        return default
    try :
        tmp = conf_section.getfloat(key)
        value = int(tmp)
    except :
        print ("config: " + str(key) + ": wrong detected" )
    return value

#获取配置文件中某一section的配置项，值的类型为float
#    conf_section：section，由conf_getsection函数获得
#    key：键，类型为str
#    default：若不包含相应key，则取相应默认值
#return：配置项的值，类型为float
def conf_getfloat(conf_section, key, default = 0.0) :
    if not type(default) is float and not type(default) is int:
        return 0.0
    value = float(default)
    if not key in conf_section:
        return default
    try :
        tmp = conf_section.getfloat(key)
        value = tmp
    except :
        print ("config: " + str(key) + ": wrong detected" )
    return value

#获取配置文件中某一section的配置项，值的类型为bool
#    conf_section：section，由conf_getsection函数获得
#    key：键，类型为str
#    default：若不包含相应key，则取相应默认值
#return：配置项的值，类型为bool
def conf_getbool(conf_section, key, default = False) :
    if not type(default) is bool :
        return bool
    value = default
    if not key in conf_section:
        return default
    try :
        tmp = conf_section.getboolean(key)
        value = tmp
    except :
        print ("config: " + str(key) + ": wrong detected" )
    return value