from collections import defaultdict, Counter
import pickle
from audio_fingerprint import generate_fingerprint

import os
import numpy as np
from skimage.feature import peak_local_max
from scipy.ndimage import maximum_filter
from collections import defaultdict
import librosa

def match_fingerprints(query_fingerprints, database):
    matches = defaultdict(list)
    for fingerprint, t in query_fingerprints:
        if fingerprint in database:
            for file_name, db_t in database[fingerprint]:
                offset = db_t - t
                matches[file_name].append(offset)
    # scores = []
    scores = {}
    for file_name, offsets in matches.items():
        _, count = Counter(offsets).most_common(1)[0]
        scores[file_name] = count

    tops = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
    return tops

def identify_audio(query_audio_path, database):
    query_fingerprints = generate_fingerprint(query_audio_path)
    top_results = match_fingerprints(query_fingerprints, database)
    
    for rank, (file_name, score) in enumerate(top_results, start=1):
        print(f"{rank}. {file_name} (Score: {score})")

    return top_results

def audioIdentification_args(queryset_path, fingerprints_path, output_path, **kwargs):
    
    with open(fingerprints_path, 'rb') as handle:
        fingerprints_db = pickle.load(handle)
    
    with open(output_path, "w") as f:
        
        for file_name in os.listdir(queryset_path):
            if file_name.endswith(('.wav', '.mp3')):
                file_path = os.path.join(queryset_path, file_name)
                query_fingerprints = generate_fingerprint(file_path, **kwargs)
                top_results = match_fingerprints(query_fingerprints, fingerprints_db)
                
                f.write(f"{file_name}")
                print(top_results)
                for rank, (pred_file_name, score) in enumerate(top_results, start=1):
                    f.write(f" {pred_file_name}")
                f.write("\n")
    print(f'written into {output_path}')
                
def audioIdentification(queryset_path, fingerprints_path, output_path):
    kwargs = {'WINDOW_SIZE': 1024,
              'HOP_LENGTH': 512,
              'PEAK_NEIGHBORHOOD_SIZE': 20}
    with open(fingerprints_path, 'rb') as handle:
        fingerprints_db = pickle.load(handle)
    
    with open(output_path, "w") as f:
        
        for file_name in os.listdir(queryset_path):
            if file_name.endswith(('.wav', '.mp3')):
                file_path = os.path.join(queryset_path, file_name)
                query_fingerprints = generate_fingerprint(file_path, **kwargs)
                top_results = match_fingerprints(query_fingerprints, fingerprints_db)
                
                f.write(f"{file_name}")
                print(top_results)
                for rank, (pred_file_name, score) in enumerate(top_results, start=1):
                    f.write(f" {pred_file_name}")
                f.write("\n")