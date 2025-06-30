import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import yt_dlp
import os
import shutil
from get_video_id import get_youtube_video_id

# FFMPEG_PATH = '/opt/homebrew/bin/ffmpeg'
FFMPEG_PATH = shutil.which("ffmpeg")


def download_video(url, output_folder, progress_callback):
    if not os.path.isdir(output_folder):
        progress_callback("Invalid output folder!\n")
        return
    ydl_opts = {
        'ffmpeg_location': FFMPEG_PATH,
        # 'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'format': 'bestaudio/best[height<=1080]',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'progress_hooks': [lambda d: progress_hook(d, progress_callback)],
        'quiet': True,  # suppress console output, we handle in callback
        'noprogress': True,  # don't print progress to stdout
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        progress_callback(f"Error: {e}\n")


def progress_hook(d, progress_callback):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '').strip()
        speed = d.get('_speed_str', '').strip()
        eta = d.get('_eta_str', '').strip()
        msg = f"Downloading: {percent} at {speed}, ETA: {eta}\n"
        progress_callback(msg)
    elif d['status'] == 'finished':
        progress_callback("Download finished, merging files finished...\n")
    elif d['status'] == 'error':
        progress_callback("Download error!\n")


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
    progress_text.delete(1.0, tk.END)  # clear previous logs

    # Thread to keep UI responsive
    threading.Thread(target=run_download, args=(url, output_folder), daemon=True).start()


def run_download(url, output_folder):
    # url = 'https://www.youtube.com/watch?v=8oLi5b4w4PQ'
    # url = 'https://www.youtube.com/watch?v=8oLi5b4w4PQ'
    video_id = get_youtube_video_id(url)
    url = f"https://www.youtube.com/watch?v={video_id}"

    def ui_callback(msg):
        progress_text.insert(tk.END, msg)
        progress_text.see(tk.END)

    download_video(url, output_folder, ui_callback)
    status_label.config(text="Done")
    download_btn.config(state='normal')
    url_entry.delete(0, tk.END)


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

tk.Label(root, text="Download Process:").grid(row=4, column=0, padx=5, pady=(10, 0), sticky='nw')
progress_text = tk.Text(root, height=10, width=60, state='normal')
progress_text.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

root.mainloop()
