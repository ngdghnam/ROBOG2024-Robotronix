import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def find_music(search_str):
    """
    Take in a string and search spotify for a song, return a string containing song name and artist
    """
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

    search_result = str(result_details['SongName'] + ' by ' + result_details['MainArtist'])

    return search_result

if __name__ == "__main__":
    print(find_music('i remember bbnos'))
