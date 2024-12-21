from tkinter import ttk
from ..data_objects.torrent_item import TorrentItem

class TorrentListCallbacks:
    def __init__(self, tree: ttk.Treeview):
        self.tree = tree

    def add_torrent(self, torrent: TorrentItem):
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

    def populate_with_dummy_torrents(self):
        dummy_torrents = [
            TorrentItem("Ubuntu ISO", "/path/to/ubuntu.iso", "1.2 MB/s", "500 KB/s", "75%", "Downloading"),
            TorrentItem("Python Docs", "/path/to/python_docs.pdf", "800 KB/s", "300 KB/s", "60%", "Downloading"),
            TorrentItem("Movie Trailer", "/path/to/movie_trailer.mp4", "2 MB/s", "1 MB/s", "90%", "Paused"),
            TorrentItem("Large Dataset", "/path/to/large_dataset.csv", "500 KB/s", "200 KB/s", "40%", "Downloading"),
            TorrentItem("Example Torrent", "/path/to/example.torrent", "1 MB/s", "450 KB/s", "50%", "Completed")
        ]

        for torrent in dummy_torrents:
            self.add_torrent(torrent)





