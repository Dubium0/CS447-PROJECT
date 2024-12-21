import tkinter as tk
from .callbacks.menu_bar_callbacks import MenuBarCallbacks

class MenuBar:
    def __init__(self, parent):
        self.parent = parent

        self.menu_bar = tk.Menu(self.parent)
        self.parent.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Add Torrent", command=MenuBarCallbacks.add_torrent)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=MenuBarCallbacks.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)


