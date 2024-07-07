URLS = [f"https://www.youtube.com{YTSearchResult['url_suffix']}"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="b89acd4356eb4d0ca884d29d568daa20",
                                               client_secret="ec186bc7b2fc4aeeb4afd41afda26cad",
                                               redirect_uri="http://localhost:8888/callback/",
                                               scope=scope))