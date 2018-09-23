from os.path import join
from os import mkdir
from re import search
from tempfile import TemporaryFile
from zipfile import ZipFile
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests import Session, HTTPError
from tqdm import tqdm
from typing import Type
from auth import Authenticator, LocalAuthenticator, DummyAuthenticator


def change_format(line):
    match = search("(\d+)", line)
    if match:
        return match.group(1)


def download_beatmaps(my_beatmap_numbers, other_beatmaps_path, songs_dir, download_video):
    # open up the file for writing
    with open(other_beatmaps_path, 'r') as other_beatmaps_file:
        # get other numbers
        other_beatmap_numbers = {change_format(line) for line in other_beatmaps_file}

    # remove your beatmaps from his list and eliminate duplicates
    other_beatmap_numbers -= my_beatmap_numbers | {None}

    # starts session with osu
    if other_beatmap_numbers:
        tqdm.write("Starting download...")
        osu_session = OsuSession(songs_dir)
        osu_session.download_beatmap_list(other_beatmap_numbers, download_video)


class OsuSession:
    def __init__(self, songs_dir: str, authenticator_cls: Type[Authenticator] = None):
        self.osu = "https://osu.ppy.sh"
        self.songs_dir = songs_dir
        self.session = Session()
        self._form = {"username": "dummyosu", "password": "rEqUEsts12"}
        self.authenticator = authenticator_cls or DummyAuthenticator(self.session)
        self._login()

    def _login(self):
        self.authenticator.login()

    def _endpoint(self, *args):
        ret = "/".join([self.osu] + list(args))
        return ret

    @staticmethod
    def attached_file_name(response):
        header = response.headers['Content-Disposition']
        # 'attachment;filename="80 Ai Otsuka - Sakuranbo.osz";'
        return search('filename="(.*).osz";', header).group(1)
        # '80 Ai Otsuka - Sakuranbo'

    @staticmethod
    def attached_file_length(response):
        return int(response.headers['Content-Length'])

    def download_beatmap(self, beatmap_number, download_video):
        try:
            download = self.session.get(self._endpoint("beatmapsets", beatmap_number, "download"),
                                        params={"noVideo": int(not download_video)}, stream=True)
            download.raise_for_status()
            with TemporaryFile() as f:
                # TODO: Adjust chunk size
                chunk_size = 128

                beatmap_name = self.attached_file_name(download)
                for chunk in download.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                self.extract_beatmap(f, beatmap_name)
            return beatmap_name
        except HTTPError:
            tqdm.write("Beatmap {} does not exist".format(beatmap_number))
        except KeyError:
            tqdm.write("Login expired/failed")
            self._login()
            self.download_beatmap(beatmap_number, download_video)
        finally:
            return ''

    def download_beatmap_list(self, beatmap_list,  download_video):
        with ThreadPoolExecutor() as executor:
            threads = {executor.submit(self.download_beatmap, beatmap, download_video): beatmap for beatmap in beatmap_list}
            for thread in tqdm(as_completed(threads), ncols=100,  desc="Downloaded", unit=' Beatmap', total=len(beatmap_list)):
                if thread.exception():
                    raise thread.exception()

    def extract_beatmap(self, beatmap_file, beatmap_name):
        zip_map = ZipFile(beatmap_file)
        beatmap_dir = join(self.songs_dir, beatmap_name)
        try:
            mkdir(beatmap_dir)
        except FileExistsError:
            print("beatmap already exists")
            raise
        zip_map.extractall(path=beatmap_dir)
