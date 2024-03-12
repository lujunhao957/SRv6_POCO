# -*- coding: utf-8 -*-

################################################################################
#提供两种测试Demo

def get_test_demand_1() :
    pathapp_demand = {
        "demandInfo" : {
            "srcId" : "4",
            "desId" : "3",
            "type" : "backbone",
            "pathCount" : 3,
            "ascending" : False,
            "damage" : 1.0,
            "pathPriorityType" : "rta"
        },
        "qosDemand" : {
            "bandwidth" : 0.1,
            "rta" : 1000.0,
            "packetLoss" : 0.1
        },
        "topologyInfo" : {
                "virtualLinks" : [
                    "3-4",
                    "4-3",
                    "1-3",
                    "3-1",
                    "4-1",
                    "1-4"
                ]
        },
        "options" : {
            "packetSize" : 64,
            "rtaDeviation" : 0.2,
            "packetLossDeviation" : 0.2,
            "serviceType" : "audio",
            "indicatorName" : "mos",
            "percentile" : [0.05, 0.25, 0.75, 0.95]
        }
    }
    return pathapp_demand
    
def get_test_demand_2() :
    pathapp_demand2 = {
        "demandInfo" : {
            "srcId" : "1",
            "desId" : "8",
            "type" : "user",
            "pathCount" : 3,
            "ascending" : False,
            "damage" : 1.0,
            "pathPriorityType" : "rta"
        },
        "qosDemand" : {
            "bandwidth" : 0.1,
            "rta" : 1000.0,
            "packetLoss" : 0.1
        },
        "topologyInfo" : {
            "virtualLinks" : [
                "1-2",
                "3-8",
                "4-8",
                "2-1",
                "8-3",
                "8-4"
            ],    
            "virtualPaths" : {
                "3-2" : "3-4-2",
                "2-3" : "2-4-3",
                "2-4" : "2-4",
                "4-2" : "4-2"
            }
        },
        "options" : {
            "packetSize" : 64,
            "rtaDeviation" : 0.2,
            "packetLossDeviation" : 0.2,
            "serviceType" : "audio",
            "indicatorName" : "mos",
            "percentile" : [0.05, 0.25, 0.75, 0.95]
        }
    }
    return pathapp_demand2