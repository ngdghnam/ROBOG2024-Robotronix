import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="b89acd4356eb4d0ca884d29d568daa20",
                                                           client_secret="ec186bc7b2fc4aeeb4afd41afda26cad"))

results = sp.search(q='bbnos', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])