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
        file_menu.add_command(label="Add Torrent", command = self.add_torrent )
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

    
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
            
            popup.on_ok_callback = lambda : self.controller.add_torrent(metainfo_file, popup.selected_dir)
            popup.on_cancel_callback = lambda : messagebox.showinfo("Canceled", "Torrent Load Operation Canceled")
            popup.show()

        else:
            messagebox.showerror("No File Selected", "Please select a torrent file.")

    def show_about(self):
         messagebox.showinfo("About", "CS 447 Torrent Client\nVersion 1.0")