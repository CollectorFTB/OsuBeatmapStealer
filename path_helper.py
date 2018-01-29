from os.path import dirname


def get_path():
    # get path and save it for later
    path = dirname(__file__)
    # get path of the OsuBeatmapStealer directory
    inner_path = path[:path.find('OsuBeatmapStealer') + len('OsuBeatmapStealer')]

    return inner_path
