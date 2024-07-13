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
    music_dir = './Music/Song'
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
        return True
    return False

import yt_dlp
from youtube_search import YoutubeSearch

def download_music(search_str: str) -> bool:
    """
    description: Download a song on youtube as a .mp3 file
    
    download directory: ./Music/Music/

    argument:
    - search_str: search_term

    return:
    - return False if the song is already been downloaded
    - return True if the song is successfully downloaded
    """
    print(f'download_music function running with {search_str}\n') # log

    YTSearchResult = YoutubeSearch(str(search_str), max_results=1).to_dict()

    URLS = "https://www.youtube.com{link}".format(link = YTSearchResult[0]['url_suffix'])

    print(YTSearchResult[0]['title']) # log

    if search_music(search_str, 80):
        return False
    else:
        ydl_opts = {
                'format': 'mp3/bestaudio/best',
                'ffmpeg_location': './.venv/ffmpeg-full_build/bin',
                'outtmpl': './Music/Song/' + search_str +'.%(ext)s',
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
    description: search spotify

    argument:
    - query: search_term

    return:
    - return a list containing songs name and its artist from the search results 
    """
    print(f'find_music function running with {query}\n') # log

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
    description: If song is available on device, play that song and return this function after playing

    argument:
    - song: song name

    return:
    - return False if the song is not available on the device
    - return True if the song is successfully found and finished playing
    """
    print(f'play_music function running with {song}\n') # log

    # Bỏ phần dir của tên bài
    music_dir = './Music/Song'
    files = glob.glob(music_dir+'/'+'*.mp3')
    
    if search_music(song, 75):
        song = process.extractOne(song, files, scorer=fuzz.partial_ratio)[0]
        song = song.strip(music_dir+"\ ")
        print(song)
        # Play .MP3 - phần này dùng api yanshee
        return True
    return False

if __name__ == '__main__':
    song_name = 'Son Tung MTP'

    #download_music(find_music(song_name)[1])
    print(play_music("Blank Space"))