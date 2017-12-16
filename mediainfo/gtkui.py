#
# gtkui.py
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

import gtk

from deluge.log import LOG as log
from deluge.ui.client import client
from deluge.plugins.pluginbase import GtkPluginBase
import deluge.component as component
import deluge.common

from common import get_resource


class MediaInfoDialog(object):
    def __init__(self):
        version = deluge.common.get_version()
        if version < '2.0':
            log.debug('mediainfo: deluge version is "%s". using glade' % version)
            self.glade = gtk.glade.XML(get_resource('mediainfo.glade'))
            self.window = self.glade.get_widget('mediainfoWindow')
            self.buffer = self.glade.get_widget('textviewMediaInfo').get_buffer()
            self.glade.signal_autoconnect({
                'on_close_clicked': self.on_close_clicked
            })
        else:
            log.debug('mediainfo: deluge version is "%s". using Builder' % version)
            self.builder = gtk.Builder()
            self.builder.add_from_file(get_resource('mediainfo.ui'))
            self.window = self.builder.get_object('dlg_mediainfo')
            self.buffer = self.builder.get_object('textviewMediaInfo').get_buffer()
            self.builder.connect_signals(self)
        self.window.set_transient_for(component.get('MainWindow').window)
        self.window.set_title('MediaInfo - Deluge')

    def show(self, media_info):
        log.debug('mediainfo: showing mediainfo')
        self.buffer.set_text(media_info)
        self.window.show()

    def on_close_clicked(self, event=None):
        log.debug('mediainfo: closing mediainfo')
        self.window.destroy()


class GtkUI(GtkPluginBase):
    def enable(self):
        self.files_tab = component.get('TorrentDetails').tabs['Files']

        log.debug('mediainfo: creating menu items')
        self.file_menu = self.files_tab.file_menu
        self.media_info_separator = gtk.SeparatorMenuItem()
        self.media_info_button = gtk.MenuItem(_('MediaInfo'))
        self.file_menu.append(self.media_info_separator)
        self.media_info_separator.show()
        self.media_info_button.connect('activate', self._on_media_info_activate)
        self.file_menu.append(self.media_info_button)
        self.media_info_button.show()
        log.debug('mediainfo: connecting handler')
        self.connector_id = self.file_menu.connect('show', self.on_popup_show)

    def disable(self):
        log.debug('mediainfo: removing menu items')
        if self.media_info_button in self.file_menu.get_children():
            self.file_menu.remove(self.media_info_button)
            self.file_menu.remove(self.media_info_separator)
        self.file_menu.disconnect(self.connector_id)

    def _on_media_info_activate(self, menuitem):
        log.debug('mediainfo: menu button clicked')
        file_index = filter(lambda index: index != -1, self.files_tab.get_selected_files())[0]
        torrent_id = self.files_tab.torrent_id
        self.media_info_dialog = MediaInfoDialog()
        client.mediainfo.get_media_info(torrent_id, file_index).addCallback(self._on_media_info)

    def _on_media_info(self, media_info):
        log.debug('mediainfo got mediainfo data')
        if media_info is not None:
            self.media_info_dialog.show(media_info)

    def on_popup_show(self, widget):
        log.debug('mediainfo: on_popup_show')
        selected = filter(lambda index: index != -1, self.files_tab.get_selected_files())
        if len(selected) > 1:
            log.debug('> 1')
            self.media_info_button.set_sensitive(False)
        else:
            log.debug('<= 1')
            self.media_info_button.set_sensitive(True)
