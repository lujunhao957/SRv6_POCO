# -*- coding: utf-8 -*-
import os
import sys
import json

import feature.topology.model_loader

_DEFAULT_SUFFIX_STR = '.json'


def load_all_topology_model(topology_dir):
    topology_dir = str(topology_dir)
    fname_list = os.listdir(topology_dir)
    topology_service_model_map = {}
    for filename in fname_list:
        if filename.endswith(_DEFAULT_SUFFIX_STR):
            filename = os.path.join(topology_dir, filename)
            topology_model = feature.topology.model_loader.load_topology_model(filename)
            if topology_model:
                service_type = feature.topology.model_loader.get_topology_service_type(topology_model)
                topology_service_model_map[service_type] = topology_model
    return topology_service_model_map


def get_topology_model(topology_service_model_map, service_type):
    topology_model = topology_service_model_map[service_type]
    return topology_model
