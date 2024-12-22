from dataclasses import dataclass

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
    

class TorrentMetainfo: 

    def __init__(self,
                 announce_url : str,
                 creation_date:str,
                 created_by : str ,
                 info : TorrentInfo):
        self.announce_url = announce_url
        self.creation_date = creation_date
        self.created_by = created_by
        self.info = info


#  self.tree.column("Name", width=300)
#   self.tree.column("Download Speed", width=120)
#   self.tree.column("Upload Speed", width=120)
#   self.tree.column("Completion", width=150)
#   self.tree.column("Status", width=120)
@dataclass
class TorrentViewInfo:
    original: TorrentMetainfo
    name :str
    download_speed : str
    upload_speed :str
    completion : str
    status : str