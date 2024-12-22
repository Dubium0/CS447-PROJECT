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
        'creation date': int(time.time()), ## update to proper date time
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

def decode_torrent_metainfo(file_path : str):
    if(not os.path.exists(file_path)):
        print(f"{file_path} does not exists!")
        return Result.FAILURE
    
    _, file_extension = os.path.splitext(file_path)
    if(file_extension != '.torrent'):
        print(f"{file_extension} is not a torrent file!")
        return Result.FAILURE

    
    decoded_data = bencode.bread(file_path)
    metainfo_raw = { 
        'announce': decoded_data.get('announce'), 
        'creation date': decoded_data.get('creation date'),
        'created by': decoded_data.get('created by'), 
        'info': { 
            'piece length': decoded_data.get('info').get('piece length'), 
            'name': decoded_data.get('info').get('name'), 
            'length':decoded_data.get('info').get('length'), 
            'pieces': decoded_data.get('info').get('pieces')
        }
    }

    return metainfo_raw
     
    

