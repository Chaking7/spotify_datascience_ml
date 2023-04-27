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

'''
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
'''

results = sp.current_user_saved_tracks()
''' for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], "  ", track['name'])
'''

example_pl = 'https://open.spotify.com/playlist/1Gdw2GwQKAgMcgBeiJQIUk?si=acf4e40e069a4cc5'
def get_playlist_data(id):
    result = sp.playlist(id)
    track_names = []
    track_uris = []
    track_analysiss = []
    track_aud_feat = []
    i = 0
    for item in result['tracks']['items']:
        track = item['track']
        if i is 0:
            print(track)
            i += 1
        track_names.append(track['name'])
        track_uris.append(track['uri'])
        track_analysiss.append(sp.audio_analysis(track['uri']))
        track_aud_feat.append(sp.audio_features(track['uri']))
    return track_names, track_aud_feat
    # print(track_names)
    # print(result['tracks']['items'][0])
    # print(track_uris)
    # print(track_analysiss[0])
    # df = pd.DataFrame(track_analysiss[0])
    # print(track_aud_feat[0])

track_names, track_aud_feat = get_playlist_data(example_pl)
feat_name = []
feat_value = []
# print(type(track_aud_feat))
# print(len(track_aud_feat))
first_graph_feat = []
first_graph_val = []
# type(track_aud_feat[0][0])
print(track_aud_feat[0][0])
track_aud_dict = track_aud_feat[0][0]

# for the graph I am going to take ou the tempo, loudness, and bring the key down
del track_aud_dict['loudness']
del track_aud_dict['tempo']
track_aud_dict['key'] = track_aud_dict.get('key') / 100.0
for key, item in track_aud_dict.items():
    first_graph_feat.append(key)
    first_graph_val.append(item)
# print(first_graph_feat)
# print(first_graph_val)
# print(first_graph_val[:11])
first_graph_feat = first_graph_feat[:9]
first_graph_val = first_graph_val[:9]
print(first_graph_feat)
print(first_graph_val)
first_graph_feat = [*first_graph_feat, first_graph_feat[0]]
first_graph_val = [*first_graph_val, first_graph_val[0]]
'''
df = pd.DataFrame({
    'feature': first_graph_feat,m
    'values': first_graph_val
}
)

'''

label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(first_graph_feat))
plt.figure(figsize=(8,8))
plt.subplot(polar=True)
plt.plot(label_loc, first_graph_val, label=  track_names[0])
plt.title('Song features')
lines, labels = plt.thetagrids(np.degrees(label_loc), labels=first_graph_feat)
plt.legend()

plt.show()
'''
categories = ['Food Quality', 'Food Variety', 'Service Quality', 'Ambiance', 'Affordability']

restaurant_1 = [4, 4, 5, 4, 3]
restaurant_2 = [5, 5, 4, 5, 2]
restaurant_3 = [3, 4, 5, 3, 5]

label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(restaurant_1))

plt.figure(figsize=(8, 8))
plt.subplot(polar=True)
plt.plot(label_loc, restaurant_1, label='Restaurant 1')
plt.plot(label_loc, restaurant_2, label='Restaurant 2')
plt.plot(label_loc, restaurant_3, label='Restaurant 3')
plt.title('Restaurant comparison', size=20)
lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)
plt.legend()
'''


# np_first_graph_feat = np.array(first_graph_feat)
# np_first_graph_val = np.array(first_graph_val)


# first_graph = track_aud_feat[0][0].split(', ')
# print(first_graph[0])
# plt.figure(figsize=(8, 8))
# plt.fill()
# plt.show()
