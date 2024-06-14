import librosa
import mfcc
import features
import numpy as np
import os

# Specify the folder path containing the songs
audio_dir = '/songs'

tonnetz_values = []

# Get a list of all .wav files in the directory
audio_files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith('.wav')]
for audio_file in audio_files:
    # Extract tonnetz feature
    y, sr = librosa.load(audio_file)
    tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
    avg_tonnetz = np.mean(tonnetz)
    tonnetz_values.append(avg_tonnetz)
    print(f'Finished collecting tonnetz data for: {audio_file}')

# Calculate tonnetz statistics
min_tonnetz = np.min(tonnetz_values)
max_tonnetz = np.max(tonnetz_values)
mean_tonnetz = np.mean(tonnetz_values)
median_tonnetz = np.median(tonnetz_values)
q1, q3 = np.percentile(tonnetz_values, [25, 75])
iqr = q3 - q1

# Print the results
print("Tonnetz Statistics:")
print(f"Minimum: {min_tonnetz}")
print(f"Maximum: {max_tonnetz}")
print(f"Mean: {mean_tonnetz}")
print(f"Median: {median_tonnetz}")
print(f"Interquartile Range (IQR): {iqr}")
