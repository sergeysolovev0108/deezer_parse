import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)


def add_playlist(playlist_title, playlist_description):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": playlist_title,
                "description": playlist_description,
                "defaultLanguage": "ru"
            },
            "status": {
                "privacyStatus": "public"
            }
        }
    )
    response = request.execute()
    print('Playlist created: ', playlist_title,)

    youtube_playlist_id = response['id']

    return youtube_playlist_id


def add_track_to_playlist(youtube_playlist_id, youtube_video_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": youtube_playlist_id,
                "position": 0,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": youtube_video_id
                }
            }
        }
    )

    response = request.execute()
