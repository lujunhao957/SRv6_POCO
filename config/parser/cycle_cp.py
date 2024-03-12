# -*- coding: utf-8 -*-
import os
import sys
import errno
from configparser import ConfigParser

#程序的环境变量，子目录测试用
#sys.path.append("..")
#sys.path.append("../..")

#import config_loader
import config.config as config

################################################################################
#解析conf_loader中的配置文件项，cp即configParser(测量时间周期与统计时间周期)
#这里的conf_loader为config.init_conf与config.refresh的返回值
#考虑到Python动态语言特性，故标出返回值的取值类型

#测量时间周期(单位为分钟，三种probe_method：ping64,ping1024,bandwidth)
#格式如下:
#    probe_cycle = {
#        'ping64' : 5,
#        'ping1024' : 5,
#        'bandwidth' : 240
#    }
#统计时间周期(单位为分钟，三种probe_method：ping64,ping1024,bandwidth)
#格式如下:
#    probe_cycle = {
#        'ping64' : {'rta':60, 'packet_loss':60},
#        'ping1024' : {'rta':60, 'packet_loss':60}
#    }
#

#检查Section common_config是否存在
#    conf_loader：配置文件加载器
#return：True为存在，反之为不存在

#检查Section monitor_config是否存在
#    conf_loader：配置文件加载器
#return：True为存在，反之为不存在
def is_monitor_config_available(conf_loader) :
    monitor_conf_sct = config.conf_getsection(conf_loader, 'monitor_config')
    if not monitor_conf_sct :
        return False
    return True

#检查Section pocomputing_config是否存在
#    conf_loader：配置文件加载器
#return：True为存在，反之为不存在
def is_pocomputing_config_available(conf_loader) :
    pocomputing_conf_sct = config.conf_getsection(conf_loader, 'pocomputing_config')
    if not pocomputing_conf_sct :
        return False
    return True


