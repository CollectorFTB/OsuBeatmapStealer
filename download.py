import os
import re
import tempfile
import zipfile
from os import remove
from os.path import join
from time import sleep
from webbrowser import open_new_tab

import concurrent.futures
import requests
from requests import Session
from tqdm import tqdm

import config
from path_helper import get_path


def download_beatmaps(my_beatmap_numbers,other_beatmaps_path,osu_dir):
    # get path and save it for later
    songs_dir = join(osu_dir,"Songs")
    # open up the file for writing
    with open(other_beatmaps_path, 'r') as other_beatmaps_file:
        # get other numbers
        other_beatmap_numbers = {line.strip() for line in other_beatmaps_file}
    # remove your beatmaps from his list and eliminate duplicates
    other_beatmap_numbers -= my_beatmap_numbers
    if other_beatmap_numbers:
        osu_session = Osu_Session(songs_dir) #TODO:switch to actual song library
        osu_session.download_beatmap_list(other_beatmap_numbers)

class Osu_Session():
    def __init__(self, songs_dir):
        self.osu = "https://osu.ppy.sh"
        self.songs_dir = songs_dir
        self.session = Session()
        self._form = {"username":"dummyosu","password":"rEqUEsts12"}
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
        return re.search('filename="(.*).osz";',header).group(1)
        #'80 Ai Otsuka - Sakuranbo'

    @staticmethod
    def attached_file_length(response):
        return int(response.headers['Content-Length'])


    def download_beatmap(self, beatmap_number):
        try:
            download = self.session.get(self._endpoint(
                "beatmapsets", beatmap_number, "download"),stream=True)
            download.raise_for_status()
            with tempfile.TemporaryFile() as f:
                # TODO:Adjust chunck size
                chunck_size = 128
                file_size = self.attached_file_length(download) 
                beatmap_name = self.attached_file_name(download)
                for chunck in download.iter_content(chunk_size=chunck_size):
                    f.write(chunck)
                self.extract_beatmap(f, beatmap_name)
        except requests.exceptions.HTTPError:
            print("Beatmap {} does not exist".format(beatmap_number))
        except KeyError:
            print("Login expiried/failed")
            self._login()
            self.download_beatmap(beatmap_number)
        finally:
            return beatmap_name

    def download_beatmap_list(self, beatmap_list):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_url = {executor.submit(self.download_beatmap, beatmap): beatmap for beatmap in beatmap_list}
            for thread in tqdm(concurrent.futures.as_completed(future_to_url),desc="Downloaded",unit='Beatmaps'):
                print(thread.result())
                if thread.exception():
                    raise thread.exception()

    def extract_beatmap(self, beatmap_file, beatmap_name):
        zipmap = zipfile.ZipFile(beatmap_file)
        beatmap_dir = os.path.join(self.songs_dir, beatmap_name)
        try:
            os.mkdir(beatmap_dir)
        except FileExistsError:
            print("beatmap already exists")
            raise
        zipmap.extractall(path=beatmap_dir)
