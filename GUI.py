import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import yt_dlp
import os

FFMPEG_PATH = '/opt/homebrew/bin/ffmpeg'  # Change to your ffmpeg path

def download_video(url, output_folder):
    if not os.path.isdir(output_folder):
        return "Invalid output folder!"
    ydl_opts = {
        'ffmpeg_location': FFMPEG_PATH,
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return "Download complete!"
    except Exception as e:
        return f"Error: {e}"

def start_download():
    url = url_entry.get()
    output_folder = output_path_var.get()
    if not url.strip():
        messagebox.showwarning("Missing URL", "Please enter a YouTube URL.")
        return
    if not output_folder.strip():
        messagebox.showwarning("Missing Output Folder", "Please select an output folder.")
        return

    status_label.config(text="Downloading...")
    download_btn.config(state='disabled')
    threading.Thread(target=run_download, args=(url, output_folder), daemon=True).start()

def run_download(url, output_folder):
    url = 'https://www.youtube.com/watch?v=WBxdmNgTA2U'
    result = download_video(url, output_folder)
    status_label.config(text=result)
    download_btn.config(state='normal')

def choose_output_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_path_var.set(folder_selected)

# --- Tkinter UI ---
root = tk.Tk()
root.title("YouTube MP4 Downloader")

tk.Label(root, text="YouTube URL:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2)

tk.Label(root, text="Output Folder:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
output_path_var = tk.StringVar()
output_path_entry = tk.Entry(root, textvariable=output_path_var, width=38)
output_path_entry.grid(row=1, column=1, padx=5, pady=5)
browse_btn = tk.Button(root, text="Browse", command=choose_output_folder)
browse_btn.grid(row=1, column=2, padx=5, pady=5)

download_btn = tk.Button(root, text="Download as MP4", command=start_download)
download_btn.grid(row=2, column=0, columnspan=3, pady=10)

status_label = tk.Label(root, text="")
status_label.grid(row=3, column=0, columnspan=3, pady=5)

root.mainloop()
