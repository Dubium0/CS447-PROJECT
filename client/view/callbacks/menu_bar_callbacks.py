from tkinter import filedialog, messagebox

class MenuBarCallbacks:
    @staticmethod
    def add_torrent():
        file_path = filedialog.askopenfilename(
            title='Select a torrent file',
            filetypes=[("Torrent Files", "*.torrent"), ("All Files", "*.*")]
        )
        
        if file_path:
            messagebox.showinfo("Torrent Selected", f"Selected file: {file_path}")
            

        else:
            messagebox.showerror("No File Selected", "Please select a torrent file.")

    @staticmethod
    def show_about():
        messagebox.showinfo("About", "CS 447 Torrent Client\nVersion 1.0")
