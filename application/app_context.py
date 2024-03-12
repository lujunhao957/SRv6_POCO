# -*- coding: utf-8 -*-
import itertools
import sys
import copy
import json
import time
import importlib
import warnings
import networkx as nx
from itertools import combinations
import pandas as pd


import application.demand.poco_demand_parser as poco_demand_parser
import application.demand.demand_parser as srv6_pathapp_webrtc_demand_parser

import application.topology.topology_handler as topology_handler
import application.topology.topology_calc as topology_calc
import application.topology.topology_connectivity_probability as topo_conn_p

import logger.logger as logger
import utils.datetime_utils as datetime_utils
import multiprocessing
import matplotlib.pyplot as plt
from database.db_conn import get_data_conn_orm
from feature.qoe.webrtcquality import path_meet_webrtc_quality
from path.path_calc import build_gpath_list
from path.path_damage import gpath_list_damage_filter
from path.path_sort import webrtc_quality_gpath_list_sort

_MODULE_NAME = u'application.app_context'
_DEBUG_MODE = True
# 性能测试使用
import copy

# test_data = {}

warnings.filterwarnings("ignore")


def test_print(test_str):
    if False: print ('' + str(test_str))


def optimal_virtual_path_cal(srv6_pathapp_webrtc_demand):
    calculator = virtual_path_calculator(srv6_pathapp_webrtc_demand, 'vpath_calc')
    result = calculator.optimal_virtual_path_cal()
    return result

all_webrtc_demand = {}

all_path = {}

node_id_ipv4_map={}
node_id_ipv6_map={}
calculator_id_demand_map={}


