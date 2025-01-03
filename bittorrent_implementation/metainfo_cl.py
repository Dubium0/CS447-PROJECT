import argparse
import metainfo



def encode(): 
    #announce_url : str, file_path : str, piece_length_power : int  = 18,creator_name :str = "No Name",output_path : str = ""
    parser = argparse.ArgumentParser(description="Encode torrent file") 
    parser.add_argument('--announceUrl', type=str, required=True, help="The URL of the tracker.") 
    parser.add_argument('--filePath', type=str, required=True, help="Path of the file metainfo will generated for") 
    parser.add_argument('--pieceLengthPower', type=int,default=18, required=False, help="Piece length exponent number pow(2,pieceLengthPower) will be result of total piece length") 
    parser.add_argument('--creatorName', type=str, default='NoName',required=False, help="Name of creator") 
    parser.add_argument('--outputPath', type=str, default='',required=False, help="Output file path (including filename)") 
    args = parser.parse_args() 

    print(args)
    if(metainfo.create_torrent_metainfo( announce_url= args.announceUrl, file_path= args.filePath)):
        print("Successfully created!")
    else:
        print("Failed")


def decode(): 
    #announce_url : str, file_path : str, piece_length_power : int  = 18,creator_name :str = "No Name",output_path : str = ""
    parser = argparse.ArgumentParser(description="Decode torrent file") 
   
    parser.add_argument('--filePath', type=str, required=True, help="Path of the file metainfo will generated for")
    args = parser.parse_args() 

    print(args)
    result = metainfo.decode_torrent_metainfo(file_path = args.filePath)
    if(not result):
        print("Failed")
    else:
         print("Successfully decoded!")
         print(result)
import json
from file_write_read_helpers import verify_file_integrity
def download():
      #announce_url : str, file_path : str, piece_length_power : int  = 18,creator_name :str = "No Name",output_path : str = ""
    parser = argparse.ArgumentParser(description="Download torrent file") 
   
    parser.add_argument('--downloadDir', type=str, required=True, help="Path of the download dir")
    parser.add_argument('--torrentPath', type=str, required=True, help="Path of the torrent file")
    parser.add_argument('--downloadItemPath', type=str, required=True, help="Path of the download item path")
    args = parser.parse_args() 

    print(args)
    result = metainfo.create_download_metainfo(download_dir_path =  args.downloadDir, torrent_path= args.torrentPath, download_item_path= args.downloadItemPath )
    if(not result):
        print("Failed")
    else:
         print("Successfully CREATED!")
         print(result)
    
    #integrity verify test
    with open(result, 'r') as file: 
        data = json.load(file) 
    piece_length  = data["piece length"]
    check_pieces_int =  data["remaining pieces"] # it should downloaded pieces in real life, for now this is for test purposes

    check_pieces_bytes = []
    for tuple_ in check_pieces_int:
        num_bytes = (tuple_[1].bit_length() + 7) // 8 
        # Encode the integer to bytes 
        byte_data = tuple_[1].to_bytes(num_bytes, byteorder='big')
        check_pieces_bytes.append((tuple_[0],byte_data))


    corruptedBytes = verify_file_integrity(check_pieces=check_pieces_bytes,piece_length=piece_length,file_to_check_path= args.downloadItemPath)
    print(f"Corrupted bytes (if exists) :{corruptedBytes}")


if __name__ == "__main__": 
    download()