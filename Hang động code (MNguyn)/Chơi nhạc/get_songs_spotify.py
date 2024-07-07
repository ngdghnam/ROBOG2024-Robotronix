import pandas as pd

def get_songs_spotify(search_str, sp):
    search_result=[]

    results = sp.search(search_str)

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

    return pd.DataFrame(search_result)