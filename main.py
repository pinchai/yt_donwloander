import yt_dlp

# Download video only
ydl_opts = {
    # 'format': 'bestvideo[height<=1080]',
    'ffmpeg_location': '/opt/homebrew/bin/ffmpeg',
    'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
    'outtmpl': '%(title)s.%(ext)s',  # This keeps the video title as filename
    'merge_output_format': 'mp4',
}
url = 'https://www.youtube.com/watch?v=8oLi5b4w4PQ'
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
