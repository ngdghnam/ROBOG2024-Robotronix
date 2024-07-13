import glob
from thefuzz import fuzz

def search_music(song: str, similiar_score: int) -> bool:
    """
    Search song on the device
    """
    # Bỏ phần dir của tên bài
    music_dir = './VoiceToMusic/Music'
    files = glob.glob(music_dir+'/'+'*.mp3')
    
    # Search song on the device
    top_result=0
    log_top_song=''
    for file in files:
        file = file.strip(music_dir+"\ ")
        similarity = fuzz.partial_ratio(song, file) # Rate how close each song name is to the search term
        if similarity > top_result and similarity > similiar_score:
            top_result = similarity
            log_top_song = file
    
    print(log_top_song + ': ' + str(top_result))

    if top_result != 0:
        return 1
    return 0

import yt_dlp
from youtube_search import YoutubeSearch

def download_music(search_str: str) -> bool:
    """
    Description: Take in a string containing song name and artist name and search youtube for a song
    Download directory: .VoiceToMusic/Music/

    return False if the song is already been downloaded
    return True if the song is successfully downloaded
    """

    print(f'download_music function running with {search_str}') # log

    YTSearchResult = YoutubeSearch(str(search_str), max_results=1).to_dict()

    URLS = "https://www.youtube.com{link}".format(link = YTSearchResult[0]['url_suffix'])

    print(YTSearchResult[0]['title'])

    if search_music(search_str, 80):
        return False
    else:
        ydl_opts = {
                'format': 'mp3/bestaudio/best',
                'ffmpeg_location': './.venv/ffmpeg-full_build/bin',
                'outtmpl': './VoiceToMusic/Music/' + search_str +'.%(ext)s',
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

def find_music(query: str) -> list:
    """
    Take in a string and search spotify, return a list containing songs name and its artist from the search results
    """
    print(f'find_music function running with {query}') # log

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id="b89acd4356eb4d0ca884d29d568daa20",
        client_secret="ec186bc7b2fc4aeeb4afd41afda26cad"
        )
    )

    results = sp.search(query, limit=10)
    search_list=[]
    for result in results['tracks']['items']:
        search_list.append(str(unidecode.unidecode(result['name'] + ' by ' + result['artists'][0]['name'])))
    return search_list

#    result_details = dict(
#        SongName = results['tracks']['items'][0]['name'],
#        MainArtist = results['tracks']['items'][0]['artists'][0]['name']
#    )

from thefuzz import process

def play_music(song: str) -> bool:
    """
    Take in a song name and search the available song on the device. If available, play that song
    Return 0 if the song is not available on the device
    Return 1 if the song is successfully found and finished playing
    """

    print(f'play_music function running with {song}') # log

    # Bỏ phần dir của tên bài
    music_dir = './VoiceToMusic/Music'
    files = glob.glob(music_dir+'/'+'*.mp3')
    
    if search_music(song, 75):
        song = process.extractOne(song, files, scorer=fuzz.partial_ratio)[0]
        song = song.strip(music_dir+"\ ")
        print(song)
        # Play .MP3
        return 1
    return 0


if __name__ == '__main__':
    song_name = 'Son Tung MTP'

    # Download_music(find_music(song_name)[1])
    print(play_music("Son Tung MTP"))