from os import getcwd


def get_path():
    # get path and save it for later
    path = getcwd()

    # outer dir
    outer_path = path[:path.find('OsuBeatmapStealer')-1]

    # inner dir
    inner_path = path[:path.find('OsuBeatmapStealer') + len('OsuBeatmapStealer')]

    return outer_path, inner_path
