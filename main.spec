# -*- mode: python -*-
from os.path import join
from logging import exception, basicConfig, DEBUG
from tkinter.filedialog import askdirectory, asksaveasfilename, askopenfilename
from tkinter.messagebox import askyesno, showinfo, showerror
from tkinter import Tk
from requests.exceptions import ConnectionError
from os import listdir
from os.path import dirname
from os import mkdir
from re import search
from tempfile import TemporaryFile
from zipfile import ZipFile
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests import Session, HTTPError
from tqdm import tqdm
from threading import Thread
from shutil import rmtree

block_cipher = None


a = Analysis(['main.py'],
             pathex=['D:\\Program Files\\OsuBeatmapStealer'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main')
