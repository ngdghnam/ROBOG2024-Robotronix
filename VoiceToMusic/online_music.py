import yt_dlp
from youtube_search import YoutubeSearch
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import unidecode
from os.path import exists

def download_music(search_str: str) -> bool:
    """
    Description: Take in a string and search youtube for a song
    Download directory: .VoiceToMusic/Music/

    return False if the song is already been downloaded
    return True if the song is successfully downloaded
    """

    YTSearchResult = YoutubeSearch(str(search_str), max_results=1).to_dict()

    URLS = "https://www.youtube.com{link}".format(link = YTSearchResult[0]['url_suffix'])

    print(YTSearchResult[0]['title'])

    if exists('./VoiceToMusic/Music/'+search_str+'.mp3'):
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

def find_music(query: str) -> list:
    """
    Take in a string and search spotify, return a list containing songs name and its artist from the search results
    """
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

if __name__ == '__main__':
    print(find_music('Sơn Tùng MTP'))
    download_music('Đen')