import os


def get_path():
    # get path and save it for later
    path = os.getcwd()

    # outer dir
    out_path = path[:path.find('OsuBeatmapStealer')-1]

    # inner dir
    in_path = path[:path.find('OsuBeatmapStealer') + len('OsuBeatmapStealer')]

    return out_path, in_path
