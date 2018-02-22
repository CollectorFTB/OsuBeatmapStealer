from os.path import dirname
from sys import executable as exec_path


def get_path():
    return dirname(exec_path)
