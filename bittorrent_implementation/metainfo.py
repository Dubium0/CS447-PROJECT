import os
import time
import hashlib
import bencode
from .utility import Result, split_bytes
import uuid
import json
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
        output_path  = file_path + '.torrent'

    with open(output_path, 'wb') as byte_stream: 
        byte_stream.write(metainfo)

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
     

#creates download metainfo file and returns its path
def create_download_metainfo(download_dir_path : str, torrent_path : str, download_item_path : str) -> str:

    if not os.path.isdir(download_dir_path):
        print("Provide directory not file path!")
        return Result.FAILURE

    torrent_meta_info = decode_torrent_metainfo(torrent_path)

    if (torrent_meta_info == Result.FAILURE):
        print("Failed to decode torrent file1")
        return
    
    if not os.path.exists(download_item_path):
        print("Download Item path does not exists!")
        return
    
    torrent_name :str = torrent_meta_info['info']['name']
    torrent_name = ''.join(torrent_name.split('_'))
    name = f"{torrent_name}_downloadMetaInfo_{uuid.uuid4().hex[:5]}.json" #lazy way of dealing duplicates

    final_download_meta_info_file_path = os.path.join(download_dir_path,name)

    byteList =  list(enumerate(list(split_bytes(torrent_meta_info['info']['pieces'],20))))
    download_metainfo  = {
        "file path" : download_item_path,
        "torrent path" : torrent_path,
        "piece length" : int(torrent_meta_info['info']['piece length']),
        "downloaded pieces" : None,
        "remaining pieces" : byteList,
    }
    print(download_metainfo["remaining pieces"])
    # Write JSON data to the file
    with open(final_download_meta_info_file_path, 'w') as file:
        json.dump(download_metainfo, file, indent=4)

    return final_download_meta_info_file_path
