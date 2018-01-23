import os
from path_helper import get_path


def steal(mode):
    file_name = ""
    # stealing from yourself
    if mode == 0:
        file_name = 'beatmaps.txt'
    # stealing for yourself
    elif mode == 1:
        file_name = 'my_beatmaps.txt'

    dirs, i = get_path()
    print(dirs)
    print(os.path.join(*dirs))

    # stop it right there
    out_dirs = dirs[:i + 1]
    dirs = dirs[:i]

    # create the path again
    new_path = os.path.join(*dirs)
    out_path = os.path.join(*out_dirs)

    # go into osu dir
    new_path = os.path.join(new_path, 'osu!')
    beatmaps_file_path = os.path.join(out_path, file_name)

    # add Songs to the path
    new_path = os.path.join(new_path, 'Songs')

    # for each beatmap save the forum number
    beatmaps = os.listdir(new_path)
    beatmap_number_list = [beatmap.split()[0] for beatmap in beatmaps]

    # filter out un-submitted maps that dont have a link
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
