import os
import sys


def path(relative_path):
    """
    生成资源文件目录访问路径
    :param relative_path:
    :return:
    """
    print('sys.prefix', sys.prefix)
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = sys.prefix
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
