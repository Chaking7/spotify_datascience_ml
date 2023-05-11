
import numpy as np
import os
import pickle
import pyarrow.feather as feather
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sklearn.linear_model import LogisticRegression
import time

# same method from the playlist visual file, however some error with dimensionality
def simplify_aud_feats(audio_feats):
        for c in range(0,len(audio_feats)):
            del audio_feats[c]['loudness']
            del audio_feats[c]['tempo']
            audio_feats[c]['key'] = audio_feats[c].get('key') / 100.0
            del audio_feats[c]['type']
            del audio_feats[c]['id']
            del audio_feats[c]['uri']
            del audio_feats[c]['track_href']
            del audio_feats[c]['analysis_url']
            del audio_feats[c]['duration_ms']
            del audio_feats[c]['time_signature']
        return audio_feats

'''
pickle file compression
time = 121 seconds
'''
def album_data_pickle(directory= '../'):
    start = time.time()
    picklefile = os.path.join(directory + '/album_data.pkl')
    if not os.path.isfile(picklefile):
        scope = "user-library-read"

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

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

        features = []
        for c in range(0, len(track_uris)):
            curr = sp.audio_features(track_uris[c])
            features.append(simplify_aud_feats(curr))
        liked = [1] * len(tracks)
        # gitprint(len(tracks))
        df = pd.DataFrame({
            'track_name': tracks,
            'features' : features,
            'liked' : liked
        })
        df.to_pickle('album_data.pkl')
        print(df)
    else:
        df = pd.read_pickle('album_data.pkl')
        print(df)
    end = time.time()
    print(end - start)

# album_data_pickle()
'''
feather file compression
time = .04 seconds lmaoooooo
'''
def album_data_feather(directory= '../'):
    start = time.time()
    feather_file = os.path.join(directory + '/album_data.ftr')
    if not os.path.isfile(feather_file):
        scope = "user-library-read"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

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

        features = []
        for c in range(0, len(track_uris)):
            curr = sp.audio_features(track_uris[c])
            features.append(simplify_aud_feats(curr))
        liked = [1] * len(tracks)
        # gitprint(len(tracks))
        df = pd.DataFrame({
            'track_name': tracks,
            'features' : features,
            'liked' : liked
        })
        feather.write_feather(df, directory + '/album_data.ftr')
    else:
        read_df = feather.read_feather(directory + '/album_data.ftr')
        print(read_df)
    end = time.time()
    print(end - start)

album_data_feather()
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