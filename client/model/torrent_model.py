from .torrent_metainfo import TorrentMetainfo, TorrentViewInfo,TorrentDownloadInfo

import json
import math
class TorrentModel:

    def __init__(self):
        self.torrent_list = [] #pair is TorrentMetafile and current path to download location


    def add_torrent(self,torrent: TorrentMetainfo, path_to_download_location : str):
        self.torrent_list.append({"Metainfo":torrent, "Download Info path":path_to_download_location})


    def remove_torrent(self,torrent_to_remove : TorrentMetainfo):
        for pair in  self.torrent_list:
            if pair["Metainfo"] is torrent_to_remove:
                self.torrent_list.remove(pair)
                break
    def get_torrent_by_name(self, name):
       
        for pair in self.torrent_list:
            metainfo : TorrentMetainfo = pair["Metainfo"]
            if metainfo.info.name == name:
                return metainfo
        return None
    def get_torrent_plus_download_info_by_name(self,name: str):
        
        for pair in self.torrent_list:
            metainfo : TorrentMetainfo = pair["Metainfo"]
            if metainfo.info.name == name:
                downloadInfoPath  = pair["Download Info path"]
                download_info : TorrentDownloadInfo = self.get_torrent_download_info(downloadInfoPath)
                return (metainfo, download_info)
        return None
    def update_torrent_plus_download_info_by_name(self,name: str, newInfo: TorrentDownloadInfo):
        
        for pair in self.torrent_list:
            metainfo : TorrentMetainfo = pair["Metainfo"]

            if metainfo.info.name == name:
               newInfo.save_as_json(pair["Download Info path"])
        return None
    

    def get_torrent_view_list(self):
        result_list = []
        for pair in self.torrent_list:
            metainfo : TorrentMetainfo = pair["Metainfo"]
            downloadInfoPath  = pair["Download Info path"]
            download_info : TorrentDownloadInfo = self.get_torrent_download_info(downloadInfoPath)
            total_numbe_of_pieces = math.ceil(metainfo.info.lenght / metainfo.info.piece_length)
            view_info = TorrentViewInfo( 
                                    original= metainfo,
                                    name = metainfo.info.name,
                                    download_speed = "0",
                                    upload_speed = "0",
                                    completion = f"{len(download_info.downloaded_pieces_bytes)}/{total_numbe_of_pieces}",
                                    status= "PENDING")
            result_list.append ( view_info) 
        return result_list
    
    def get_torrent_download_info(self,download_info_path : str) -> TorrentDownloadInfo:
        with open(download_info_path, 'r') as file: 
            data = json.load(file) 
            download_info :TorrentDownloadInfo = TorrentDownloadInfo(
                data["file path"],
                data["torrent path"],
                data["piece length"],
                [] if data["downloaded pieces"] == None else data["downloaded pieces"],
                [] if data["remaining pieces"] == None else data["remaining pieces"])
            return download_info