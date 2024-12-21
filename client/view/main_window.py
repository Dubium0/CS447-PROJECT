import tkinter as tk
from .menu_bar import MenuBar
from .torrent_details import TorrentDetails
from .torrent_list import TorrentList

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CS447-PROJECT: OzU Torrent")
        self.root.geometry("1920x1080")
        self.root.resizable(True, True)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.main_menu_bar = MenuBar(self.root)

        self.torrent_frame = tk.Frame(self.root)
        self.torrent_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.torrent_frame.pack_propagate(False)
        self.torrent_list = TorrentList(self.torrent_frame)

        self.detail_frame = tk.Frame(self.root)
        self.detail_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.detail_frame.pack_propagate(False)
        self.torrent_details = TorrentDetails(self.detail_frame)

    def start(self):
        self.root.mainloop()

