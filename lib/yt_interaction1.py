from ytmusicapi import YTMusic

def create_result_dict(sr):
    video_id = sr['videoId']
    duration = sr['duration']
    artist = [i['name'] for i in sr['artists'] if i['id'] is not None]
    title = sr['title']
    album = sr['album']['name']
    album_id = sr['album']['id']
    return {"videoID": video_id,
            "duration": duration,
            "artist": artist,
            "title": title,
            "album": album,
            "album_id": album_id}

yt = YTMusic('oauth.json')
playlistId = yt.create_playlist(title='test',
                                description='test description',
                                privacy_status='PUBLIC')

track_name = "Wonderwall"
artist_name = "Oasis"

songs = yt.search(query=f"{track_name} by {artist_name}", filter="songs")

print(songs[1])

yt.add_playlist_items(playlistId, [songs[1]['videoId']])
print(create_result_dict(songs[1]))