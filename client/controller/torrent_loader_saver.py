from bittorrent_implementation import metainfo
from bittorrent_implementation.utility import Result
from ..model.torrent_metainfo import TorrentInfo,TorrentMetainfo


def createTorrentMetainfoFromFile(filePath :str):
    decoded_metainfo = metainfo.decode_torrent_metainfo(filePath)
    if(decoded_metainfo == Result.FAILURE ):
        return Result.FAILURE

    info = decoded_metainfo['info']
    torrent_info = TorrentInfo(piece_length=info['piece length'],
                                name = info['name'],
                                lenght = info['length'],
                                pieces = info['pieces'])
    torrent_metainfo= TorrentMetainfo(announce_url = decoded_metainfo['announce'],
                                    creation_date= decoded_metainfo['creation date'],
                                    created_by= decoded_metainfo['created by'],
                                    info = torrent_info) 
    return torrent_metainfo      

