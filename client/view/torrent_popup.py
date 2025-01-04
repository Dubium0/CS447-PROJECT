from tkinter import Toplevel
import tkinter as tk
import requests
import hashlib
import random
import math
class TorrentPopup:
    def __init__(self, parent, item, controller):
        self.parent = parent
        self.item = item
        self.controller = controller

    def create_popup(self):
        # Create the popup window
        self.popup = Toplevel(self.parent)
        self.popup.title("Torrent Options")
        self.popup.geometry('300x200')
        # Create a label to show the torrent name
        label = tk.Label(self.popup, text=f"Torrent: X", font=("Arial", 14))
        label.pack(pady=20)
        # Create the Start button which will trigger the download function
        start_button = tk.Button(self.popup, text="Start Download",command=self.announce)
        start_button.pack(pady=10)




    def show_popup(self):
        self.create_popup()
      


    def announce(self):

        # URL to fetch data from
        url = self.item.announce_url
        info_hash = hashlib.sha1(self.item.info.pieces).hexdigest()


        port = self.controller.get_next_port()
        ip = self.controller.get_public_ip()
        params = {
        'info_hash': info_hash,
        'peer_id': random.randint(1, 2**28-1),
        'ip': ip,
        'port': port,
       
        }
        # Send the GET request
        response = requests.get(url, params=params)
        peers :str = response.json()['peers']
       
        self.controller.create_torrent_download_thread(peers,self.item.info.name)
        print(response.json())
        # Check if the request was successful
       
