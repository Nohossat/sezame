# Music processing
from skimage.feature.peak import peak_local_max
import librosa
import librosa.display

#Utils
import matplotlib.pyplot as plt
import numpy as np
import hashlib
import sys
import os 
import re
import pandas as pd

# Database
from pymongo import MongoClient
from bson.objectid import ObjectId

data_wrangling_path = os.path.join(os.getcwd(), "data_wrangling")
sys.path.append(data_wrangling_path)

import data_wrangling.config as config

def generate_fingerprints(samples, sr=44100, min_dist=5, fan_value=15, n_fft=4096):
   # transform data from time-domain to frequency domain
    signal = np.abs(librosa.stft(samples, n_fft=n_fft))
    
    # get log spectrum
    signal_db = librosa.power_to_db(signal**2, ref=np.max)
    
    # get spectrograms peaks
    peaks = peak_local_max(signal_db, min_distance=min_dist)
    print(f"nb peaks : {len(peaks)}")
    
    # extract fingerprints and create hashes
    idx_freq = 0
    idx_time = 1
    
    MIN_HASH_TIME_DELTA = 0
    MAX_HASH_TIME_DELTA = 200
    FINGERPRINT_REDUCTION = 30
    
    hashes = []
    
    for i in range(len(peaks)):
        for j in range(1, fan_value): 
            if (i + j) < len(peaks):
                freq1 = peaks[i][idx_freq]
                freq2 = peaks[i + j][idx_freq]
                t1 = peaks[i][idx_time]
                t2 = peaks[i + j][idx_time]
                t_delta = t2 - t1
            
                if MIN_HASH_TIME_DELTA <= t_delta <= MAX_HASH_TIME_DELTA:
                    h = hashlib.sha1(f"{str(freq1)}|{str(freq2)}|{str(t_delta)}".encode('utf-8'))
                    hashes.append((h.hexdigest()[0:FINGERPRINT_REDUCTION], int(t1))) # hash and time_offset
    
    return hashes

def fingerprint_song(file, sr=44100):
    samples, sr = librosa.load(file, sr=sr)
    duration = librosa.get_duration(y=samples, sr=sr) 
    print(f"durée : {duration}")
    fingerprints = generate_fingerprints(samples)
    f = pd.DataFrame(fingerprints, columns=["hash", "offset"])
    f.to_csv("sample_fingerprints.csv")
    print(f"nb fingerprints : {len(fingerprints)}")

    return fingerprints

def match_song(fingerprints):
    """
    Match sample fingerprints with the ones in the database => get the most similar song id
    """

    uri_local = f"mongodb://{config.mongo_local_user}:{config.mongo_local_pwd}@{config.mongo_localhost}:{config.mongo_local_port}/?authSource=admin&readPreference=primary&ssl=false"
    uri_cloud = f"mongodb+srv://{config.mongo_user}:{config.mongo_pwd}@{config.mongo_host}/?retryWrites=true&w=majority"
    client = MongoClient(uri_local)
    
    db = client.sezame

    found_hashes = []

    # a sample fingerprint is like (hash, offset)
    for fingerprint in fingerprints:
        result = db.fingerprints.find({"hash" : fingerprint[0]})

        if result is not None:
            for element in result:
                found_hashes.append([fingerprint[0], fingerprint[1], element["song_id"], element["offset"], element["_id"]])


    found_hashes = pd.DataFrame(found_hashes, columns=["hash", "offset_sample", "song_id", "offset_db", "db_id"])
    found_hashes.to_csv("found.csv")
    total_results = found_hashes.shape[0]
    print(total_results)
    sorted_hashes = found_hashes["song_id"].value_counts()
    sorted_hashes.to_csv("sorted_found.csv")
    song_matched_id = sorted_hashes.index.values[0]

    song = db.songs.find_one({"_id" : ObjectId(song_matched_id)}, {"name" : 1, "artists" : 1, "_id" : 0})
    confidence = int(sorted_hashes.values[0]) / total_results
    print(f"result : {song}, confidence : {confidence}")

    return song, confidence

