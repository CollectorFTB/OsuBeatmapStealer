from steal import steal, create_steal_file
from download import download_beatmaps
from path_helper import get_path
from os.path import join
from logging import exception, basicConfig, DEBUG
from tkinter.filedialog import askdirectory, asksaveasfilename, askopenfilename
from tkinter.messagebox import askyesno, showinfo
from tkinter import Tk
from requests.exceptions import ConnectionError


def main():
    print("~~ https://github.com/CollectorFTB/OsuBeatmapStealer ~~")
    root = Tk()
    root.withdraw()  # Hide ghost window
    initial_dir = get_path()
    showinfo(parent=root, message="Please Select your osu songs folder")
    osu_dir = askdirectory(title="Osu! Songs Folder", initialdir=initial_dir)

    if askyesno(parent=root, title="Mode", message="Create your own beatmap list?"):
        showinfo(parent=root, title="File select",
                 message="Select where to save the beatmap file")
        beatmap_file_path = asksaveasfilename(parent=root, filetypes=[("Txt File", "*.txt")],
                                              initialdir=initial_dir, title="Your beatmap file", initialfile="beatmaps.txt")
        create_steal_file(beatmap_file_path, osu_dir)
        showinfo(parent=root, title="Done!",
                 message="Finished creating beatmaps.txt, the file should be waiting for you after you close this window\nGive this to other people for them to download your beatmaps!")
    elif askyesno(parent=root, title="Mode", message="Steal beatmaps from someone else?"):
        showinfo(parent=root, title="beatmap file",
                 message="Please select the file you want to steal from")
        other_beatmap = askopenfilename(parent=root, title="Beatmap file to steal from", initialdir=initial_dir)
        my_beatmaps = steal(osu_dir)
        try:
            download_beatmaps(my_beatmaps, other_beatmap, osu_dir)
        except ConnectionError:
            showinfo(parent=root, title="No internet",message="It seems like you aren't connected to the Internet.\nPlease connect and try again")
        else:
            showinfo(parent=root, title="Done!",
                    message="Finished downloading the beatmaps you didn't already have!")
    else:
        showinfo(parent=root, title="Done!",
                 message="Didn't do anything. Bye Bye.")


if __name__ == "__main__":
    path = get_path()
    log_path = join(path, 'error_log.txt')
    basicConfig(filename=log_path, level=DEBUG)
    try:
        main()
    except Exception as e:
        exception(str(e))
        raise
