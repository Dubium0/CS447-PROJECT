from tkinter import ttk
from ...model.torrent_metainfo import TorrentMetainfo

class TorrentListCallbacks:
    def __init__(self, tree: ttk.Treeview):
        self.tree = tree

    def add_torrent(self, torrent: TorrentMetainfo):
        self.tree.insert("", "end", values=(
            torrent.name,
            torrent.download_speed,
            torrent.upload_speed,
            torrent.completion_percentage,
            torrent.status
        ))

    def remove_selected_torrent(self):
        selected_item = self.tree.selection()[0]
        if selected_item:
            self.tree.delete(selected_item)

    def get_selected_torrent(self):
        selected_item = self.tree.selection()[0]
        if selected_item:
            return self.tree.item(selected_item)
        return None





