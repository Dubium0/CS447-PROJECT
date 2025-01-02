from ..model.torrent_model import TorrentModel
from ..view.torrent_view import TorrentView
from ..model.torrent_metainfo import TorrentMetainfo,TorrentViewInfo

from . import torrent_loader_saver
from bittorrent_implementation.metainfo import create_torrent_metainfo

import os
from pathlib import Path

class TorrentController:
    def __init__(self):
        self.model = TorrentModel()
        self.view  = TorrentView(self)
  
    def run(self):
        self.view.mainloop()

    def create_torrent(self, src_path, dest_path):
        file_name = os.path.splitext(os.path.basename(src_path))[0]
        dest_path = str(Path(dest_path) / (file_name + '.torrent'))

        create_torrent_metainfo(
            file_path=src_path,
            output_path=dest_path,
            announce_url="http://cs447-ozu-torrent-tracker-server.francecentral.cloudapp.azure.com:6881/announce"
        )

        print(f"Torrent file created: {dest_path}")

        torrent_metainfo = torrent_loader_saver.createTorrentMetainfoFromFile(dest_path)
        print("Adding torrent...")
        self.model.add_torrent(torrent_metainfo, dest_path)

        self.update_torrent_view(self.model.get_torrent_view_list())

    def add_torrent(self,metainfo :TorrentMetainfo,output_dir_path : str):
        print("Adding torrent...")
        self.model.add_torrent(metainfo, output_dir_path)

        self.update_torrent_view( self.model.get_torrent_view_list())


    def remove_torrent(self, torrent_to_remove : TorrentMetainfo ):
        self.model.remove_torrent(torrent_to_remove)
        self.update_torrent_view( self.model.get_torrent_view_list())


    def update_torrent_view(self, torrent_view_list : list[TorrentViewInfo]):
        self.view.update_torrent_list(torrent_view_list)

    @staticmethod
    def getMetaInfoFile(file_path :str) ->TorrentMetainfo:
        return torrent_loader_saver.createTorrentMetainfoFromFile(file_path)

 