import os


def main():
    # get path and save it for later
    path = os.getcwd()
    original_path = path

    # split into directories
    dirs = path.split('\\')

    # find the current dir
    i = 0
    for i in range(len(dirs)):
        if dirs[i] == 'OsuBeatmapStealer':
            break

    # stop it right there
    dirs = dirs[:i]

    # create the path again
    new_path = '\\'.join(dirs)

    # go into osu dir
    new_path = os.path.join(new_path, 'osu!')

    # add Songs to the path
    if os.listdir(new_path).count('Songs') == 1:
        new_path = os.path.join(new_path, 'Songs')

    # for each beatmap save the forum number
    beatmaps = os.listdir(new_path)
    re = list()
    for beatmap in beatmaps:
        beatmap_details = beatmap.split(' ')
        beatmap_number = beatmap_details[0]
        re.append(beatmap_number)

    print(re)

    # input("write something to close")


if __name__ == "__main__":
    main()
