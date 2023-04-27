import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import plotly.graph_objects as go
import plotly.offline as pyo

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

example_pl = 'https://open.spotify.com/playlist/1Gdw2GwQKAgMcgBeiJQIUk?si=acf4e40e069a4cc5'

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

print(df)