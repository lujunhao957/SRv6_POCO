# -*- coding: utf-8 -*-
import os
import gc
import sys
import ujson

def json_data_cache(json_data, cache_dir, filename) :
    pathname = os.path.join(str(cache_dir), str(filename))
    cache_str = ujson.dumps(json_data)
    f = open(pathname, 'w')
    f.write(cache_str)
    f.close()
    return True

def dataframe_data_cache(pd_data, cache_dir, filename) :
    pathname = os.path.join(str(cache_dir), str(filename))
    pd_data.to_csv(str(pathname))
    return True