import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="b89acd4356eb4d0ca884d29d568daa20",
                                               client_secret="ec186bc7b2fc4aeeb4afd41afda26cad",
                                               redirect_uri="http://localhost:8888/callback/",
                                               scope="user-library-read"))

taylor_uri = 'spotify:artist:41X1TR6hrK8Q2ZCpp2EqCz'

results = sp.artist_albums(taylor_uri, album_type='album')
albums = results['items']
while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])

