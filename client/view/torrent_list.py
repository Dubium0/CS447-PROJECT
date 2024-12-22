import tkinter as tk
from tkinter import ttk

from .callbacks.torrent_list_callbacks import TorrentListCallbacks
from ..model.torrent_metainfo import TorrentMetainfo,TorrentViewInfo


class TorrentList:
    def __init__(self, parent,controller):
        self.parent = parent
        self.controller =controller
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

    def redraw_torrent_list(self, list_of_torrent : list[TorrentViewInfo]):
        
        self.tree.children.clear()
        for item in list_of_torrent:
            self.tree.insert("", "end", values=(
                item.name,
                item.download_speed,
                item.upload_speed,
                item.completion,
                item.status
            ))

    def remove_selected_torrent(self ):
        selected_item : TorrentViewInfo = self.tree.selection()[0]
        self.controller.remove_torrent(selected_item.original)

    def get_selected_torrent(self):
        return self.callbacks.get_selected_torrent()


