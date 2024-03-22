import re
from ytmusicapi import YTMusic
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from environs import Env


def find_song(yt, track_name, artist_name, album_name):
    songs = yt.search(query=f"{track_name} by {artist_name}", filter="songs")

    #  This would need to do fuzzy matching
    for song in songs:
        # Remove everything in brackets in the song title
        song_title_without_brackets = re.sub(r"[\[(].*?[])]", "", song["title"])
        if (
                (
                        song_title_without_brackets == track_name
                        and song["album"]["name"] == album_name
                )
                or (song_title_without_brackets == track_name)
                or (song_title_without_brackets in track_name)
                or (track_name in song_title_without_brackets)
        ) and (
                song["artists"][0]["name"] == artist_name
                or artist_name in song["artists"][0]["name"]
        ):
            return song

    # Finds approximate match
    # This tries to find a song anyway. Works when the song is not released as a music but a video.
    else:
        track_name = track_name.lower()
        first_song_title = songs[0]["title"].lower()
        if (
                track_name not in first_song_title
                or songs[0]["artists"][0]["name"] != artist_name
        ):  # If the first song is not the one we are looking for
            print("Not found in songs, searching videos")
            new_songs = yt.search(
                query=f"{track_name} by {artist_name}", filter="videos"
            )  # Search videos

            # From here, we search for videos reposting the song. They often contain the name of it and the artist. Like with 'Nekfeu - Ecrire'.
            for new_song in new_songs:
                new_song_title = new_song[
                    "title"
                ].lower()  # People sometimes mess up the capitalization in the title
                if (
                        track_name in new_song_title
                        and artist_name in new_song_title
                ) or (track_name in new_song_title):
                    print("Found a video")
                    return new_song
            else:
                # Basically we only get here if the song isn't present anywhere on YouTube
                raise ValueError(
                    f"Did not find {track_name} by {artist_name} from {album_name}"
                )
        else:
            return songs[0]


def create_yt_playlist(yt, i_title, i_description="", i_privacy_status="PUBLIC"):
    return yt.create_playlist(title=i_title, description=i_description, privacy_status=i_privacy_status)


def fetch_playlist_songs(playlist_url, env):
    # Spotify API credentials (you need to get these from Spotify Developer Dashboard)
    client_id = env.str("client_id")
    client_secret = env.str("client_secret")

    # Initialize Spotipy with client credentials
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    # Get playlist ID from the URL
    playlist_id = slice_until_non_alphanumeric(playlist_url.split('/')[-1])

    returnList = []

    for track_info in sp.playlist(playlist_id)['tracks']['items']:
        if track_info['track'] is None:
            continue

        # Get first Artist name
        artist = track_info['track']['album']['artists'][0]['name']
        # Get track name
        track_name = track_info['track']['name']
        # Get album name
        album_name = track_info['track']['album']['name']

        returnList.append({"track_name": track_name, "artist": artist, "album_name": album_name})

    return returnList


def slice_until_non_alphanumeric(input_string):
    for i, char in enumerate(input_string):
        if not char.isalnum():
            return input_string[:i]
    return input_string


def create_populate_yt_playlist(link, playlist_title, playlist_description="", playlist_privacy="PUBLIC"):
    yt = YTMusic('oauth.json')

    env = Env()
    env.read_env()

    # List of dicts of the form {"track_name": "", "artist": "", "album_name": ""}
    playlist_info = fetch_playlist_songs(link, env)

    playlist_obj = create_yt_playlist(yt, playlist_title, playlist_description, playlist_privacy)

    for song_info in playlist_info:
        track_name, artist_name, album_name = song_info['track_name'], song_info['artist'], song_info['album_name']
        song_id = find_song(yt, track_name, artist_name, album_name)
        yt.add_playlist_items(playlist_obj, [song_id['videoId']])

    # return link to the playlist
    yt_playlist_url_header = "https://music.youtube.com/playlist?list="
    return yt_playlist_url_header + playlist_obj


def main():
    playlist_link = "https://open.spotify.com/playlist/1CWuCxneZ9R32IseMQe9JO?si=520f8b6d9f714427"
    create_populate_yt_playlist(playlist_link, "test4")


main()


