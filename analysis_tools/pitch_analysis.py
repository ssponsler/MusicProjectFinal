import librosa
import mfcc
import features
import numpy as np
import os

# specify the folder path containing the songs
audio_dir = '/songs_wav'

pitch_values = []

# get a list of all .wav files in the directory
audio_files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith('.wav')]
for audio_file in audio_files:
    # extract MFCCs and estimate average pitch
    # mfccs = features.extract_features_mfcc(audio_file)
    # avg_pitch = features.estimate_pitch_from_mfccs(mfccs, sr=22050)
    pitch = features.estimate_pitch_pyin(audio_file)
    # pitch = features.estimate_pitch_crepe(audio_file)
    pitch_values.append(pitch)
    print(f'Finished collecting pitch data for: {audio_file}, {pitch}')

# calculate pitch statistics
min_pitch = np.min(pitch_values)
max_pitch = np.max(pitch_values)
mean_pitch = np.mean(pitch_values)
median_pitch = np.median(pitch_values)
q1, q3 = np.percentile(pitch_values, [25, 75])
iqr = q3 - q1

# print the results
print("Pitch Statistics:")
print(f"Minimum: {min_pitch}")
print(f"Maximum: {max_pitch}")
print(f"Mean: {mean_pitch}")
print(f"Median: {median_pitch}")
print(f"Interquartile Range (IQR): {iqr}")