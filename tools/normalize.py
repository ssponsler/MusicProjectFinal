import os
from pydub import AudioSegment

# path to the "songs" folder
songs_path = "../songs"

# iterate over each file in the "songs" folder
for file_name in os.listdir(songs_path):
    if file_name.endswith(".wav"):
        try:
            audio_file_path = os.path.join(songs_path, file_name)

            # normalize the audio levels
            audio = AudioSegment.from_file(audio_file_path)
            normalized_audio = audio.normalize()

            # re-export the normalized audio
            normalized_audio.export(audio_file_path, format="wav")
            print(f"Normalized: {file_name}")
        except Exception as e:
            print(f"Error normalizing {file_name}: {e}")
