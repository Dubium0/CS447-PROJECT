from ..model.torrent_model import TorrentModel
from ..view.torrent_view import TorrentView
from ..model.torrent_metainfo import TorrentMetainfo,TorrentViewInfo
from ..view.torrent_popup import TorrentPopup

from . import torrent_loader_saver
from bittorrent_implementation.metainfo import create_torrent_metainfo,create_download_metainfo

import os
from pathlib import Path
import requests
import threading
import json
import hashlib

from . import p2p  
from . import torrent_download

from ..model.database import Database

class TorrentController:
    def __init__(self):
        self.model = TorrentModel()
        self.view  = TorrentView(self)
        self.port = 50000
        self.download_threads = []
        self.db = Database()
  
    def run(self):
        self.view.mainloop()

    def load_torrents_from_database(self):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT path FROM download_info_locations")
        paths = cursor.fetchall()

        if not paths:
            print("No directories found in the database.")
            return

        for path_tuple in paths:
            file_path = path_tuple[0]

            # Validate that the path exists and is a file
            if not os.path.isfile(file_path):
                print(f"Invalid file path in database: {file_path}")
                continue

            try:
                # Load the download info from the file
                with open(file_path, "r") as file:
                    download_info = json.load(file)

                torrent_path = download_info.get("torrent path")
                if not torrent_path or not os.path.exists(torrent_path):
                    print(f"Torrent file not found: {torrent_path}")
                    continue

                # Load TorrentMetainfo
                torrent_metainfo = torrent_loader_saver.createTorrentMetainfoFromFile(torrent_path)
                output_dir_path = os.path.dirname(file_path)

                # Call add_torrent
                self.add_torrent(
                    metainfo=torrent_metainfo,
                    output_dir_path=output_dir_path,
                    torrent_src_path=torrent_path
                )
                print(f"Torrent added successfully: {torrent_path}")

            except Exception as e:
                print(f"Error processing {file_path}: {e}")

        conn.close()

    def create_torrent(self, src_path, torrent_dest, download_dest_path = None):
        file_name = os.path.splitext(os.path.basename(src_path))[0]
        dest_path = str(Path(torrent_dest) / (file_name + '.torrent'))

        create_torrent_metainfo(
            file_path=src_path,
            output_path=dest_path,
            announce_url="http://cs447-ozu-torrent-tracker-server.francecentral.cloudapp.azure.com:6881/announce"
        )

        print(f"Torrent file created: {dest_path}")

        torrent_metainfo = torrent_loader_saver.createTorrentMetainfoFromFile(dest_path)
        self.add_torrent(torrent_metainfo,download_dest_path, dest_path, has_file=1,existing_file_path =src_path)

    def add_torrent(self,metainfo :TorrentMetainfo,output_dir_path : str, torrent_src_path :str, has_file=0,existing_file_path =""):

        # download_info_path = None
        # # Iterate through files in the directory
        # for filename in os.listdir(output_dir_path):
        #     # Check if the file has a .json extension
        #     if filename.endswith(".json"):
        #         # Split the filename by '_'
        #         parts = filename.split("_")
        #
        #         # Check if the second index is "downloadInfo"
        #         if len(parts) > 1 and parts[1] == "downloadMetaInfo":
        #             print(f"File '{filename}' matches the criteria.")
        #
        #             # Construct the full file path
        #             download_info_path = os.path.join(output_dir_path, filename)
        #
        #         else:
        #             print(f"File '{filename}' does not match the criteria.")
        #             download_file_path =  self.create_file(output_dir_path,metainfo.info.name, metainfo.info.lenght)
        #             if not download_file_path:
        #                 print("Failed to add torrent")
        #                 return
        #             download_info_path =  create_download_metainfo(output_dir_path,torrent_src_path,download_file_path)
        #             #save downlaod info
        #             if( not download_info_path ):
        #                 print("Failed to add download info")
        #                 os.remove(download_file_path)
        #                 return

        download_info_path = None

        # Iterate through files in the directory
        for filename in os.listdir(output_dir_path):
            if filename.endswith(".json"):
                parts = filename.split("_")
                if len(parts) > 1 and parts[1] == "downloadMetaInfo" and parts[0] == metainfo.info.name:
                    print(f"File '{filename}' matches the criteria.")
                    download_info_path = os.path.join(output_dir_path, filename)
                    break  # Exit loop since we found the desired file

        # If no matching file was found, create new files
        if not download_info_path:
            if has_file:
                download_file_path = existing_file_path
            else:
                download_file_path = self.create_file(output_dir_path, metainfo.info.name, metainfo.info.lenght)
            if not download_file_path:
                print("Failed to create download file.")
                return

            download_info_path = create_download_metainfo(output_dir_path, torrent_src_path, download_file_path,has_file)
            if not download_info_path:
                print("Failed to create download info metadata.")
                os.remove(download_file_path)  # Clean up the created file
                return

        # Validate the final download_info_path
        if not download_info_path:
            raise ValueError("download_info_path is None. Torrent addition failed.")

        print(f"Final download_info_path: {download_info_path}")

        info_hash = hashlib.sha1(metainfo.info.pieces).hexdigest()

        conn = self.db.connect()
        cursor = conn.cursor()

        # Check if the download info path is already in the database
        cursor.execute("SELECT 1 FROM download_info_locations WHERE path = ?", (download_info_path,))
        result = cursor.fetchone()

        if result is None:  # If not present, insert into the database
            cursor.execute("INSERT INTO download_info_locations (path) VALUES (?)", (download_info_path,))
            conn.commit()
            print(f"Added {download_info_path} to the database.")

        # Check if the info_hash is already in the has_file table
        cursor.execute("SELECT 1 FROM has_file WHERE info_hash = ?", (info_hash,))
        result = cursor.fetchone()
        if result is None:  # If not present, insert into the database
            cursor.execute(
                "INSERT INTO has_file (info_hash, has) VALUES (?, ?)",
                (info_hash, has_file)
            )
            print(f"Added info_hash {info_hash} with has = {has_file} to the has_file table.")

        conn.commit()
        
        self.model.add_torrent(metainfo, download_info_path)
        self.update_torrent_view( self.model.get_torrent_view_list())

        conn.close()


    def create_file(self,createDirPath : str, fileName:str, fileSizeInBytes : int ) ->bool:
        if not os.path.exists(createDirPath):
            os.makedirs(createDirPath)
        
        finalDestDir = os.path.join(createDirPath,fileName)
        if os.path.exists(finalDestDir):
            print("A file with same name exists on the path")
            return None

        with open(finalDestDir, 'wb') as f:
            f.seek(fileSizeInBytes - 1)
            f.write(b'\0')  # Write a single null byte at the end to set file size
        print(f"Created empty file '{finalDestDir}' of size {fileSizeInBytes} bytes.")
        return finalDestDir

    def remove_torrent(self, torrent_to_remove : TorrentMetainfo ):
        self.model.remove_torrent(torrent_to_remove)
        self.update_torrent_view( self.model.get_torrent_view_list())

    def get_torrent_by_name(self, torrent_name : str):
        return self.model.get_torrent_by_name(torrent_name)
    
    def get_torrent_and_download_info_by_name (self, torrent_name : str):
        return self.model.get_torrent_plus_download_info_by_name(torrent_name)
    
    def update_torrent_view(self, torrent_view_list : list[TorrentViewInfo]):
        self.view.update_torrent_list(torrent_view_list)

    @staticmethod
    def getMetaInfoFile(file_path :str) ->TorrentMetainfo:
        return torrent_loader_saver.createTorrentMetainfoFromFile(file_path)

    def show_torrent_options(self, item):
        popup = TorrentPopup(self.view, item,self)
        popup.show_popup()

    def update_torrent_download_info_by_name(self, name:str, torrentDownloadInfo):
        self.model.update_torrent_plus_download_info_by_name(name,torrentDownloadInfo)
        self.update_torrent_view( self.model.get_torrent_view_list())


    def get_next_port(self) ->int:
        self.port +=1
        return self.port
    
    def create_torrent_download_thread(self, peers, torrent_name):
        assigner = torrent_download.DownloadJobAssigner(torrent_name,peers,self)
        assigner.start()
        self.download_threads.append({torrent_name,assigner})

   
    def get_public_ip(self):
        try:
            # Use a service to get the public IP address
            response = requests.get('https://api.ipify.org?format=json')
            
            # Parse the JSON response
            ip_data = response.json()
            
            # Return the public IP address
            return ip_data['ip']
        except Exception as e:
            return f"Error: {e}"

    def check_has_file(self, info_hash):
        conn = self.db.connect()
        cursor = conn.cursor()

        try:
            # Query the database for the info_hash
            cursor.execute("SELECT has FROM has_file WHERE info_hash = ?", (info_hash,))
            result = cursor.fetchone()

            if result:
                return result[0]  # Return the 'has' value (0 or 1)
            else:
                print(f"Info hash {info_hash} not found in has_file table.")
                return 0
        except Exception as e:
            print(f"Error checking has_file: {e}")
            return 0
        finally:
            conn.close()

   