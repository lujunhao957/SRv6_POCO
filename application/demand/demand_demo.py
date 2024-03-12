# -*- coding: utf-8 -*-

################################################################################
#提供两种测试Demo

def get_test_demand_1() :
    demand_1 = {
        'poco_source_id' : 1,
        'poco_des_id' : 2,
        'path_count' : 3,
        'demand_type' : 'backbone',
        'sort_by' : 'rta',
        'ascending': False,
        'topology_info' : {
            'user_side_links' : [
                [1, 2], [2, 3], [1, 3],
                [2, 1], [3, 2], [3, 1],
            ]
        },
        'qos_demand' : {
            'rta' : { 'max' : 80 },
            'packet_loss' : { 'max' : 0.10 },
            'bandwidth' : { 'min' : 1 }
        },
        'qoe_demand' : {
        },
        'topology_demand' : {
            'paths_damage' : { 'max' : 0.80 }
        },
        'options' : {
            'qos' : {
                'packet_size' : 64,
                'rta' : {'deviation' : 0.2 },
                'packet_loss' : {'deviation' : 0.2 }
            },
            'qoe' : { 'indicator_name' : 'mos', 'service_type' : 'audio' },
            'instability' : { 'service_type' : 'audio' },
            'addition' : {
                'percentile' : {
                    'percentile1' : 0.05,
                    'percentile2' : 0.25,
                    'percentile3' : 0.75,
                    'percentile4' : 0.95
                }
            }
        }
    }
    return demand_1
    #return {'demand' : str(demand_1)}

def get_test_demand_2() :
    demand_2 = {
        'poco_source_id' : 1,
        'poco_des_id' : 2,
        'path_count' : 3,
        'sort_by' : 'rta',
        'demand_type' : 'user',
        'ascending': False,
        'topology_info' : {
            'user_side_links' : [
                [1, 2], [3, 8], [4, 8],
                [2, 1], [8, 3], [8, 4]
            ],
            'backbone_side_links' :[
                [[2, 4],[2, 3, 4]],
                [[3, 4],[3, 2, 4]]
            ]
        },
        'qos_demand' : {
            'rta' : { 'max' : 80 },
            'packet_loss' : { 'max' : 0.10 },
            'bandwidth' : { 'min' : 1 }
        },
        'qoe_demand' : {
        },
        'topology_demand' : {
            'paths_damage' : { 'max' : 0.80 }
        },
        'options' : {
            'qos' : {
                'packet_size' : 64,
                'rta' : {'deviation' : 0.2 },
                'packet_loss' : {'deviation' : 0.2 }
            },
            'qoe' : { 'indicator_name' : 'mos', 'service_type' : 'audio' },
            'instability' : { 'service_type' : 'audio' },
            'addition' : {
                'percentile' : {
                    'percentile1' : 0.05,
                    'percentile2' : 0.25,
                    'percentile3' : 0.75,
                    'percentile4' : 0.95
                }
            }
        }
    }
    return demand_2