class virtual_path_calculator(object):

    def __init__(self, srv6_pathapp_webrtc_demand, request_type):
        s = time.time()
        self.request_type = request_type
        self.calculator_id = str(int(time.time() * 10000))[-12:]
        logger.log_info(_MODULE_NAME, u'Starting application context initialization')

        self.srv6_pathapp_webrtc_demand = srv6_pathapp_webrtc_demand['demandInfo']
        logger.log_info(_MODULE_NAME, u'Loading basic information from config file')

        calculator_id_demand_map[self.calculator_id]=self.srv6_pathapp_webrtc_demand

        # self._load_config_from_file()
        # logger.log_info(_MODULE_NAME, u'Loading basic information from config file successful')
        # logger.log_info(_MODULE_NAME, u'Loading basic information from database')

        self._load_config_from_database()
        # logger.log_info(_MODULE_NAME, u'Loading basic information from database successful')
        # logger.log_info(_MODULE_NAME, u'Starting parsing pocomputing demand')

        self._parse_srv6_pathapp_webrtc_demand(srv6_pathapp_webrtc_demand['demandInfo'])
        logger.log_info(_MODULE_NAME, u'Parsing pocomputing demand finished')
        # if _DEBUG_MODE:
        #     data_cache.json_data_cache(pocomputing_demand, self.data_cache_dir, \
        #                                self.calculator_id + '_demand' + '.json')
        logger.log_info(_MODULE_NAME, u'Application context initialization Finished \n\n')
        test_print('app init total time : ' + str(time.time() - s))

    def result_list_to_string(self,result_list):
        rows_as_strings = [' '.join(str(row)) for row in result_list]
        templist=[]
        for path in result_list:
            res = ' '.join(map(str, path))
            templist.append(res)
        result = '|'.join(templist)
        return result

    def optimal_virtual_path_cal(self):
        s1 = time.time()
        result_list = self.webrtc_virtual_path_cal()
        result= self.result_list_to_string(result_list)
        s2 = time.time()
        return 202, result

    def demand_is_calculate(self):     #判断该需求是否被计算
        if str(self.webrtc_quality) in all_webrtc_demand:
            return True
        return False

    def get_result_from_calculate(self):       #若计算过，直接从结果中获得
        all_path=all_webrtc_demand[json.dumps(self.webrtc_quality)]
        result=[]
        for path_info in all_path:
            path=path_info.get_path()
            if path[0]==self.source_id and path[len(path)-1]==self.des_id:
                result.append(path_info)
        return result


    def cal_all_path_webrtc_quality(self):             #根据webrtc视频质量需求计算所有满足需求的虚拟专线
        all_paths=[]
        all_nodes=list(self.topology_graph.nodes())
        for i in range(0,len(all_nodes)):
            for j in range(0,len(all_nodes)):
                if i!=j:
                    temp_paths = nx.all_simple_paths(self.topology_graph, source=all_nodes[i], target=all_nodes[j])
                    for path in temp_paths:
                        all_paths.append(path)
        json_str = json.dumps(self.webrtc_quality)
        result=[]
        for path in all_paths:
            path_info=path_meet_webrtc_quality(path,self.webrtc_quality)           #判断虚拟专线是否满足webrtc视频播放质量需求
            # print(path_info.get_path(),path_info.get_buffer_duration_probability(),path_info.get_continuous_playback_duration_probability())
            if path_info.get_buffer_duration_probability() < self.webrtc_quality['buffer_duration_probability'] and path_info.get_continuous_playback_duration_probability() > self.webrtc_quality['continuous_playback_duration_probability']:
                result.append(path_info)
        all_webrtc_demand[json_str]=result


    def get_webrtc_all_virtual_path(self):   #获取符合需求的所有虚拟专线
        if self.demand_is_calculate()==True:      #计算过，直接获取
            result=self.get_result_from_calculate()
        else:                               #没计算过，先计算在获取
            self.cal_all_path_webrtc_quality()
            result = self.get_result_from_calculate()
        return result

    def get_hop(self,path):          #获取路径最大跳数
        return len(path)

    def get_webrtc_all_max_hop_virtual_path(self,webrtc_all_virtual_path):      #根据最大跳数过滤虚拟专线
        webrtc_all_max_hop_virtual_path=[]
        for path_info in webrtc_all_virtual_path:
            path = path_info.get_path()
            if self.get_hop(path)<self.max_hop:
                webrtc_all_max_hop_virtual_path.append(path_info)
        return webrtc_all_max_hop_virtual_path


    def get_webrtc_all_max_damage_virtual_path(self,webrtc_all_max_hop_virtual_path):            #根据破坏度过滤虚拟专线

        group_path_list=build_gpath_list(webrtc_all_max_hop_virtual_path, self.path_count)          #虚拟专线分组

        group_path_list_filter=gpath_list_damage_filter(group_path_list,self.max_damage)                      #过滤不满足虚拟专线破坏度的组

        result=webrtc_quality_gpath_list_sort(group_path_list_filter)             #对满足虚拟专线破坏度的组排序

        return result



    def webrtc_virtual_path_cal(self):          #虚拟专线计算业务
        s = time.time()
        webrtc_all_virtual_path = self.get_webrtc_all_virtual_path()            #获取所有虚拟专线
        webrtc_all_max_hop_virtual_path=self.get_webrtc_all_max_hop_virtual_path(webrtc_all_virtual_path)            #根据最大跳数过滤虚拟专线
        webrtc_all_max_damage_virtual_path=self.get_webrtc_all_max_damage_virtual_path(webrtc_all_max_hop_virtual_path)                 #根据破坏度过滤虚拟专线
        result=[]
        for path_info in webrtc_all_max_damage_virtual_path[0]:
            result.append(path_info.get_path())
        return result
        # return webrtc_all_max_damage_virtual_path


    def _load_config_from_file(self):
        return True

    def _load_config_from_database(self):     #加载节点id到节点name的映射关系
        conn = get_data_conn_orm('')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM node")
        nodelist = cursor.fetchall()
        cursor.execute("SELECT * FROM topo")
        topolist=cursor.fetchall()
        self.node_id_name_map = {}
        self.node_name_id_map = {}
        self.node_id_ipv4_map = {}
        self.node_id_ipv6_map = {}
        for row in nodelist:
            self.node_id_name_map[row[0]]=row[1]
            self.node_name_id_map[row[1]] = row[0]
            node_id_ipv4_map[row[0]] = row[2]
            node_id_ipv6_map[row[0]] = row[3]
        self._initialize_topology_graph(topolist)
        return True

    def _parse_srv6_pathapp_webrtc_demand(self, srv6_pathapp_webrtc_demand):
        self.source_name = srv6_pathapp_webrtc_demand_parser.get_source_name(srv6_pathapp_webrtc_demand, self.node_id_name_map)
        logger.log_info(_MODULE_NAME, u'Source name : ' + str(self.source_name))
        self.des_name = srv6_pathapp_webrtc_demand_parser.get_des_name(srv6_pathapp_webrtc_demand, self.node_id_name_map)
        logger.log_info(_MODULE_NAME, u'Destination name : ' + str(self.des_name))

        self.source_id = srv6_pathapp_webrtc_demand_parser.get_source_id(srv6_pathapp_webrtc_demand)
        logger.log_info(_MODULE_NAME, u'Source name : ' + str(self.source_id))
        self.des_id = srv6_pathapp_webrtc_demand_parser.get_des_id(srv6_pathapp_webrtc_demand)
        logger.log_info(_MODULE_NAME, u'Destination name : ' + str(self.des_id))

        self.webrtc_quality=srv6_pathapp_webrtc_demand_parser.get_webrtc_quality(srv6_pathapp_webrtc_demand)

        self.path_count = srv6_pathapp_webrtc_demand_parser.get_path_count(srv6_pathapp_webrtc_demand)
        logger.log_info(_MODULE_NAME, u'Path count : ' + str(self.path_count))
        self.max_hop = srv6_pathapp_webrtc_demand_parser.get_max_hop(srv6_pathapp_webrtc_demand)
        logger.log_info(_MODULE_NAME, u'Max router count : ' + str(self.max_hop))
        self.max_damage = srv6_pathapp_webrtc_demand_parser.get_max_damage(srv6_pathapp_webrtc_demand)
        logger.log_info(_MODULE_NAME, u'max_damage : ' + str(self.max_damage))
        return True

    def _initialize_topology_graph(self,topo_list):         #初始化计算拓扑
        self.topology_graph = nx.Graph()
        # 添加节点
        for row in topo_list:
            self.topology_graph.add_node(row[0])
            # 添加边
        for row in topo_list:
            # 将邻居字符串拆分为列表
            neighbor_list = row[2].split('|')
            # 添加从当前节点到每个邻居节点的边
            for neighbor in neighbor_list:
                self.topology_graph.add_edge(int(row[0]), int(neighbor))
        return True

    def _load_qos_data_set(self):
        format_data_set_map = {}
        # 性能测试临时代码，虚拟专线计算的数据不通过OpenFalcon读取，通过截取网络切片计算数据获得
        # if self.request_type == 'topo_calc':
        #     # probe_list = qos_data_loader.get_probe_list(self.ping_packet_size)
        #     global test_data
        #     format_data_set_map = test_data
        #     logger.log_debug(_MODULE_NAME, 'Get data for path cal success!')

        return format_data_set_map



