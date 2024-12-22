from .torrent_metainfo import TorrentMetainfo, TorrentViewInfo


class TorrentModel:

    def __init__(self):
        self.torrent_list = [] #pair is TorrentMetafile and current path to download location


    def add_torrent(self,torrent: TorrentMetainfo, path_to_download_location : str):
        self.torrent_list.append({"Metainfo":torrent, "Download Location":path_to_download_location})


    def remove_torrent(self,torrent_to_remove : TorrentMetainfo):
        for pair in  self.torrent_list:
            if pair["Metainfo"] is torrent_to_remove:
                self.torrent_list.remove(pair)
                break
    
    def get_torrent_view_list(self):
        result_list = []
        for pair in self.torrent_list:
            metainfo : TorrentMetainfo = pair["Metainfo"]
            view_info = TorrentViewInfo( 
                                    original= metainfo,
                                    name = metainfo.info.name,
                                    download_speed = "0",
                                    upload_speed = "0",
                                    completion = f"0/1",
                                    status= "PENDING")
            result_list.append ( view_info) 
        return result_list