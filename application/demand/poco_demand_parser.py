# -*- coding: utf-8 -*-
import json
import copy

################################################################################
# 负责完成解析相应的需求信息，将需求转换为变量

_DEFAULT_PATH_COUNT = 1
#  偏向于最新值
_DEFAULT_QOS_DEVIATION = 1.0
_DEFAULT_PING_PACKET_SIZE = 64
#  QoE与不稳定度模型默认值
# _ DEFAULT_QOE_INDICATOR_NAME = 'mos'
# _DEFAULT_QOE_SERVICE_TYPE = 'demo'
# _DEFAULT_INSTAB_SERVICE_TYPE = 'demo'
_DEFAULT_MAX_HOP = 4

_DEFAULT_PERCENTILE = {
    'percentile1': 0.05,
    'percentile2': 0.25,
    'percentile3': 0.75,
    'percentile4': 0.95
}

_POCO_COMPUTING_NOUN_MAP = {
    'rta': 'rta',
    'packetLoss': 'packet_loss',
    'jitter': 'jitter',
    'bandwidth': 'bandwidth'
}


def parse_poco_demand(poco_demand):
    pocomputing_demand = {}
    pocomputing_demand['topology_info'] = {}
    pocomputing_demand['qos_demand'] = {}
    pocomputing_demand['qoe_demand'] = {}
    pocomputing_demand['topology_demand'] = {}
    pocomputing_demand['options'] = {}

    demand_info = poco_demand['demandInfo']
    pocomputing_demand['poco_source_id'] = int(demand_info['srcId'])
    pocomputing_demand['poco_des_id'] = int(demand_info['desId'])
    pocomputing_demand['path_count'] = demand_info.get('pathCount', _DEFAULT_PATH_COUNT)
    pocomputing_demand['ascending'] = bool(demand_info['ascending'])
    pocomputing_demand['demand_type'] = str(demand_info['type'])
    pocomputing_demand['max_hop'] = _DEFAULT_MAX_HOP
    if 'maxHop' in demand_info:
        pocomputing_demand['max_hop'] = int(demand_info['maxHop'])

    sort_by = str(demand_info['pathPriorityType'])
    pocomputing_demand['sort_by'] = sort_by

    if sort_by in _POCO_COMPUTING_NOUN_MAP:
        pocomputing_demand['sort_by'] = _POCO_COMPUTING_NOUN_MAP[sort_by]
    if 'betweenness' in demand_info:
        pocomputing_demand['topology_demand']['damage'] = {'max': demand_info['betweenness']}



    return pocomputing_demand
