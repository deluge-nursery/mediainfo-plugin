#!/bin/bash
BUILD_DIRECTORY="/tmp/build_mediainfo-plugin_$(date +%s)"
mkdir -p $BUILD_DIRECTORY
export PYTHONPATH=$BUILD_DIRECTORY
env python2 setup.py build develop --install-dir $BUILD_DIRECTORY/
cp $BUILD_DIRECTORY/MediaInfo.egg-link ~/.config/deluge/plugins
rm -rf $BUILD_DIRECTORY

