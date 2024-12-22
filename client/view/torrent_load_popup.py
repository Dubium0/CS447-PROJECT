import tkinter as tk
from tkinter import filedialog
import ctypes

class TorrentLoadPopup:
    def __init__(self, parent, name : str = "", creation_date : str ="", creator : str = "", file_size: int = 0 ):
        self.parent = parent
        self.popup = None
        self.entry = None
        self.name_value_label = None
        self.creation_date_value_label = None
        self.creator_value_label = None
        self.file_size_value_label = None

        self.selected_dir = None

        self.name_value = name
        self.creation_date_value = creation_date
        self.creator_value = creator
        self.file_size_value = file_size


        self.on_ok_callback = None
        self.on_cancel_callback = None


       
    def on_ok(self):
        self.selected_dir = self.entry.get()
        if self.selected_dir:
            print(f"Selected Directory: {self.selected_dir}")
        self.popup.destroy()
        if self.on_ok_callback is not None:
            self.on_ok_callback() 
        

    def on_cancel(self):
        print("Operation canceled.")
        self.popup.quit()  # Stop the event loop
        self.popup.destroy()
        if self.on_cancel_callback is not None:
            self.on_cancel_callback()
        

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, directory)

    def update_right_panel(self, name, creation_date, creator, file_size):
        self.name_value_label.config(text=name)
        self.creation_date_value_label.config(text=creation_date)
        self.creator_value_label.config(text=creator)
        self.file_size_value_label.config(text=file_size)

    def enable_dark_mode(self):
        # Enable dark mode for Windows if supported
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
            ctypes.windll.uxtheme.SetPreferredAppMode(1)  # 1 enables dark mode
        except Exception:
            pass

    def create_popup(self):
        self.popup = tk.Toplevel(self.parent)
        self.popup.title("Select Output Directory")
        self.popup.geometry("700x250")
        self.popup.configure(bg="#202020")  # Dark background

        # Configure grid to make the entry resizable
        self.popup.grid_rowconfigure(1, weight=1)
        self.popup.grid_columnconfigure(1, weight=1)

        # Create a section for torrent info
        torrent_info_frame = tk.Frame(self.popup, bg="#2a2a2a")
        torrent_info_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        torrent_info_label = tk.Label(torrent_info_frame, text="Torrent Info", font=("Segoe UI", 12, "bold"), bg="#2a2a2a", fg="#ffffff")
        torrent_info_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        name_label = tk.Label(torrent_info_frame, text="Name:", font=("Segoe UI", 10), bg="#2a2a2a", fg="#ffffff")
        name_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.name_value_label = tk.Label(torrent_info_frame, text=self.name_value, font=("Segoe UI", 10), bg="#2a2a2a", fg="#ffffff")
        self.name_value_label.grid(row=1, column=1, sticky="w", padx=5, pady=2)

        creation_date_label = tk.Label(torrent_info_frame, text="Creation Date:", font=("Segoe UI", 10), bg="#2a2a2a", fg="#ffffff")
        creation_date_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.creation_date_value_label = tk.Label(torrent_info_frame, text=self.creation_date_value, font=("Segoe UI", 10), bg="#2a2a2a", fg="#ffffff")
        self.creation_date_value_label.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        creator_label = tk.Label(torrent_info_frame, text="Creator:", font=("Segoe UI", 10), bg="#2a2a2a", fg="#ffffff")
        creator_label.grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.creator_value_label = tk.Label(torrent_info_frame, text=self.creator_value, font=("Segoe UI", 10), bg="#2a2a2a", fg="#ffffff")
        self.creator_value_label.grid(row=3, column=1, sticky="w", padx=5, pady=2)

        file_size_label = tk.Label(torrent_info_frame, text="File Size:", font=("Segoe UI", 10), bg="#2a2a2a", fg="#ffffff")
        file_size_label.grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.file_size_value_label = tk.Label(torrent_info_frame, text=f"{self.file_size_value}", font=("Segoe UI", 10), bg="#2a2a2a", fg="#ffffff")
        self.file_size_value_label.grid(row=4, column=1, sticky="w", padx=5, pady=2)

        # Create a label
        label = tk.Label(self.popup, text="Output Directory:", font=("Segoe UI", 12), bg="#202020", fg="#ffffff")
        label.grid(row=1, column=0, padx=5, pady=10, sticky="w")

        # Create an entry widget for the directory
        self.entry = tk.Entry(self.popup, font=("Segoe UI", 10), bg="#2a2a2a", fg="#ffffff", insertbackground="#ffffff")
        self.entry.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

        # Create a Browse button
        browse_button = tk.Button(self.popup, text="Browse", font=("Segoe UI", 10), bg="#3a3d41", fg="#ffffff", activebackground="#4a4e53", activeforeground="#ffffff", command=self.browse_directory)
        browse_button.grid(row=1, column=2, padx=5, pady=10)

        # Create OK and Cancel buttons
        button_frame = tk.Frame(self.popup, bg="#202020")
        button_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky="ew")

        ok_button = tk.Button(button_frame, text="OK", font=("Segoe UI", 10), bg="#3a3d41", fg="#ffffff", activebackground="#4a4e53", activeforeground="#ffffff", command=self.on_ok)
        ok_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", font=("Segoe UI", 10), bg="#3a3d41", fg="#ffffff", activebackground="#4a4e53", activeforeground="#ffffff", command=self.on_cancel)
        cancel_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

    def show(self):
        self.enable_dark_mode()
        self.create_popup()


