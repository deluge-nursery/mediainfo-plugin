@echo off
mkdir temp
set PYTHONPATH=.\temp
"C:\Python27\python.exe" setup.py build develop --install-dir .\temp
copy .\temp\mediainfo.egg-link "%appdata%\deluge\plugins"
rmdir  .\temp \s \q
