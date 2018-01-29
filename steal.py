from os.path import join
from os import listdir


def is_number(number):
    try:
        int(number)
        return True
    except ValueError:
        return False


def steal(songs_dir):
    songs_dir = join(songs_dir)
    # for each beatmap save the forum number
    beatmap_number_set = {beatmap[:beatmap.find(' ')] for beatmap in listdir(songs_dir)}
    # filter out un-submitted maps that don't have a link
    filter(is_number, beatmap_number_set)
    return beatmap_number_set


def create_steal_file(file_path, songs_dir):
    beatmap_number_set = steal(songs_dir)
    # open up the file for writing
    with open(file_path, 'w') as beatmaps_file:
        # write the links into the file
        for beatmap_number in beatmap_number_set:
            beatmaps_file.write(beatmap_number + '\n')
