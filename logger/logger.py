# -*- coding: utf-8 -*-
import sys
import datetime

import logging
import logging.handlers
import os

log_name = 'pccp'
time_handler = logging.handlers.TimedRotatingFileHandler(os.path.join("D:\pythonProject\SRv6_PATHAPP_WEBRTC\logger", log_name),
                                                         when='MIDNIGHT', interval=1)
time_handler.suffix = '%Y%m%d.log'
time_handler.setLevel('DEBUG')

fmt = '%(asctime)s - %(funcName)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt)
time_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(time_handler)

def log_info(module_str, log_str) :
    loginfo = str(datetime.datetime.now()) + ' INFO - ' + str(module_str) + ' - ' + str(log_str)
    logger.info(log_str)

def log_debug(module_str, log_str) :
    loginfo = str(datetime.datetime.now()) + ' DEBUG - ' + str(module_str) + ' - ' + str(log_str)
    logger.debug(log_str)
    print (loginfo)
    
def log_warn(module_str, log_str) :
    loginfo = str(datetime.datetime.now()) + ' WARN - ' + str(module_str) + ' - ' + str(log_str)
    logger.warn(log_str)
    print (loginfo)