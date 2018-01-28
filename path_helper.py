from os import getcwd


def get_path():
    # get path and save it for later
    path = getcwd()

    # get path of the OsuBeatmapStealer directory
    inner_path = path[:path.find('OsuBeatmapStealer') + len('OsuBeatmapStealer')]

    return inner_path
