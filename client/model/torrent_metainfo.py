from dataclasses import dataclass
import json
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
                 info : TorrentInfo,
                 ):
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


class TorrentDownloadInfo:
    def __init__(self,
                 file_path : str,
                 torrent_path:str,
                 piece_length : str ,
                 downloaded_pieces : list[tuple[int,int]],
                 remaining_pieces  : list[tuple[int,int]],
                 ):
        self.file_path = file_path
        self.torrent_path = torrent_path
        self.piece_length = piece_length

        self.downloaded_pieces_bytes  : list[tuple[int,bytes]]= []
        for tuple_ in downloaded_pieces:
            num_bytes = (tuple_[1].bit_length() + 7) // 8 
            # Encode the integer to bytes 
            byte_data = tuple_[1].to_bytes(num_bytes, byteorder='big')
            self.downloaded_pieces_bytes.append((tuple_[0],byte_data))

        self.remaining_pieces_bytes  : list[tuple[int,bytes]]= []
        for tuple_ in remaining_pieces:
            num_bytes = (tuple_[1].bit_length() + 7) // 8 
            # Encode the integer to bytes 
            byte_data = tuple_[1].to_bytes(num_bytes, byteorder='big')
            self.remaining_pieces_bytes.append((tuple_[0],byte_data))
        
    def save_as_json(self,path : str):
        downloaded_pieces_int  : list[tuple[int,int]]= []
        for tuple_ in self.downloaded_pieces_bytes:
            
            int_data = int.from_bytes(tuple_[1], byteorder= 'big')
            downloaded_pieces_int.append((tuple_[0],int_data))

        remaining_pieces_int  : list[tuple[int,int]]= []
        for tuple_ in self.downloaded_pieces_bytes:
            int_data = int.from_bytes(tuple_[1], byteorder= 'big')
            remaining_pieces_int.append((tuple_[0],int_data))

        download_metainfo  = {
            "file path" :  self.file_path,
            "torrent path" : self.torrent_path ,
            "piece length" :  self.piece_length,
            "downloaded pieces" : downloaded_pieces_int,
            "remaining pieces" : remaining_pieces_int,
        }
        with open(path, "w") as outfile:
            json.dump(download_metainfo, outfile, indent=4)  # Save with pretty-printing
