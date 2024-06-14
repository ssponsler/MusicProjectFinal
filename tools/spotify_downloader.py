import spotipy
import os
import requests
from spotipy.oauth2 import SpotifyClientCredentials

# UNUSED

client_id = '437f8c21a3414605bbbbbf94c1dc84e6'
client_secret = '7adc4443c1b14be58f770bd0d5700a71'

# Authenticate
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist_id = '0goC2ziixBh5SdONAl901J?si=95a7929b215b4f79'

results = sp.playlist_items(playlist_id)
tracks = results['items']
while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])

