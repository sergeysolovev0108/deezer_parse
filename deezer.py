import json
import requests
from add_to_youtube import add_playlist, add_track_to_playlist
from youtubesearchpython import SearchVideos


def get_data_from_deezer_api():
    while True:
        playlist_url = input('Input playlist link: ')
        playlist_id = playlist_url.split('/')[-1]
        url = 'https://api.deezer.com/playlist/{}'.format(playlist_id)
        print(url)
        global data
        data = requests.get(url)
        if 'error' in data.json():
            print('Playlist Not Found. Please enter a valid link')
            get_data_from_deezer_api()
        break
    return data


data = get_data_from_deezer_api()

playlist_title = data.json()['title']
playlist_description = data.json()['description']


# Creating playlist on Youtube end return created playlist id
youtube_playlist_id = add_playlist(playlist_title, playlist_description)
# Not added tracks list
not_added_to_playlist = []

for track in data.json()['tracks']['data']:
    song = track['artist']['name'] + ' ' + track['title']
    print(song)
    s = json.loads(SearchVideos(song, offset=1, mode="json", max_results=1).result())

    if bool(s['search_result']):
        print('Link: ', s['search_result'][0]['link'])
        youtube_video_id = s['search_result'][0]['id']
        add_track_to_playlist(youtube_playlist_id, youtube_video_id)
        print('Added to playlist: ', song)
        print('___________________________________________________________')
    else:
        print(song, ':', 'Not added to playlist')
        not_added_to_playlist.append(song)
        print('___________________________________________________________')

if bool(not_added_to_playlist):
    print('Some errors. Track not added to playlist:', not_added_to_playlist)
