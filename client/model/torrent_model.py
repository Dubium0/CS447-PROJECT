

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
                 created_by : str ):
        print("damn")


    def createTorrentModelFromFile(filePath :str):
        print("damn")
     #'announce': announce_url, 
     #  'creation date': int(time.time()), 
     #  'created by': creator_name, 
     #  'info': { 
     #      'piece length': piece_length, 
     #      'name': os.path.basename(file_path), 
     #      'length': os.path.getsize(file_path), 
     #      'pieces': b''
     #  }

