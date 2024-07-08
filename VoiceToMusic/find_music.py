import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
from youtube_search import YoutubeSearch

def download_music(search_str):
    YTSearchResult = YoutubeSearch(search_str, max_results=1).to_dict()

    URLS = "https://www.youtube.com{link}".format(link = YTSearchResult[0]['url_suffix'])

    ydl_opts = {
        'format': 'mp3/bestaudio/best',
        'ffmpeg_location': './.venv/ffmpeg-full_build/bin/',
        'outtmpl': './Music/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download((URLS,))

def find_music(search_str):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id="b89acd4356eb4d0ca884d29d568daa20",
        client_secret="ec186bc7b2fc4aeeb4afd41afda26cad"
        )
    )

    results = sp.search(search_str, limit=1)
    
    result_details = dict(
        SongName = results['tracks']['items'][0]['name'],
        MainArtist = results['tracks']['items'][0]['artists'][0]['name']
    )

    search_result = str(result_details['SongName'] + ' ' + result_details['MainArtist'])

    return search_result

download_music(find_music("Skibidi"))