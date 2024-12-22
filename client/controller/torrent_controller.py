from ..model.torrent_model import TorrentModel
from ..view.torrent_view import TorrentView
from ..model.torrent_metainfo import TorrentMetainfo,TorrentViewInfo

from . import torrent_loader_saver

class TorrentController:
    def __init__(self):
        self.model = TorrentModel()
        self.view  = TorrentView(self)
  
    def run(self):
        self.view.mainloop()


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

 