import librosa
import pandas as pd
import numpy as np
import os

# estimate Average Pitch
def average_mfccs(mfccs, sr):
    coeffs = []
    for mfcc_coeff in mfccs:
        autocorr = np.correlate(mfcc_coeff, mfcc_coeff, mode='full')
        period = np.argmax(autocorr)
        freq = sr / period
        coeffs.append(freq)
    avg_mfcc = np.mean(coeffs)
    return avg_mfcc

# function to extract features from an audio file
def extract_features(audio_file):
    y, sr = librosa.load(audio_file, sr=None)

    # extract MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    estimated_avg_pitch = average_mfccs(mfccs, sr)

    # concatenate MFCCs into a single feature vector
    feature_vector = mfccs.flatten()
    return feature_vector, estimated_avg_pitch
