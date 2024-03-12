# -*- coding: utf-8 -*-
import os
import errno

################################################################################
#此py设计目的为，包装原生os库，实现基本功能

#递归创建文件目录
#return：无返回
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise