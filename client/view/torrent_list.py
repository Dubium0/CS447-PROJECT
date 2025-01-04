import tkinter as tk
from tkinter import ttk

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

        self.tree.bind("<Double-1>", self.on_double_click)

    def remove_children(self):
        """Remove all children of a specific parent node."""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def redraw_torrent_list(self, list_of_torrent : list[TorrentViewInfo]):
        
        self.remove_children()
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

    def on_double_click(self, event):
        selected_item = self.tree.selection()[0]
        self.controller.show_torrent_options(selected_item)


