import glob
from thefuzz import fuzz

def search_music(song: str, similiar_score: int) -> bool:
    """
    description: Search song on the device

    arguments:
    - song: search term
    - similiar_score: define how similiar it is to the search term (higher = need more exact wording)

    return:
    - return True if the function found the song on the device
    - return False if the function did not find the song on the device
    """
    # Bỏ phần dir của tên bài
    music_dir = './Functions/Music/Song'
    files = glob.glob(music_dir+'/'+'*.mp3')
    
    # Search song on the device
    top_result=0
    for file in files:
        file = file.strip(music_dir)
        file = file[1:]
        similarity = fuzz.partial_ratio(song, file) # Rate how close each song name is to the search term
        if similarity > top_result and similarity > similiar_score:
            top_result = similarity

    if top_result != 0:
        return True
    return False

import yt_dlp
from youtube_search import YoutubeSearch

def download_music(search_str: str) -> bool:
    """
    description: Download a song on youtube as a .mp3 file
    
    download directory: ./Functions/Music/Music/

    argument:
    - search_str: search_term

    return:
    - return False if the song is already been downloaded
    - return True if the song is successfully downloaded
    """
    print(f'download_music function running with {search_str}\n') # log

    YTSearchResult = YoutubeSearch(str(search_str), max_results=1).to_dict()

    URLS = "https://www.youtube.com{link}".format(link = YTSearchResult[0]['url_suffix'])

    search_result = YTSearchResult[0]['title']
    
    print(search_result) # log

    if search_music(search_str, 80):
        return False
    else:
        ydl_opts = {
                'format': 'mp3/bestaudio/best',
                'ffmpeg_location': './.venv/ffmpeg-full_build/bin', # https://ffmpeg.org/ | Tải về rồi chỉ đến mục bin
                'outtmpl': './Functions/Music/Song/' + search_str +'.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }]
            }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download((URLS,))
        return True

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import unidecode
import sys
import os
sys.path.append(os.path.abspath('.'))
import config

def find_music(query: str) -> list:
    """
    description: search spotify

    argument:
    - query: search_term

    return:
    - return a list containing songs name and its artist from the search results 
    """
    print(f'find_music function running with {query}\n') # log

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id = config.Spotify_CLIENT_KEY,
        client_secret = config.Spotify_CLIENT_SECRET
        )
    )

    results = sp.search(query, limit=10)
    search_list=[]
    for result in results['tracks']['items']:
        search_list.append(str(unidecode.unidecode(result['name'] + ' by ' + result['artists'][0]['name'])))
    return search_list

from thefuzz import process
import YanAPI as YanAPI
import time

ip_addr = config.YanIP
YanAPI.yan_api_init(ip_addr)

def check_available_song(gemini: bool=False) -> list:
    """
    description: return a list of avaliable song on the device
    
    argument:
    - gemini: check if Gemini is calling the function
    """
    music_dir = './Functions/Music/Song/'
    files = glob.glob(music_dir+'*.mp3')
    songs=[]
    for song in files:
        # Bỏ phần dir của tên bài
        song = song.strip(music_dir)
        song = song[1:]
        songs.append(song)

    system_songs=YanAPI.get_media_music_list()
    for song in system_songs['data']['music']:
        songs.append(song['name'])
    return songs

from mutagen.mp3 import MP3

def play_music(song: str) -> bool:
    """
    description: If song is available on device, play that song and return this function after playing

    argument:
    - song: song name

    return:
    - return False if the song is not available on the device
    - return True if the song is successfully found and finished playing
    """
    print(f'play_music function running with {song}\n') # log
    music_dir = './Functions/Music/Song/'
    files = glob.glob(music_dir+'*.mp3')

    if search_music(song, 75):
        song = process.extractOne(song, files, scorer=fuzz.partial_ratio)[0]
        # Bỏ phần dir của tên bài
        song = song.strip(music_dir) 
        song = song[1:]
        print(YanAPI.start_voice_tts("Playing "+song.strip('.mp3')+"", False)) # log
        time.sleep(2)
        YanAPI.upload_media_music(f'./Functions/Music/Song/{song}')
        time.sleep(3)
        # YanAPI.start_play_music(song)
        print(YanAPI.start_play_music(name=song)) # log
        time.sleep(MP3('./Functions/Music/Song/{title}'.format(title=song)).info.length)
        YanAPI.stop_play_music()
        YanAPI.delete_media_music(song)
        return True
    else:
        for song_inter in check_available_song():
            if fuzz.partial_ratio(song, song_inter) > 75:
                song = song_inter
                YanAPI.start_voice_tts("Playing "+song.strip('.mp3')+"", False)
                time.sleep(2)
                try:
                    YanAPI.start_voice_tts("I can also dance to this song, here we go",False)
                    time.sleep(3)
                    YanAPI.sync_play_motion(name=song.strip('.mp3'))
                except:
                    YanAPI.sync_play_music(name=song)
                finally:
                    YanAPI.stop_play_motion()
                    YanAPI.stop_play_music()
                    return True
    return False

if __name__ == '__main__':
    song_name = 'Hello'
    # download_music(song_name)
    # check_available_song()