
import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sklearn.linear_model import LogisticRegression

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# recently_played
'''
playlists = sp.user_playlists('spotify')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
'''

albums = sp.current_user_saved_albums()
test = 0
tracks = []
track_uris = []
while albums:
    for i, album in enumerate(albums['items']):
        # print(album)
        # print(album['album'].keys())
        # print(album['album']['name'])
        # print(album['album']['tracks']['items'][0]['name'])
        #print(album['album']['tracks']['items'][0]['name'])
        for item in album['album']['tracks']['items']:
            tracks.append(item['name'])
            track_uris.append(item['uri'])
    if albums['next']:
        albums = sp.next(albums)
    else:
        albums = None

# print(len(tracks))