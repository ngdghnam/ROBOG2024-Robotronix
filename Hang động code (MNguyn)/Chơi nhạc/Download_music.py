from search_song import search_song
import yt_dlp
from youtube_search import YoutubeSearch

YTSearchResult = YoutubeSearch(search_song(), max_results=1).to_dict()

URLS = f"https://www.youtube.com{YTSearchResult[0]['url_suffix']}"

ydl_opts = {
    'format': 'mp3/bestaudio/best',
    'ffmpeg_location': '.venv/Lib/site-packages/ffmpeg-full_build/bin',
    'outtmpl': './Hang động code (MNguyn)/Chơi Nhạc/Music/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }]
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(URLS)