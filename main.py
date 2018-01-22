import os


def main():
    # get path and save it for later
    path = os.getcwd()
    beatmaps_file_path = os.path.join(path, 'beatmaps.txt')

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
    beatmap_number_list = list()
    for beatmap in beatmaps:
        beatmap_details = beatmap.split(' ')
        beatmap_number = beatmap_details[0]
        beatmap_number_list.append(beatmap_number)

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
    beatmap_link_list = list()
    for beatmap_number in beatmap_number_list:
        beatmap_link_list.append("https://osu.ppy.sh/s/"+str(beatmap_number))

    # open up the file for writing
    beatmaps_file = open(beatmaps_file_path, 'w')

    # write the links into the file
    for beatmap_link in beatmap_link_list:
        beatmaps_file.write(beatmap_link+'\n')

    print(beatmap_link_list)
    # input("write something to close")

if __name__ == "__main__":
    main()
