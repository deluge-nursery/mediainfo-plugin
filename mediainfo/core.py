#
# core.py
#
# Copyright (C) 2017 DjLegolas <DjLegolas@users.noreply.github.com>
#
# Basic plugin template created by:
# Copyright (C) 2008 Martijn Voncken <mvoncken@gmail.com>
# Copyright (C) 2007-2009 Andrew Resch <andrewresch@gmail.com>
# Copyright (C) 2009 Damien Churchill <damoxc@gmail.com>
#
# Deluge is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.
#

import os

from deluge.log import LOG as log
from deluge.plugins.pluginbase import CorePluginBase
import deluge.component as component
import deluge.configmanager
from deluge.core.rpcserver import export

from MediaInfoDLL import MediaInfo


class Core(CorePluginBase):
    def enable(self):
        self.media_info = MediaInfo()

    def disable(self):
        pass

    def update(self):
        pass

    @export
    def get_media_info(self, torrent_id, file_index):
        """
        Generates the media info for the file.
        :param torrent_id: The Torrent the file belongs to
        :param file_index: The file index to generate the media info for
        :return: MediaInfo string
        """
        log.debug('mediainfo info request for:\nTorrent ID: %s\nFile ID: %s' % (torrent_id, file_index))
        media_file = self._get_torrent_data(torrent_id, file_index)
        self.media_info.Open(media_file)
        info = self.media_info.Inform()
        self.media_info.Close()
        return info

    @staticmethod
    def _get_torrent_data(torrent_id, file_index):
        data = component.get('Core').get_torrent_status(torrent_id, ['save_path', 'files'])
        file_path = filter(lambda file_: file_index == file_['index'], data['files'])
        if len(file_path) != 1:
            log.error('no file index %d' % file_index)
            return None
        file_path = file_path[0]['path']
        log.debug('download path: %s\nfile path: %s',  str(data['save_path']), str(file_path))
        return os.path.join(data['save_path'], file_path)
