from steal import steal, create_steal_file
from download import download_beatmaps
from path_helper import get_path
from os.path import join, splitext
from logging import exception, basicConfig, DEBUG
from tkinter.filedialog import askdirectory, asksaveasfilename, askopenfilename
from tkinter.messagebox import askyesno, showinfo, showerror
from tkinter import Tk, Button, Label, Entry, W, E, S, N, END, Checkbutton, BooleanVar
from requests.exceptions import ConnectionError
from functools import wraps


def force_txt_ext(file_path):
    file_path,  _ = splitext(file_path)
    return file_path + ".txt"


def check_path(file_path):
    """Cancels program run if path wa s not entered"""
    return not file_path == ''


class StealerApp:
    def __init__(self):
        self.initial_dir = get_path()
        self.root = Tk(className="Osu! Utility Program")
        row_names = ["title_row", "dir_row", "check_row", "delete_low_row", "delete_high_row", "button_row"]  # for maintainability
        rows = {row: index for index, row in enumerate(row_names)}
        Label(master=self.root, text="Osu! Map Tool", font=("Verdana", 18)).grid(row=rows["title_row"], column=0, columnspan=3, sticky=W + E)

        Label(master=self.root, text="Osu! songs folder:").grid(row=rows["dir_row"], sticky=W)
        self._dir_entry = Entry(master=self.root)
        self._dir_entry.grid(row=rows["dir_row"], column=1)
        Button(self.root, text="Browse...", command=self.select_dir).grid(row=rows["dir_row"], column=2, sticky=W)

        Button(master=self.root, text="Create a shareable beatmap file",
               command=self.create_steal_file).grid(row=rows["button_row"], column=0)
        Button(master=self.root, text="Download from file", command=self.steal_beatmaps).grid(row=rows["button_row"], column=1)
        Button(master=self.root, text="Just Delete", command=self.delete_maps).grid(row=rows["button_row"], column=2)

        Label(master=self.root, text="Download flags:").grid(row=rows["check_row"], column=0, sticky=W)
        self._download_video = BooleanVar(master=self.root, value=False)
        Checkbutton(master=self.root, text="noVid",
                    variable=self._download_video, onvalue=False, offvalue=True).grid(row=rows["check_row"], column=1, sticky=W)
        self.apply_all_beatmaps = BooleanVar(master=self.root, value=True)
        Checkbutton(master=self.root, text="Apply For ALL beatmaps (including already existing ones)",
                    variable=self.apply_all_beatmaps, onvalue=False, offvalue=True).grid(row=rows["check_row"], column=2, sticky=W)

        Label(master=self.root, text="Delete Songs Below (can leave as blank):").grid(row=rows["delete_low_row"], column=0, sticky=W)
        self.low_star_entry = Entry(master=self.root)
        self.low_star_entry.grid(row=rows["delete_low_row"], column=1)

        Label(master=self.root, text="Delete Songs Above (can leave as blank):").grid(row=rows["delete_high_row"], column=0, sticky=W)
        self.high_star_entry = Entry(master=self.root)
        self.high_star_entry.grid(row=rows["delete_high_row"], column=1)

    @property
    def download_video(self):
        return self._download_video.get()

    def needs_songs_dir(fun):
        @wraps(fun)
        def songs_dir_checked_function(self, *args, **kwargs):
            if check_path(self.songs_dir):
                return fun(self, *args, **kwargs)
            else:
                showinfo(parent=self.root,
                         message="Please enter your osu song folder first!")
        return songs_dir_checked_function

    @property
    def songs_dir(self):
        return self._dir_entry.get()

    @songs_dir.setter
    def songs_dir(self, value):
        self._dir_entry.delete(0, END)
        self._dir_entry.insert(0, value)

    def run(self):
        self.root.mainloop()

    def select_dir(self):
        self.songs_dir = askdirectory(title="Osu! Songs Folder", initialdir=self.initial_dir)

    @needs_songs_dir
    def create_steal_file(self):
        showinfo(parent=self.root, title="File select",
                 message="Select where to save the beatmap file")
        beatmap_file_path = asksaveasfilename(parent=self.root, filetypes=[("Txt File", "*.txt")],
                                              initialdir=self.initial_dir, title="Your beatmap file", initialfile="beatmaps.txt")
        beatmap_file_path = force_txt_ext(beatmap_file_path)
        if check_path(beatmap_file_path):
            create_steal_file(beatmap_file_path, self.songs_dir)
            showinfo(parent=self.root, title="Done!",
                     message="Finished creating sharable beatmap file, the file should be waiting for you after you close this window\nGive this to other people for them to download your beatmaps!")
            self.root.quit()

    @needs_songs_dir
    def steal_beatmaps(self):
        showinfo(parent=self.root, title="beatmap file",
                 message="Please select the file you want to steal from")
        other_beatmap = askopenfilename(parent=self.root, title="Beatmap file to steal from",
                                        initialdir=self.initial_dir, filetypes=[("Txt File", "*.txt")])
        if check_path(other_beatmap):
            my_beatmaps = steal(self.songs_dir)
            try:
                download_beatmaps(my_beatmaps, other_beatmap, self.songs_dir, self.download_video)
            except ConnectionError:
                showinfo(parent=self.root, title="No internet",
                         message="It seems like you aren't connected to the Internet.\nPlease connect and try again")
                self.root.quit()
            else:
                showinfo(parent=self.root, title="Done!",
                         message="Finished downloading the beatmaps you didn't already have!")
                self.root.destroy()

    @needs_songs_dir
    def delete_maps(self):
        low = self.low_star_entry.get()
        high = self.high_star_entry.get()
        if askyesno(parent=self.root, title="Confirmation", message="Are you sure you want to delete all maps below " + str(low) + " and above " + str(high) + "?"):
            pass


def main():
    print("~~ https://github.com/CollectorFTB/OsuBeatmapStealer ~~")
    app = StealerApp()
    app.run()

if __name__ == "__main__":
    path = get_path()
    log_path = join(path, 'error_log.txt')
    basicConfig(filename=log_path, level=DEBUG)
    try:
        main()
    except Exception as e:
        root = Tk()
        root.withdraw()
        showerror(parent=root, title="ERROR", message="Unexpected Error\nPlease send the created errorlog.txt file through discord to Collector(#5029) or send it to gilad.david95@gmail.com")
        exception(str(e))
        raise
