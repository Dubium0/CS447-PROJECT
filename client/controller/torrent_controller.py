from ..model.torrent_model import TorrentModel
from ..view.torrent_view import TorrentView
from ..model.torrent_metainfo import TorrentMetainfo,TorrentViewInfo
from ..view.torrent_popup import TorrentPopup

from . import torrent_loader_saver
from bittorrent_implementation.metainfo import create_torrent_metainfo

import os
from pathlib import Path
import requests
class TorrentController:
    def __init__(self):
        self.model = TorrentModel()
        self.view  = TorrentView(self)
        self.port = 50000
        self.download_threads = []
  
    def run(self):
        self.view.mainloop()

    def create_torrent(self, src_path, torrent_dest, download_dest_path = None):
        file_name = os.path.splitext(os.path.basename(src_path))[0]
        dest_path = str(Path(torrent_dest) / (file_name + '.torrent'))

        create_torrent_metainfo(
            file_path=src_path,
            output_path=dest_path,
            announce_url="http://cs447-ozu-torrent-tracker-server.francecentral.cloudapp.azure.com:6881/announce"
        )

        print(f"Torrent file created: {dest_path}")

        torrent_metainfo = torrent_loader_saver.createTorrentMetainfoFromFile(dest_path)
        print("Adding torrent...")
        self.model.add_torrent(torrent_metainfo, download_dest_path)

        self.update_torrent_view(self.model.get_torrent_view_list())

    def add_torrent(self,metainfo :TorrentMetainfo,output_dir_path : str):
        print("Adding torrent...")
        self.model.add_torrent(metainfo, output_dir_path)
    
        self.update_torrent_view( self.model.get_torrent_view_list())


    def remove_torrent(self, torrent_to_remove : TorrentMetainfo ):
        self.model.remove_torrent(torrent_to_remove)
        self.update_torrent_view( self.model.get_torrent_view_list())

    def get_torrent_by_name(self, torrent_name : str):
        return self.model.get_torrent_by_name(torrent_name)

    def update_torrent_view(self, torrent_view_list : list[TorrentViewInfo]):
        self.view.update_torrent_list(torrent_view_list)

    @staticmethod
    def getMetaInfoFile(file_path :str) ->TorrentMetainfo:
        return torrent_loader_saver.createTorrentMetainfoFromFile(file_path)

    def show_torrent_options(self, item):
        popup = TorrentPopup(self.view, item,self)
        popup.show_popup()


    def get_next_port(self) ->int:
        self.port +=1
        return self.port
    def get_public_ip(self):
        try:
            # Use a service to get the public IP address
            response = requests.get('https://api.ipify.org?format=json')
            
            # Parse the JSON response
            ip_data = response.json()
            
            # Return the public IP address
            return ip_data['ip']
        except Exception as e:
            return f"Error: {e}"
   