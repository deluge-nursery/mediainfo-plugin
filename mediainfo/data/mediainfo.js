/*
Script: mediainfo.js
    The client-side javascript code for the MediaInfo plugin.

Copyright:
    (C) DjLegolas 2017 <DjLegolas@users.noreply.github.com>
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3, or (at your option)
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, write to:
        The Free Software Foundation, Inc.,
        51 Franklin Street, Fifth Floor
        Boston, MA  02110-1301, USA.

    In addition, as a special exception, the copyright holders give
    permission to link the code of portions of this program with the OpenSSL
    library.
    You must obey the GNU General Public License in all respects for all of
    the code used other than OpenSSL. If you modify file(s) with this
    exception, you may extend this exception to your version of the file(s),
    but you are not obligated to do so. If you do not wish to do so, delete
    this exception statement from your version. If you delete this exception
    statement from all source files in the program, then also delete it here.
*/

Ext.ns('Deluge.ux');

/**
 * @class Deluge.ux.AddLabelWindow
 * @extends Ext.Window
 */
Deluge.ux.MediaInfoWindow = Ext.extend(Ext.Window, {

    title: _('MediaInfo'),
    width: 600,
    height: 500,
    resizable: false,

    initComponent: function() {
        Deluge.ux.AddLabelWindow.superclass.initComponent.call(this);
        this.addButton(_('Close'), this.onCloseClick, this);

        this.media = this.add({
            xtype: 'textarea',
            height: 438,
            width: 588,
            baseCls: 'x-plain',
            bodyStyle:'padding:5px 5px 0',
            style: {
                overflow: 'scroll'
            },
            readOnly: true,
            hideLabel: true
        });
    },

    onCloseClick: function() {
        this.hide();
    },

    onHide: function(comp) {
        Deluge.ux.MediaInfoWindow.superclass.onHide.call(this, comp);
        this.media.reset();
    },

    show: function (media_info) {
        this.media.setValue(media_info);
        Deluge.ux.MediaInfoWindow.superclass.show.call(this)
    }
});

Ext.ns('Deluge.plugins');

MediaInfoPlugin = Ext.extend(Deluge.Plugin, {

	name: 'MediaInfo',

	constructor: function(config) {
		config = Ext.apply({
			name: "MediaInfo"
		}, config);
		MediaInfoPlugin.superclass.constructor.call(this, config);
	},

	onDisable: function() {
		deluge.menus.filePriorities.remove(this.miSep);
		deluge.menus.filePriorities.remove(this.mi);
	},

	onEnable: function() {
		this.miSep = deluge.menus.filePriorities.add({
            xtype: 'menuseparator'
        });

        this.mi = deluge.menus.filePriorities.add({
			text: _('MediaInfo'),
			listeners: {
				click: this.onMediaInfoClick
			}
		});
	},

    onMediaInfoClick: function () {
        var nodes = deluge.details.activeTab.getSelectionModel().getSelectedNodes();
        if (nodes.length === 1) {
            var torrentId = deluge.details.activeTab.torrentId;
            var fileIndex = nodes[0]['attributes']['fileIndex'];

            console.log('torrentId: ' + torrentId + '\nfileIndex: ' + fileIndex + '\n');

            deluge.client.mediainfo.get_media_info(torrentId, fileIndex, {
                success: function(media_info) {
                    if (!this.mediaInfoWindow) {
                        this.mediaInfoWindow = new Deluge.ux.MediaInfoWindow();
                    }
                    if (media_info !== null) {
                        this.mediaInfoWindow.show(media_info);
                    }
                }
            });
        }
    }
});
Deluge.registerPlugin('MediaInfo', MediaInfoPlugin);
