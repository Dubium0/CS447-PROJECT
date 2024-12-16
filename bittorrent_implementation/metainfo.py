import os
import time
import hashlib
import bencode
from utility import Result
# I enforced the piece length to be power of twos because it is recomended
def create_torrent_metainfo(announce_url : str, file_path : str, piece_length_power : int  = 18,creator_name :str = "No Name",output_path : str = "") -> Result: 
    
    if(not os.path.exists(file_path)):
        print(f"{file_path} does not exists!")
        return Result.FAILURE
    
    piece_length = pow(2,piece_length_power) 

    metainfo_raw = { 
        'announce': announce_url, 
        'creation date': int(time.time()), 
        'created by': creator_name, 
        'info': { 
            'piece length': piece_length, 
            'name': os.path.basename(file_path), 
            'length': os.path.getsize(file_path), 
            'pieces': b''
        }
    }
    with open(file_path, 'rb') as byte_stream:
        while True:
            piece = byte_stream.read(piece_length)
            if not piece:
                break
            metainfo_raw['info']['pieces'] += hashlib.sha1(piece).digest()
    metainfo = bencode.encode(metainfo_raw)
    
    if not output_path:
        output_path = file_path
    
    output_path  = file_path + '.torrent'
    with open(output_path, 'wb') as byte_stream: 
        byte_stream.write(metainfo)

    print(f".torrent file created: {output_path}")
    return Result.SUCCESS
