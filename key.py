import librosa
import numpy as np
import matplotlib.pyplot as plt

def detect_key(audio_file):
    # Load the audio file
    y, sr = librosa.load(audio_file, sr=None)

    # compute the chroma features
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)

    major_template = np.array([1, 0, 0, 0.5, 1, 0, 0, 1, 0, 0.5, 0, 0.5])
    minor_template = np.array([1, 0, 0.5, 1, 0, 0.5, 0, 1, 0.5, 0, 0, 0.5])

    major_keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    minor_keys = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']

    correlations = []
    for i in range(12):
        major_correlation = np.correlate(np.roll(major_template, i), chroma_mean)
        minor_correlation = np.correlate(np.roll(minor_template, i), chroma_mean)
        correlations.append((major_correlation[0], minor_correlation[0]))

    # determine the key with the highest correlation
    max_correlation_index = np.argmax([max(c) for c in correlations])
    if correlations[max_correlation_index][0] > correlations[max_correlation_index][1]:
        detected_key = major_keys[max_correlation_index]
    else:
        detected_key = minor_keys[max_correlation_index]

    return detected_key