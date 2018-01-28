import os
import tempfile
import zipfile
from os import remove
from os.path import join
from time import sleep
from webbrowser import open_new_tab
import re
from requests import Session

import config
from path_helper import get_path


def download_beatmaps(interval):
    # get path and save it for later
    new_path = get_path()

    # get the paths for both the files
    my_beatmaps_path = join(new_path, 'my_beatmaps.txt')
    other_beatmaps_path = join(new_path, 'beatmaps.txt')

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

    # delete the my_beatmap.txt file cuz you don't need it anymore
    remove(my_beatmaps_path)

    osu_session = Osu_Session(os.join(new_path,"..","osu","Songs")) #TODO:switch to actual song library
    osu_session.download_beatmap_list(other_beatmap_numbers)

class Osu_Session():
    def __init__(self, songs_dir):
        self.osu = "https://osu.ppy.sh"
        self.songs_dir = songs_dir
        self.session = Session()
        self._form = dict(config.DUMMY)
        self._login()

    def _login(self):
        self.session.get(self._endpoint("home")) #get XSRF-TOKEN to prove we're not a malicous phishing program
        pst = self.session.post(self._endpoint("session"),data=self.form)

    @property
    def form(self):
        self._refresh_form()
        return self._form

    def _refresh_form(self):
        self._form['_token'] = self.session.cookies['XSRF-TOKEN']

    def _endpoint(self, *args):
        ret= "/".join([self.osu] + list(args))
        return ret

    @staticmethod
    def attached_file_name(response):
        header = response.headers['Content-Disposition']
        #'attachment;filename="80 Ai Otsuka - Sakuranbo.osz";'
        return re.search("filename=(.*).osz;",header).group(0)
        #'80 Ai Otsuka - Sakuranbo'

    def download_beatmap(self, beatmap_number):
        try:
            download = self.session.get(self._endpoint(
                "beatmapsets", str(beatmap_number), "download"))
            print(download.headers)
            with tempfile.NamedTemporaryFile(suffix=".zip") as f:
                f.write(download.content)
                self.extract_beatmap(f, self.attached_file_name(download))
        except KeyError:
            print("Login expiried/failed")
            self._login()
            self.download_beatmap(beatmap_number)
        finally:
            pass

    def download_beatmap_list(self, beatmap_list):
        for beatmap in beatmap_list:
            download_beatmaps(beatmap)

    def extract_beatmap(self, beatmap_file, beatmap_name):
        zipmap = zipfile.ZipFile(beatmap_file)
        beatmap_dir = os.path.join(self.songs_dir, beatmap_name)
        try:
            os.mkdir(beatmap_dir)
        except FileExistsError:
            print("beatmap already exists")
            raise
        zipmap.extractall(path=beatmap_dir)