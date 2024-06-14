from pytube import Playlist
import os
import subprocess

# URL of the playlist
# MY URL
#playlist_url = 'https://www.youtube.com/playlist?list=PL5qidnULHES1wKpZV0fuTtB3suWJBXrYQ'

playlist_url = 'https://www.youtube.com/playlist?list=PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj'
playlist = Playlist(playlist_url)

# create a subfolder named "songs" if it doesn't exist
if not os.path.exists('../songs'):
    os.makedirs('../songs')

# iterate over each video in the playlist
for video in playlist.videos:
    try:
        # download the audio stream as a .wav file to the "songs" subfolder
        audio_file_path = f"songs/{video.title}.wav"
        video.streams.filter(only_audio=True).first().download(output_path='../songs', filename=f"{video.title}.wav")
        print(f"Downloaded: {video.title}")
    except Exception as e:
        print(f"Error downloading {video.title}: {e}")

# normalize the audio files
subprocess.run(["python", "normalize.py"])
