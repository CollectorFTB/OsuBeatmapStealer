@echo off
pip install -r requirements.txt
del dist\main.exe 
pyinstaller.exe -y -F main.py
del main.spec