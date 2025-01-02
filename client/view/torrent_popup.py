from tkinter import Toplevel
import tkinter as tk


class TorrentPopup:
    def __init__(self, parent, item):
        self.parent = parent

    def create_popup(self):
        # Create the popup window
        self.popup = Toplevel(self.parent)
        self.popup.title("Torrent Options")
        self.popup.geometry('300x200')
        # Create a label to show the torrent name
        label = tk.Label(self.popup, text=f"Torrent: X", font=("Arial", 14))
        label.pack(pady=20)
        # Create the Start button which will trigger the download function
        start_button = tk.Button(self.popup, text="Start Download",)
        start_button.pack(pady=10)

    def show_popup(self):
        self.create_popup()


