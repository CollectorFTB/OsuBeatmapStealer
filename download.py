from os.path import join
from os import mkdir
from re import search
from tempfile import TemporaryFile
from zipfile import ZipFile
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests import Session, exceptions
from tqdm import tqdm


def change_format(line):
    match = search("(\d+)", line)
    if match:
        return match.group(1)


def download_beatmaps(my_beatmap_numbers, other_beatmaps_path, songs_dir):
    # open up the file for writing
    with open(other_beatmaps_path, 'r') as other_beatmaps_file:
        # get other numbers
        other_beatmap_numbers = {change_format(line) for line in other_beatmaps_file}

    # remove your beatmaps from his list and eliminate duplicates
    other_beatmap_numbers -= my_beatmap_numbers | {None}

    # starts session with osu
    if other_beatmap_numbers:
        osu_session = OsuSession(songs_dir)
        osu_session.download_beatmap_list(other_beatmap_numbers)


class OsuSession:
    def __init__(self, songs_dir):
        self.osu = "https://osu.ppy.sh"
        self.songs_dir = songs_dir
        self.session = Session()
        self._form = {"username": "dummyosu", "password": "rEqUEsts12"}
        self._login()

    def _login(self):
        self.session.get(self._endpoint("home"))  # get XSRF-TOKEN to prove we're not a malicious phishing program
        self.session.post(self._endpoint("session"), data=self.form)

    @property
    def form(self):
        self._refresh_form()
        return self._form

    def _refresh_form(self):
        self._form['_token'] = self.session.cookies['XSRF-TOKEN']

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

    def download_beatmap(self, beatmap_number):
        try:
            download = self.session.get(self._endpoint(
                "beatmapsets", beatmap_number, "download"), stream=True)
            download.raise_for_status()
            with TemporaryFile() as f:
                # TODO: Adjust chunk size
                chunk_size = 128
                beatmap_name = self.attached_file_name(download)
                for chunk in download.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                self.extract_beatmap(f, beatmap_name)
            return beatmap_name
        except exceptions.HTTPError:
            tqdm.write("Beatmap {} does not exist".format(beatmap_number))
        except KeyError:
            tqdm.write("Login expired/failed")
            self._login()
            self.download_beatmap(beatmap_number)
        finally:
            return ''

    def download_beatmap_list(self, beatmap_list):
        with ThreadPoolExecutor() as executor:
            threads = {executor.submit(self.download_beatmap, beatmap): beatmap for beatmap in beatmap_list}
            for thread in tqdm(as_completed(threads), ncols=100,  desc="Downloaded", unit=' Beatmaps', total=len(beatmap_list)):
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
