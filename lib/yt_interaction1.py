from ytmusicapi import YTMusic

yt = YTMusic('oauth.json')
playlistId = yt.create_playlist(title='test',
                                description='test description',
                                privacy_status='PUBLIC')

search_results = yt.search('Oasis Wonderwall')
print(search_results[1])

yt.add_playlist_items(playlistId, [search_results[1]['videoId']])
