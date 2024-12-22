import tkinter as tk


from .menu_bar import MenuBar
from .torrent_details import TorrentDetails
from .torrent_list import TorrentList
from ..model.torrent_metainfo import TorrentViewInfo

class TorrentView(tk.Tk):
    def __init__(self, controller ):
        
        super().__init__()
        self.title("CS447-PROJECT: OzU Torrent")
        self.geometry("600x400")
        self.controller = controller


        self.resizable(True, True)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_menu_bar = MenuBar(self,controller=controller)

        
        self.torrent_frame = tk.Frame(self)
        self.torrent_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.torrent_frame.pack_propagate(False)
        self.torrent_list = TorrentList(self.torrent_frame,controller)

        self.detail_frame = tk.Frame(self)
        self.detail_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.detail_frame.pack_propagate(False)
        self.torrent_details = TorrentDetails(self.detail_frame)


    def update_torrent_list(self, torrent_list):
        self.torrent_list.redraw_torrent_list(torrent_list)