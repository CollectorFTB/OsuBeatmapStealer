import os


def get_path():
    # get path and save it for later
    path = os.getcwd()

    # split into directories
    dirs = path.split('\\')

    # find the current dir
    i = dirs.index('OsuBeatmapStealer')

    return dirs, i
