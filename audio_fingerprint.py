import os
import numpy as np
from skimage.feature import peak_local_max
from scipy.ndimage import maximum_filter
from collections import defaultdict
import librosa

import pickle
# import matplotlib.pyplot as plt


def generate_fingerprint(audio_path, **kwargs):
    """
    taken from week 9 lab material:
    """

    # Load audio
    y, sr = librosa.load(audio_path, sr=22050)

    # Compute and plot STFT spectrogram
    D = np.abs(librosa.stft(y, n_fft=kwargs["WINDOW_SIZE"], window='hann', hop_length=kwargs["HOP_LENGTH"]))
    S_log = librosa.amplitude_to_db(D, ref=np.max)  # Convert to log scale (decibels)

    # Detect peaks
    # peaks = peak_local_max(np.log(D), min_distance=10,threshold_rel=0.05)
    local_max = maximum_filter(D, size=kwargs["PEAK_NEIGHBORHOOD_SIZE"]) == D
    peaks = np.argwhere(local_max)

    # Generate fingerprints
    frequencies = librosa.fft_frequencies(sr=sr, n_fft=kwargs["WINDOW_SIZE"])
    times = librosa.frames_to_time(np.arange(S_log.shape[1]), sr=sr, hop_length=kwargs["HOP_LENGTH"])

    fingerprints = generate_hashes(peaks, frequencies, times)
    
    return fingerprints

def generate_hashes(peaks, frequencies, times):
    '''
    return: [((freq1, freq2, delta_time),time) ]
    ''' 

    fingerprints = []
    for i in range(len(peaks)):
        for j in range(1, 10):
            if i + j < len(peaks):
                freq1 = frequencies[peaks[i][0]]
                freq2 = frequencies[peaks[i + j][0]]
                time1 = times[peaks[i][1]]
                time2 = times[peaks[i + j][1]]
                delta_time = time2 - time1

                fingerprint_tuple = (int(freq1), int(freq2), int(delta_time))
                fingerprints.append((fingerprint_tuple, time1))
    return fingerprints


def fingerprintBuilder_args(folder_path, fingerprints_path, **kwargs):
    database = defaultdict(list)
    c = 0
    for file_name in os.listdir(folder_path):
        if file_name.endswith(('.wav', '.mp3')):
            file_path = os.path.join(folder_path, file_name)
            c += 1
            fingerprints = generate_fingerprint(file_path, **kwargs)
            for fingerprint, time in fingerprints:
                database[fingerprint].append((file_name, time))

    with open(fingerprints_path, 'wb') as handle:
        pickle.dump(database, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"{c} fingerprints saved to {fingerprints_path}")
    
    
def fingerprintBuilder(folder_path, fingerprints_path):
    kwargs = {'WINDOW_SIZE': 1024,
              'HOP_LENGTH': 512,
              'PEAK_NEIGHBORHOOD_SIZE': 20}
    database = defaultdict(list)
    c = 0
    for file_name in os.listdir(folder_path):
        if file_name.endswith(('.wav', '.mp3')):
            file_path = os.path.join(folder_path, file_name)
            c += 1
            fingerprints = generate_fingerprint(file_path, **kwargs)
            for fingerprint, time in fingerprints:
                database[fingerprint].append((file_name, time))

    with open(fingerprints_path, 'wb') as handle:
        pickle.dump(database, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"{c} fingerprints saved to {fingerprints_path}")