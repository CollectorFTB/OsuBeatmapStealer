import os


def main():
    # get path
    path = os.getcwd()
    # split into directories
    dirs = path.split('\\')
    i = 0
    # find the current dir
    for i in range(len(dirs)):
        if dirs[i] == 'OsuBeatmapStealer':
            break
    # stop it right there
    dirs = dirs[:i]
    # create the path again
    new_path = '\\'.join(dirs)
    # go into osu dir
    new_path = os.path.join(new_path, 'osu!')
    print(new_path)
    # input("write something to close")


if __name__ == "__main__":
    main()
