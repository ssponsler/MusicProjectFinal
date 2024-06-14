import librosa
import features
from key import detect_key
import numpy as np
import matplotlib.pyplot as plt
import os


def normalize_value(value, lb, ub):
    # clamp between 0 and 1
    return max(0, min((value - lb) / (ub - lb), 1))


def generate_chart(audio_file):
    # mfccs, avg pitch
    mfccs = features.extract_features_mfcc(audio_file)
    avg_pitch = features.estimate_pitch_from_mfccs(mfccs, sr=22050)
    print(f'avg_pitch: {avg_pitch}')

    # tonnetz
    y, sr = librosa.load(audio_file)
    tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
    avg_tonnetz = np.mean(tonnetz)
    print(f'avg_tonnetz: {avg_tonnetz}')

    # tempo
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    tempo = int(round(tempo))
    print(f'tempo: {tempo}')

    detected_key = detect_key(audio_file)
    print(f'detected_key: {detected_key}')

    all_keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#',
                'g', 'g#', 'a', 'a#', 'b']
    key_position = all_keys.index(detected_key) / len(all_keys)

    data = {
        'Pitch': avg_pitch,
        'Harmonics': avg_tonnetz,
        'Tempo': tempo,
        'Key': key_position
    }

    # Radial limits
    pitch_lb = 1.4
    pitch_ub = 4.2
    tonnetz_lb = -0.09
    tonnetz_ub = 0.09
    tempo_lb = 60
    tempo_ub = 185

    normalized_pitch = normalize_value(data['Pitch'], pitch_lb, pitch_ub)
    normalized_tonnetz = normalize_value(data['Harmonics'], tonnetz_lb, tonnetz_ub)
    normalized_tempo = normalize_value(data['Tempo'], tempo_lb, tempo_ub)
    normalized_key = data['Key']
    print(f'normalized pitch: {normalized_pitch}')
    print(f'normalized tonnetz: {normalized_tonnetz}')
    print(f'normalized tempo: {normalized_tempo}')
    print(f'normalized key: {normalized_key}')

    # normalize values
    data_normalized = {
        'Pitch': normalized_pitch,
        'Harmonics': normalized_tonnetz,
        'Tempo': normalized_tempo,
        'Key': normalized_key
    }

    # list names for chart data
    variables = list(data_normalized.keys())
    values = list(data_normalized.values())

    # update the label for the key to display the actual key instead of "Key"
    variables[variables.index('Key')] = f'Key: {detected_key}'

    # convert data for filling the radar chart
    theta = np.linspace(0, 2 * np.pi, len(values), endpoint=False).tolist()
    theta += theta[:1]
    values += values[:1]

    # RADAR CHART
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='polar'))
    ax.plot(theta, values, linewidth=2)  # draws line to connect vertices
    ax.fill(theta, values, 'b', alpha=0.25)  # fills polygon

    # annotations
    for i in range(len(values) - 1):  # remove last repeated value
        ax.text(theta[i], values[i] + 0.05, f'{values[i]:.2f}', ha='center', va='center', fontsize=10, color='black')

    # chart configuration
    ax.set_ylim(0, 1)
    ax.set_yticklabels([])
    ax.set_xticks(np.linspace(0, 2 * np.pi, len(variables), endpoint=False))
    ax.set_xticklabels(variables, fontsize=12)
    ax.tick_params(axis='x', pad=20)  # increase padding for the labels
    ax.set_theta_direction(-1)
    ax.set_theta_offset(np.pi / 2)

    # Extract and set the file name as title
    file_name = os.path.basename(audio_file)
    ax.set_title(f'{file_name}', fontsize=14)

    plt.show()


if __name__ == '__main__':
    print("chartgen.py executed directly")
    generate_chart('songs_wav/Take On Me.wav')
