from steal import steal, create_steal_file
from download import download_beatmaps
from path_helper import get_path
from os.path import join
from logging import exception, basicConfig, DEBUG
from tkinter.filedialog import askdirectory, asksaveasfilename, askopenfilename
from tkinter.messagebox import askyesno, showinfo,showerror
from tkinter import Tk,Button,Label,Entry,W,E,S,N,END,Checkbutton,BooleanVar
from requests.exceptions import ConnectionError
from functools import wraps


def force_txt_ext(file_path):
    return 

def check_path(path):
    """Cancels program run if path was not entered"""
    return not path == ''

class App:
    def __init__(self):
        self.initial_dir = get_path()
        self.root = Tk("Osu! Beatmap Stealer")
        row_names = ["title_row", "dir_row","button_row","check_row"]  # for maintainability
        rows = {row: index for index, row in enumerate(row_names)}

        Label(master=self.root, text="OsuBeatmapStealer", font=("Verdana", 18)).grid(row=rows["title_row"], column=0, columnspan=3, sticky=W + E)

        Label(master=self.root, text="Osu! songs folder:").grid(row=rows["dir_row"], sticky=W)
        self.dir_entry = Entry(master=self.root)
        self.dir_entry.grid(row=rows["dir_row"], column=1)
        Button(self.root, text="Browse...", command=self.select_dir).grid(row=rows["dir_row"], column=2, sticky=E)
        Button(master=self.root, text="Create a shareable beatmap file",
               command=self.create_steal_file).grid(row=rows["button_row"], column=0)
        Button(master=self.root, text="Steal Beatmaps", command=self.steal_beatmaps).grid(row=rows["button_row"], column=1)

        self._download_video = BooleanVar(master=self.root, value=False)
        Checkbutton(master=self.root, text="noVid",
                    variable=self._download_video, onvalue=False, offvalue=True).grid(row=rows["check_row"], sticky=W)
    
    @property
    def download_video(self):
        return self._download_video.get()

    def needs_osu_dir(fun):
        @wraps(fun)
        def osu_dir_checked_function(self, *args, **kwargs):
            if check_path(self.osu_dir):
                return fun(self,*args, **kwargs)
            else:
                showinfo(parent=self.root,
                         message="Please enter your osu song folder first!")
        return osu_dir_checked_function

    @property
    def osu_dir(self):
        return self.dir_entry.get()

    @osu_dir.setter
    def osu_dir(self, value):
        self.dir_entry.delete(0, END)
        self.dir_entry.insert(0, value)

    def run(self):
        self.root.mainloop() #self.root.oddloop() amirite
    
    def select_dir(self):
        self.osu_dir = askdirectory(title="Osu! Songs Folder", initialdir=self.initial_dir)

    @needs_osu_dir
    def create_steal_file(self):
        showinfo(parent=self.root, title="File select",
                 message="Select where to save the beatmap file")
        beatmap_file_path = asksaveasfilename(parent=self.root, filetypes=[("Txt File", "*.txt")],
                                              initialdir=self.initial_dir, title="Your beatmap file", initialfile="beatmaps.txt")
        if check_path(beatmap_file_path):
            create_steal_file(beatmap_file_path, self.osu_dir)
            showinfo(parent=self.root, title="Done!",
                     message="Finished creating sharable beatmap file, the file should be waiting for you after you close this window\nGive this to other people for them to download your beatmaps!")

    @needs_osu_dir
    def steal_beatmaps(self):
        showinfo(parent=self.root, title="beatmap file",
                 message="Please select the file you want to steal from")
        other_beatmap = askopenfilename(parent=self.root, title="Beatmap file to steal from",
                                        initialdir=self.initial_dir, filetypes=[("Txt File", "*.txt")])
        if check_path(other_beatmap):
            my_beatmaps = steal(self.osu_dir)
            try:
                download_beatmaps(my_beatmaps, other_beatmap, self.osu_dir, self.download_video)
            except ConnectionError:
                showinfo(parent=self.root, title="No internet",
                         message="It seems like you aren't connected to the Internet.\nPlease connect and try again")
            else:
                showinfo(parent=self.root, title="Done!",
                         message="Finished downloading the beatmaps you didn't already have!")


def main():
    app = App()
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
        showerror("ERROR","Unexpected Error\nPlease send the created errorlog.txt file through discord to Collector(#5029) or send it to gilad.david95@gmail.com",parent=root)
        exception(str(e))
        raise

