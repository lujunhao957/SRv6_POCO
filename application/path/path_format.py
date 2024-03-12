# -*- coding: utf-8 -*-
import path.path_format as path_format

def optimal_vpaths_to_str(final_path_list, poco_nameid_map) :
    final_path_list_str = path_format.format_vpathcal_result(final_path_list, poco_nameid_map)
    return final_path_list_str