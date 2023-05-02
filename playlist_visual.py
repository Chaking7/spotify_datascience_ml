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
# example_pl = 'https://open.spotify.com/playlist/2xsaTfj4RdIMG4MPHdvJ5x?si=a3fc31337df444b5'
example_pl = 'https://open.spotify.com/playlist/3G2nlO2F0zEjW4mGiTdFt3?si=47cc05d8bcac402f'



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

track_names, track_artist, track_aud_feats = get_playlist_data(example_pl)
for c in range(0,len(track_aud_feats) - 1):
  track_aud_feats[c] = track_aud_feats[c][0]
  del track_aud_feats[c]['loudness']
  del track_aud_feats[c]['tempo']
  track_aud_feats[c]['key'] = track_aud_feats[c].get('key') / 100.0
  del track_aud_feats[c]['type']
  del track_aud_feats[c]['id']
  del track_aud_feats[c]['uri']
  del track_aud_feats[c]['track_href']
  del track_aud_feats[c]['analysis_url']
  del track_aud_feats[c]['duration_ms']
  del track_aud_feats[c]['time_signature']
print(track_names[0])
print(track_artist[0])
print(track_aud_feats[0])

df = pd.DataFrame({
  'track_name' : track_names,
  'track_artist' : track_artist,
  'track_features': track_aud_feats
})

# print(df)
track_fea = df['track_features'].to_list()
track_name = df['track_name'].to_list()

feature_names = []
song_vals = []
for key, item in track_fea[0].items():
  feature_names.append(key)

for c in range(0, len(track_fea) - 1):
  this_val = []
  for key, item in track_fea[c].items():
    this_val.append(item)
  this_val = [*this_val, this_val[0]]
  song_vals.append(this_val)

feature_names = [*feature_names, feature_names[0]]


fig = make_subplots(rows= 5, cols= 5)

for c in range(0, len(song_vals) -1):
  fig.add_trace(go.Scatterpolar(r=song_vals[c], theta=feature_names, name=track_name[c]))

fig.show()