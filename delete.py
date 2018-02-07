from os import listdir
from os.path import join, splitext
from steal import is_number
from os import remove
from shutil import rmtree
from tqdm import tqdm


def delete(songs_dir, game_modes, download_video):
    if not download_video:
        for beatmap in listdir(songs_dir):
            if is_number(beatmap[:beatmap.find(' ')]):
                for file in listdir(join(songs_dir, beatmap)):
                    if splitext(file)[1] in ['.mp4', '.flv', '.avi']:
                        remove(join(songs_dir, beatmap, file))

    modes = ['std', 'taiko', 'ctb', 'mania']
    mode_nums = list()
    for key in game_modes.keys():
        if game_modes[key]:
            mode_nums.append(modes.index(key))

    if mode_nums:
        for beatmap in tqdm(listdir(songs_dir), unit=' Beatmap', ncols=100, desc='Deleting bad maps', total=len(listdir(songs_dir)), mininterval=0.2):
            beatmaps_to_delete = list()
            osu_files = (file for file in listdir(join(songs_dir, beatmap)) if file.endswith('.osu'))
            for file in osu_files:
                try:
                    with open(join(songs_dir, beatmap, file), 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line in ["[Metadata]", "[Editor]"]:
                                break
                            if line[:5] == "Mode:":
                                if int(line[5:]) not in mode_nums:
                                    beatmaps_to_delete.append(join(songs_dir, beatmap, file))
                                break
                except UnicodeDecodeError:
                    pass
            for bad_beatmap in beatmaps_to_delete:
                remove(bad_beatmap)

            if not [1 for file in listdir(join(songs_dir, beatmap)) if splitext(file)[1] == '.osu']:
                rmtree(join(songs_dir, beatmap))






