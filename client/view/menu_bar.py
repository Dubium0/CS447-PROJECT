import tkinter as tk
from tkinter import filedialog, messagebox
from .torrent_load_popup import TorrentLoadPopup

from ..model.torrent_metainfo import TorrentMetainfo, TorrentInfo
class MenuBar:
    def __init__(self, parent, controller ):
        self.parent = parent
        self.controller = controller
        self.menu_bar = tk.Menu(self.parent)
        self.parent.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Create Torrent", command=self.create_torrent)
        file_menu.add_command(label="Add Torrent", command = self.add_torrent )
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

    def create_torrent(self):
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[("All Files", "*.*")]
        )

        if file_path:
            destination_path = filedialog.askdirectory(
                title="Select Torrent Destination Folder"
            )

            if not destination_path:
                messagebox.showwarning("No Destination Selected", "Please select a destination folder.")
                return

            download_dest_path = filedialog.askdirectory(
                title="Select Download Destination Folder"
            )

            if not download_dest_path:
                messagebox.showwarning("No Destination Selected", "Please select a destination folder.")
                return

            try:
                torrent_metainfo = self.controller.create_torrent(file_path, destination_path, download_dest_path)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        else:
            messagebox.showwarning("No File Selected", "Please select a file to create the torrent.")


    def add_torrent(self):
        file_path = filedialog.askopenfilename(
            title='Select a torrent file',
            filetypes=[("Torrent Files", "*.torrent"), ("All Files", "*.*")]
        )

        if file_path:
            metainfo_file : TorrentMetainfo = self.controller.getMetaInfoFile(file_path)


            popup = TorrentLoadPopup(self.parent,name = metainfo_file.info.name,
                                     creation_date= metainfo_file.creation_date,
                                     creator= metainfo_file.created_by,
                                     file_size= metainfo_file.info.lenght)

            popup.on_ok_callback = lambda : self.controller.add_torrent(metainfo_file, popup.selected_dir,file_path)
            popup.on_cancel_callback = lambda : messagebox.showinfo("Canceled", "Torrent Load Operation Canceled")
            popup.show()

        else:
            messagebox.showerror("No File Selected", "Please select a torrent file.")

    def show_about(self):
         messagebox.showinfo("About", "CS 447 Torrent Client\nVersion 1.0")