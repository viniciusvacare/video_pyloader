import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from ttkthemes import ThemedTk
from pytube import YouTube
import os

def download_video(url, path, file_format):
    try:
        yt = YouTube(url)
        if file_format == 'mp3':
            audio_stream = yt.streams.filter(only_audio=True).first()
            out_file = audio_stream.download(output_path=path)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
        elif file_format == 'mp4':
            video_stream = yt.streams.get_highest_resolution()
            video_stream.download(output_path=path)
        messagebox.showinfo("Success", f"Downloaded {yt.title} successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video. Error: {str(e)}")

def browse_path():
    download_path = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, download_path)

def start_download():
    url = url_entry.get()
    path = path_entry.get()
    file_format = format_var.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter the YouTube URL")
        return
    if not path:
        messagebox.showwarning("Input Error", "Please select a download path")
        return
    download_video(url, path, file_format)

# Configuração da Interface Gráfica com ThemedTk
app = ThemedTk(theme="arc")
app.title("YouTube Video Downloader")
app.geometry("470x200")
app.resizable(False, False)

style = ttk.Style()
style.configure('TLabel', font=('Arial', 12))
style.configure('TButton', font=('Arial', 12))

ttk.Label(app, text="YouTube URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = ttk.Entry(app, width=40)
url_entry.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

ttk.Label(app, text="Download Path:").grid(row=1, column=0, padx=10, pady=10)
path_entry = ttk.Entry(app, width=30)
path_entry.grid(row=1, column=1, padx=10, pady=10)
ttk.Button(app, text="Browse", command=browse_path).grid(row=1, column=2, padx=10, pady=10)

ttk.Label(app, text="Format:").grid(row=2, column=0, padx=10, pady=10)
format_var = tk.StringVar(value="mp4")
ttk.Radiobutton(app, text="MP3", variable=format_var, value="mp3").grid(row=2, column=1, padx=10, pady=10)
ttk.Radiobutton(app, text="MP4", variable=format_var, value="mp4").grid(row=2, column=2, padx=10, pady=10)

ttk.Button(app, text="Download", command=start_download).grid(row=3, column=1, padx=10, pady=20, columnspan=2)

app.mainloop()
