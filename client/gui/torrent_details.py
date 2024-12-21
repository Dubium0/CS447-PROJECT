import tkinter as tk

class TorrentDetails:
    def __init__(self, parent: tk.Frame):
        self.parent = parent

        self.parent.grid_rowconfigure(0, weight=0)
        self.parent.grid_rowconfigure(1, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)

        self.uploading_label = tk.Label(self.parent, text="Uploading Peers", font=("Arial", 12, "bold"))
        self.uploading_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.uploading_peers_listbox = tk.Listbox(self.parent, height=10, selectmode=tk.SINGLE,
                                                  bd=2, relief="solid", font=("Arial", 10), bg="#f4f4f4")
        self.uploading_peers_listbox.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")


        self.downloading_label = tk.Label(self.parent, text="Downloading Peers", font=("Arial", 12, "bold"))
        self.downloading_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.downloading_peers_listbox = tk.Listbox(self.parent, height=10, selectmode=tk.SINGLE,
                                                  bd=2, relief="solid", font=("Arial", 10), bg="#f4f4f4")
        self.downloading_peers_listbox.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")