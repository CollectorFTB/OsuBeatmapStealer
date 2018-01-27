import os
import webbrowser
import time
from path_helper import get_path


def download_beatmaps(interval):
    # get path and save it for later
    new_path = get_path()[1]

    # get the paths for both the files
    my_beatmaps_path = os.path.join(new_path, 'my_beatmaps.txt')
    other_beatmaps_path = os.path.join(new_path, 'beatmaps.txt')

    # open up the file for writing
    with open(my_beatmaps_path, 'r') as my_beatmaps_file:
        # get your numbers
        my_beatmap_numbers = [int(line.split('/')[-1]) for line in my_beatmaps_file]

    with open(other_beatmaps_path, 'r') as other_beatmaps_file:
        # get other numbers
        other_beatmap_numbers = [int(line.split('/')[-1]) for line in other_beatmaps_file]

    # remove your beatmaps from his list and eliminate duplicates
    my_beatmap_numbers = set(my_beatmap_numbers)
    other_beatmap_numbers = set(other_beatmap_numbers)
    other_beatmap_numbers -= my_beatmap_numbers
    other_beatmap_numbers = list()

    # create download links for each of the numbers left on his list
    beatmap_link_list = ["https://osu.ppy.sh/d/" + str(beatmap_number) for beatmap_number in other_beatmap_numbers]

    # start downloading beatmaps
    for url in beatmap_link_list:
        webbrowser.open_new_tab(url)
        time.sleep(interval)
