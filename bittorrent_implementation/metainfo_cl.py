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
if __name__ == "__main__": 
    decode()