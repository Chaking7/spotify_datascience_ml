import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import plotly.graph_objects as go
import plotly.offline as pyo
from plotly.subplots import make_subplots

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# example_pl = 'https://open.spotify.com/playlist/1Gdw2GwQKAgMcgBeiJQIUk?si=acf4e40e069a4cc5'
# example_pl = 'https://open.spotify.com/playlist/23Yae1UK3nBZhnjuq96Sit?si=eb8cee1dc3ac440c'
# example_pl = 'https://open.spotify.com/playlist/1BGYxCTJaHiGf8wXPHDWcB?si=54d08f9863dc48fb'
example_pl = 'https://open.spotify.com/playlist/2xsaTfj4RdIMG4MPHdvJ5x?si=a3fc31337df444b5'
# example_pl = 'https://open.spotify.com/playlist/3G2nlO2F0zEjW4mGiTdFt3?si=47cc05d8bcac402f'
# example_pl = 'https://open.spotify.com/playlist/4SyYGXFLFWBPrugtLkm0l3?si=89990794736a435a'


def get_playlist_data(id):
  result = sp.playlist(id)
  track_names = []
  track_artist = []
  # track_uris = []
  track_aud_feats = []
  for item in result['tracks']['items']:
    track = item['track']
    track_names.append(track['name'])
    track_artist.append(track['artists'][0]['name'])
    # track_uris.append(track['uri'])
    track_aud_feats.append(sp.audio_features(track['uri']))
  return track_names, track_artist, track_aud_feats

example_album = 'https://open.spotify.com/album/6pChEm0qiDT32ZHfNwVwqh?si=1ts6jkBpRaCPIBjvjRKLiQ'
def get_album_data(id):
  result = sp.album_tracks(id)
  track_names = []
  # track_artist = result['items']['artists']['name']
  # track_uris = []
  track_aud_feats = []
  artist = result['items'][0]['artists'][0]['name']
  for item in result['items']:
    track_names.append(item['name'])
    track_aud_feats.append(sp.audio_features(item['uri']))
  return track_names, artist, track_aud_feats
track_names, track_artist, track_aud_feats = get_playlist_data(example_pl)

track_names2, artist, track_aud_feats2 = get_album_data(example_album)


def simplify_aud_feats(audio_feats):
  for c in range(0,len(audio_feats)):
    audio_feats[c] = audio_feats[c][0]
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
track_aud_feats = simplify_aud_feats(track_aud_feats)
album_aud_feats = simplify_aud_feats(track_aud_feats2)

df = pd.DataFrame({
  'track_name' : track_names,
  'track_artist' : track_artist,
  'track_features': track_aud_feats
})

# print(df)
track_fea = df['track_features'].to_list()
track_name = df['track_name'].to_list()

def separate(features):
  feature_names = []
  song_vals = []
  for key, item in features[0].items():
    feature_names.append(key)

  for c in range(0, len(features)):
    this_val = []
    for key, item in features[c].items():
      this_val.append(item)
    this_val = [*this_val, this_val[0]]
    song_vals.append(this_val)

  feature_names = [*feature_names, feature_names[0]]
  return feature_names, song_vals
'''
feature_names, song_vals = separate(track_fea)
length = len(song_vals) - 2

album_feat_names, album_song_vals = separate(track_aud_feats2)

fig = make_subplots(rows= 1, cols= 2, specs=[[{'type': 'polar'}] * 2] * 1)


for c in range(0, len(song_vals) -1):
  fig.add_trace(go.Scatterpolar(r=song_vals[c], theta=feature_names, name=track_name[c]), row= 1, col = 1)
for c in range(0, len(album_song_vals) - 1):
  fig.add_trace(go.Scatterpolar(r=album_song_vals[c], theta=album_feat_names, name=track_names2[c]), row=1, col =2)
'''



# fig.show()


def compare_two_albums(id1, id2):
  album1_track_names, album1_artist, album1_aud_feats = get_album_data(id1)
  album2_track_names, album2_artist, album2_aud_feats = get_album_data(id2)

  album1_aud_feats = simplify_aud_feats(album1_aud_feats)
  album2_aud_feats = simplify_aud_feats(album2_aud_feats)

  album1_feat_names, album1_song_vals = separate(album1_aud_feats)
  album2_feat_names, album2_song_vals = separate(album2_aud_feats)

  fig = make_subplots(rows= 1, cols= 2, specs=[[{'type': 'polar'}] * 2] * 1)

  for c in range(0, len(album1_song_vals)):
    fig.add_trace(go.Scatterpolar(r=album1_song_vals[c], theta= album1_feat_names, name= album1_track_names[c]), row= 1, col=1)
  for c in range(0, len(album2_song_vals)):
    fig.add_trace(go.Scatterpolar(r=album2_song_vals[c], theta= album2_feat_names, name= album2_track_names[c]), row= 1, col=2)

  fig.show()

# igor
album1 = 'https://open.spotify.com/album/5zi7WsKlIiUXv09tbGLKsE?si=pfEctMYKRqChtWvcoSP0JQ'
# damn
album2 = 'https://open.spotify.com/album/4eLPsYPBmXABThSJ821sqY?si=T_CkyiH4RO2Grc3TFvklAg'
compare_two_albums(album1, album2)