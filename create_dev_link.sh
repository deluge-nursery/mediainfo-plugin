#!/bin/bash
cd D:\progrmming\python\mediainfo
mkdir temp
export PYTHONPATH=./temp
C:\Python27\python.exe setup.py build develop --install-dir ./temp
cp ./temp/MediaInfo.egg-link C:\Users\Ido\AppData\Roaming\deluge\/plugins
rm -fr ./temp
