import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
from environs import Env

env = Env()
env.read_env()


def fetch_playlist_songs(playlist_url, output_file):
    # Spotify API credentials (you need to get these from Spotify Developer Dashboard)
    client_id = env.str("client_id")
    client_secret = env.str("client_secret")

    # Initialize Spotipy with client credentials
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    # Get playlist ID from the URL
    playlist_id = playlist_url.split('/')[-1]

    print(sp.playlist(playlist_id, fields='name'))
    for track_info in sp.playlist(playlist_id)['tracks']['items']:
        if track_info['track'] is None:
            continue
        artist_list = []

        print(track_info['track']['name'])
        print(track_info['track'])
        print([i['name'] for i in track_info['track']['album']['artists']])



         #print(sp.playlist(playlist_id)['tracks'][track_info])
        print("------------")
    # print(sp.playlist(playlist_id)['tracks'])

# Example usage:
playlist_url = 'https://open.spotify.com/playlist/0S0cuX8pnvmF7gA47Eu63M'
output_file = 'playlist_songs.csv'
fetch_playlist_songs(playlist_url, output_file)