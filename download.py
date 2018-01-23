import os
import webbrowser
import time


def download_beatmaps():
    # get path and save it for later
    path = os.getcwd()

    # split into directories
    dirs = path.split('\\')

    # find the current dir
    i = 0
    for i in range(len(dirs)):
        if dirs[i] == 'OsuBeatmapStealer':
            break

    # stop it right there
    dirs = dirs[:i+1]

    # create the path again
    new_path = '\\'.join(dirs)

    # get the paths for both the files
    my_beatmaps_path = os.path.join(new_path, 'my_beatmaps.txt')
    other_beatmaps_path = os.path.join(new_path, 'beatmaps.txt')

    # open up the file for writing
    my_beatmaps_file = open(my_beatmaps_path, 'r')
    other_beatmaps_file = open(other_beatmaps_path, 'r')

    # get your numbers
    my_beatmap_numbers = list()
    for line in my_beatmaps_file:
        my_beatmap_numbers.append(int(line.split('/')[-1]))

    # get other numbers
    other_beatmap_numbers = list()
    for line in other_beatmaps_file:
        other_beatmap_numbers.append(int(line.split('/')[-1]))

    # remove your beatmaps from his list
    for beatmap in my_beatmap_numbers:
        try:
            other_beatmap_numbers.remove(beatmap)
        except ValueError:
            pass

    # remove maps that appear more than once
    for i in range(len(other_beatmap_numbers)-1):
        while other_beatmap_numbers[i] == other_beatmap_numbers[i+1]:
            other_beatmap_numbers.remove(other_beatmap_numbers[i+1])

    # create download links for each of the numbers left on his list
    beatmap_link_list = list()
    for beatmap_number in other_beatmap_numbers:
        beatmap_link_list.append("https://osu.ppy.sh/d/" + str(beatmap_number))

    # start downloading beatmaps
    for url in beatmap_link_list:
        webbrowser.open_new_tab(url)
        ##################################################################
        # if your browser is dying you might want to up this number to 3 #
        ##################################################################
        time.sleep(2)
