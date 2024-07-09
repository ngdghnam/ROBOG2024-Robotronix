import yt_dlp
from youtube_search import YoutubeSearch

def download_music(search_str: str):
    """
    Take in a string and search youtube for a song, return 0 if download is completed
    """
    YTSearchResult = YoutubeSearch(search_str, max_results=1).to_dict()

    URLS = "https://www.youtube.com{link}".format(link = YTSearchResult[0]['url_suffix'])

    ydl_opts = {
        'format': 'mp3/bestaudio/best',
        'ffmpeg_location': './.venv/ffmpeg-full_build/bin',
        'outtmpl': './ChatBot/Music/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download((URLS,))

    return