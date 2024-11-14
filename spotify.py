from dotenv import load_dotenv
import os, requests, json

# load .env
load_dotenv()

CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

AUTH_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_URL = 'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

def Authenticate():
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    #Convert response to JSON
    auth_response_data = auth_response.json()

    #Save the access token
    access_token = auth_response_data['access_token']

    #Need to pass access token into header to send properly formed GET request to API server
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    return headers

def get_playlist(headers):
    playlist_input = input("Playlist link or id : ")
    playlist_id = ''
    
    # For Playlist ID
    if ('https' not in playlist_input) and ('?' not in playlist_input) :
        playlist_id = playlist_input
    # For shared link
    elif 'https' in playlist_input and '?' in playlist_input:
        playlist_id = playlist_input.split('playlist/')[1].split('?')[0]
    # For Web URL
    elif 'https' in playlist_input and '?' not in playlist_input:
        playlist_id = playlist_input.split('playlist/')[1]
        
    offset = 0
    
    response=get_request(playlist_id, headers, 0)
    data_dic=response.json()
    track_len=data_dic['total']
    
    if track_len>50:
        for i in range(50, track_len, 50):
            additional_data =get_request(playlist_id, headers, i).json()
            data_dic['items'].extend(additional_data['items'])
    
    result = tuple({
    "album_type": item["track"]["album"]["album_type"],
    "album_name": item["track"]["album"]["name"],
    "artist": item["track"]["artists"][0]["name"],  # Assuming the first artist in the list
    "title": item["track"]["name"]
    } for item in data_dic["items"])
    return result

def get_request(playlist_id, headers, offset):
    return requests.get(
        SPOTIFY_URL.format(playlist_id=playlist_id),
        params={
        'fields' : 'total,items(track(name,album(album_type,name),artists(name)))',
        'limit' : 50,
        'offset' : offset
        },
        headers=headers
        )