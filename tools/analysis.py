import features
import pandas as pd
import os

# set the directory containing the audio files
audio_dir = '../songs'

# get a list of all .wav files in the directory
audio_files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith('.wav')]

# extract feature vectors for each audio file
feature_vectors = []
for audio_file in audio_files:
    feature_vector = features.extract_features(audio_file)
    feature_vectors.append(feature_vector)
    print(f"Finished retrieving feature vectors for {audio_file}.")

# create a DataFrame from the feature vectors
df = pd.DataFrame(feature_vectors)

# save the DataFrame to a CSV file
df.to_csv('analysis/feature_vectors.csv', index=False)
