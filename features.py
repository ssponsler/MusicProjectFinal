import librosa
import numpy as np
import warnings
import pandas as pd
import os
import torch
import crepe
import torchcrepe


# Load an audio file
# audio_file = 'path/to/your/audio/file.wav'
# y, sr = librosa.load(audio_file)
# estimate average pitch
def estimate_pitch_from_mfccs(mfccs, sr):
    pitches = []
    for mfcc_coeff in mfccs:
        # Establish correlation coefficient from MFCC data
        autocorr = np.correlate(mfcc_coeff, mfcc_coeff, mode='full')
        # Establish pitch period and frequency from obtained correlation coefficient
        pitch_period = np.argmax(autocorr)
        pitch_freq = sr / pitch_period
        pitches.append(pitch_freq)
    # Obtain simple average pitch
    avg_pitch = np.mean(pitches)
    return avg_pitch


def estimate_pitch_pyin(audio_file):
    # downsampling to 16 kHz for quicker execution
    y,sr = librosa.load(audio_file, sr=16000)

    # set minimum and maximum frequencies to consider
    f_min = 50
    f_max = 11025 # Absolute maximum

    # extract pitch, voicing mask, voicing probabilities
    # voicing mask: Does the audio frame contain a pitch
    # voicing probability: Probability that the frame contains a voice (?)
    pitches, v_mask, v_prob = librosa.pyin(y, fmin=f_min, fmax=f_max)

    # obtain general pitch of audio file
    if pitches.size > 0:
        pitch = np.nanmean(pitches)
    else:
        return None
    # TODO: error handling
    return pitch


def estimate_pitch_crepe(audio_file):
    # load audio using librosa, since torchcrepe might not handle loading correctly in this case
    audio, sr = librosa.load(audio_file, sr=None)  # Load with original sample rate

    # check if the audio signal is too short
    if len(audio) < sr:
        raise ValueError(f"Input signal length={len(audio)} is too small to resample from {sr}->16000")

    # resample audio to 16000 Hz if necessary
    if sr != 16000:
        audio = librosa.resample(y=audio, orig_sr=sr, target_sr=16000)
        sr = 16000

    # convert audio to a PyTorch tensor and add a batch dimension
    audio = torch.tensor(audio).unsqueeze(0)

    # ensure the audio tensor is of the correct shape and type
    assert audio.ndim == 2, f"Expected 2D tensor, got {audio.ndim}D tensor"
    assert audio.dtype == torch.float32, f"Expected float32 tensor, got {audio.dtype}"

    # here we'll use a 5 millisecond hop length
    hop_length = int(sr / 200.)

    fmin = 65  # C2
    fmax = 20000  # C7

    # select a model capacity--one of "tiny" or "full"
    model = 'tiny'

    # choose a device to use for inference
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

    # pick a batch size that doesn't cause memory errors on your gpu
    batch_size = 2048

    print("about to predict")

    # compute pitch using first gpu
    pitch = torchcrepe.predict(audio,
                               sr,
                               hop_length,
                               fmin,
                               fmax,
                               model,
                               batch_size=batch_size,
                               device=device)
    return pitch


def extract_features_mfcc(audio_file, num_bins=200):
    y, sr = librosa.load(audio_file)
    hop_length = 512  # number of samples between successive frames
    n_fft = 2048  # number of FFT points

    # extract MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    # extract average pitch from MFCCs
    estimated_avg_pitch = estimate_pitch_from_mfccs(mfccs, sr)

    # compute Tonnetz features
    tonnetz = librosa.feature.tonnetz(y=y, sr=sr)

    return mfccs


def extract_features_spectral(audio_file, num_bins=200):
    y, sr = librosa.load(audio_file)
    hop_length = 512  # Number of samples between successive frames
    n_fft = 2048  # Number of FFT points

    # compute spectral centroid
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr).flatten()

    # compute spectral rolloff
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr).flatten()

    # compute spectral flux
    spectral_flux = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)

    # compute spectral flatness
    flatness = librosa.feature.spectral_flatness(y=y).flatten()

    print(flatness)

    # take the mean of spectral flux to make it a scalar
    # TODO: investigate quality dropoff
    spectral_flux_mean = np.mean(spectral_flux)

    # concatenate all binned features into a single feature vector
    # TODO: investigate why NaN values are retrieved
    feature_vector = np.concatenate([
        spectral_centroid, spectral_rolloff, [spectral_flux_mean]
    ])

    return feature_vector


print(f"pitch: {estimate_pitch_pyin('songs_wav/Take On Me.wav')}")