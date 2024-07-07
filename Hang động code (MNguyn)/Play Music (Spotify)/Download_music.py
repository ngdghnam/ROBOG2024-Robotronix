import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from search_music import search_music
import spotipy
import yt_dlp
from youtube_search import YoutubeSearch

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="b89acd4356eb4d0ca884d29d568daa20",
                                                           client_secret="ec186bc7b2fc4aeeb4afd41afda26cad"))


search_str = str(input("Tìm Nhạc/Nhạc sĩ: "))

result = search_music(search_str=search_str, sp=sp)

result.to_csv('./Hang động code (MNguyn)/Play Music (Spotify)/Result.csv')

print(result)
choice = int(input("Chọn bài để tải (số): "))


search_str = str(result['SongName'][choice] + ' ' + result['MainArtist'][choice])

YTSearchResult = YoutubeSearch(search_str, max_results=1).to_dict()



URLS = f"https://www.youtube.com{YTSearchResult[0]['url_suffix']}"

ydl_opts = {
    'format': 'mp3/bestaudio/best',
    'ffmpeg_location': '.venv/Lib/site-packages/ffmpeg-full_build/bin',
    'outtmpl': './Hang động code (MNguyn)/Play Music (Spotify)/Music/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }]
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(URLS)