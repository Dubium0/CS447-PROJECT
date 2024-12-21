import tkinter as tk
from tkinter import ttk

from .callbacks.torrent_list_callbacks import TorrentListCallbacks
from .data_objects.torrent_item import TorrentItem

class TorrentList:
    def __init__(self, parent):
        self.parent = parent

        self.tree = ttk.Treeview(
            self.parent,
            columns=("Name", "Download Speed", "Upload Speed", "Completion", "Status"),
            show="headings",
            height=15,
            selectmode="browse"
        )
        self.tree.heading("Name", text="Torrent Name")
        self.tree.heading("Download Speed", text="Download Speed")
        self.tree.heading("Upload Speed", text="Upload Speed")
        self.tree.heading("Completion", text="Completion (%)")
        self.tree.heading("Status", text="Status")

        self.tree.column("Name", width=300)
        self.tree.column("Download Speed", width=120)
        self.tree.column("Upload Speed", width=120)
        self.tree.column("Completion", width=150)
        self.tree.column("Status", width=120)

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.callbacks = TorrentListCallbacks(self.tree)

    def add_torrent(self, torrent: TorrentItem):
        self.callbacks.add_torrent(torrent)

    def remove_selected_torrent(self, ):
        self.callbacks.remove_selected_torrent()

    def get_selected_torrent(self, ):
        return self.callbacks.get_selected_torrent()

    def populate_with_dummy_torrents(self, ):
        self.callbacks.populate_with_dummy_torrents()

