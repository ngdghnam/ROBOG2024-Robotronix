import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

def find_music(search_str):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id="b89acd4356eb4d0ca884d29d568daa20",
        client_secret="ec186bc7b2fc4aeeb4afd41afda26cad"
        )
    )

    results = sp.search(search_str)

    search_result=[]
    for result in results['tracks']['items']:
            
        AssistArtist = ""
        for i in range(1,len(result['artists'])):
            temp = result['artists'][i]['name']
            if i == 1:
                AssistArtist += temp
            else:
                AssistArtist = ", " + temp
            
        result_details = dict(
            SongName = result['name'],
            MainArtist = result['artists'][0]['name'],
            FeaturedArtist = AssistArtist,
            URI = result['uri']
        )
        search_result.append(result_details)

    result = pd.DataFrame(search_result)

    result.to_csv('./Result.csv')
    print(result)

    search_str = str(result['SongName'][0] + ' ' + result['MainArtist'][0])

    return search_str