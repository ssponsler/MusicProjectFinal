import librosa
import numpy as np
import os

audio_dir = '/songs'

tempo_values = []
audio_files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith('.wav')]

for audio_file in audio_files:
    y, sr = librosa.load(audio_file)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    # convert to usable type
    tempo = int(round(tempo))
    tempo_values.append(tempo)
    print(f'Finished collecting tempo data for: {audio_file}')

# calculate tempo statistics
min_tempo = np.min(tempo_values)
max_tempo = np.max(tempo_values)
mean_tempo = np.mean(tempo_values)
median_tempo = np.median(tempo_values)
q1, q3 = np.percentile(tempo_values, [25, 75])
iqr = q3 - q1

print("Tempo Statistics:")
print(f"Minimum: {min_tempo} BPM")
print(f"Maximum: {max_tempo} BPM")
print(f"Mean: {mean_tempo} BPM")
print(f"Median: {median_tempo} BPM")
print(f"Interquartile Range (IQR): {iqr} BPM")