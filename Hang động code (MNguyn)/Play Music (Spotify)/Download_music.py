import spotipy
from spotipy.oauth2 import SpotifyOAuth
from search_music import search_music

import os
import spotipy
import spotipy.oauth2 as oauth2
import yt_dlp
from youtube_search import YoutubeSearch
import urllib.request
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="b89acd4356eb4d0ca884d29d568daa20",
                                               client_secret="ec186bc7b2fc4aeeb4afd41afda26cad",
                                               redirect_uri="http://localhost:8888/callback/",
                                               scope=scope))

result = search_music(search_str='Đen', sp=sp)

result.to_csv('./Hang động code (MNguyn)/Play Music (Spotify)/Result.csv')


def find_and_download_songs(reference_file: str):
    TOTAL_ATTEMPTS = 10
    with open(reference_file, "r", encoding='utf-8') as file:
        for line in file:
            temp = line.split(",")
            name, artist, album_art_url = temp[0], temp[1], temp[3]
            text_to_search = artist + " - " + name
            best_url = None
            attempts_left = TOTAL_ATTEMPTS
            while attempts_left > 0:
                try:
                    results_list = YoutubeSearch(text_to_search, max_results=1).to_dict()
                    best_url = "https://www.youtube.com{}".format(results_list[0]['url_suffix'])
                    break
                except IndexError:
                    attempts_left -= 1
                    print("No valid URLs found for {}, trying again ({} attempts left).".format(
                        text_to_search, attempts_left))
            if best_url is None:
                print("No valid URLs found for {}, skipping track.".format(text_to_search))
                continue

            print("Initiating download for Image {}.".format(album_art_url))
            f = open('{}.jpg'.format(name),'wb')
            f.write(urllib.request.urlopen(album_art_url).read())
            f.close()

            # Run you-get to fetch and download the link's audio
            print("Initiating download for {}.".format(text_to_search))
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl':'%(title)s',     #name the file the ID of the video
                'embedthumbnail': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }, {
                    'key': 'FFmpegMetadata',
                }]
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info([best_url][0], download=True)

                # extract the name of the downloaded file from the info_dict
            filename = ydl.prepare_filename(info_dict)
            print(f"The downloaded file name is: {filename}")

            print('AddingCoverImage ...')
            audio = MP3(f'{filename}' + '.mp3', ID3=ID3)
            try:
                audio.add_tags()
            except error:
                pass

            audio.tags.add(
                APIC(
                    encoding=3,  # 3 is for utf-8
                    mime="image/jpeg",  # can be image/jpeg or image/png
                    type=3,  # 3 is for the cover image
                    desc='Cover',
                    data=open("{}.jpg".format(name), mode='rb').read()
                )
            )
            audio.save()
            os.remove("{}.jpg".format(name))

