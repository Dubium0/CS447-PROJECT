from bittorrent_implementation import metainfo
from bittorrent_implementation.utility import Result
class TorrentInfo:
    def __init__(self, 
                 piece_length : int,
                 name : str, 
                 lenght : int,
                 pieces : bytearray):
        self.piece_length = piece_length
        self.name = name
        self.lenght = lenght
        self.pieces = pieces
    

class TorrentModel: 

    def __init__(self,
                 announce_url : str,
                 creation_date:str,
                 created_by : str ,
                 info : TorrentInfo):
        self.announce_url = announce_url
        self.creation_date = creation_date
        self.created_by = created_by
        self.info = info

    @staticmethod
    def createTorrentModelFromFile(filePath :str):
        decoded_metainfo = metainfo.decode_torrent_metainfo(filePath)
        if(decoded_metainfo == Result.FAILURE ):
            return Result.FAILURE
       # #else successfully created
       #'announce': decoded_data.get('announce'), 
       # 'creation date': decoded_data.get('creation date'),
       # 'created by': decoded_data.get('created by'), 
       # 'info': { 
       #     'piece length': decoded_data.get('info').get('piece length'), 
       #     'name': decoded_data.get('info').get('name'), 
       #     'length':decoded_data.get('info').get('length'), 
       #     'pieces': decoded_data.get('info').get('pieces')
        info = decoded_metainfo['info']
        torrent_info = TorrentInfo(piece_length=info['piece length'],
                                   name = info['name'],
                                   lenght = info['length'],
                                   pieces = info['pieces'])
        torrent_model = TorrentModel(announce_url = decoded_metainfo['announce'],
                                     creation_date= decoded_metainfo['creation date'],
                                     created_by= decoded_metainfo['created by'],
                                     info = torrent_info) 
        return torrent_model      
