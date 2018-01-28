from os.path import join
from os import listdir
from path_helper import get_path


def steal(mode):
    file_name = ""
    # stealing from yourself
    if mode == 0:
        file_name = 'beatmaps.txt'
    # stealing for yourself
    elif mode == 1:
        file_name = 'my_beatmaps.txt'

    # get the path for the output and osu dir
    outer_path, inner_path = get_path()

    # create path for the output file
    beatmaps_file_path = join(inner_path, file_name)

    # go into songs dir inside osu dir
    outer_path = join(inner_path, '..', 'osu!', 'Songs')

    # for each beatmap save the forum number
    beatmaps = listdir(outer_path)
    beatmap_number_list = [beatmap[:beatmap.find(' ')] for beatmap in beatmaps]

    # filter out un-submitted maps that don't have a link
    for beatmap_number in beatmap_number_list[:]:
        try:
            int(beatmap_number)
        except ValueError:
            beatmap_number_list.remove(beatmap_number)

    # make into int instead of string
    beatmap_number_list = [int(element) for element in beatmap_number_list]

    # sort the result for faster checking later
    beatmap_number_list = sorted(beatmap_number_list)

    # create links for each of the numbers
    beatmap_link_list = ["https://osu.ppy.sh/s/" + str(beatmap_number) for beatmap_number in beatmap_number_list]

    # open up the file for writing
    with open(beatmaps_file_path, 'w') as beatmaps_file:

        # write the links into the file
        for beatmap_link in beatmap_link_list:
            beatmaps_file.write(beatmap_link + '\n')
