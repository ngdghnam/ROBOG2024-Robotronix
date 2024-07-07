from Authentication import Authentication
from get_songs_spotify import get_songs_spotify

def search_song():
    search_str = str(input("Tìm Nhạc/Nhạc sĩ: "))

    result = get_songs_spotify(search_str=search_str, sp=Authentication())

    result.to_csv('./Hang động code (MNguyn)/Chơi Nhạc/Result.csv')

    print(result)
    choice = int(input("Chọn bài để tải (số): "))

    search_str = str(result['SongName'][choice] + ' ' + result['MainArtist'][choice])

    return search_str