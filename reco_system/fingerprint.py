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

def generate_fingerprints(samples, sr=44100, min_dist=3, fan_value=15, n_fft=4096):
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

    Parameters
    ==============
    fingerprints: the fingerprints of the sample song

    Output
    ==============
    The most similar song with the confidence level
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
                found_hashes.append([fingerprint[0], fingerprint[1] - element["offset"], element["song_id"]])


    found_hashes = pd.DataFrame(found_hashes, columns=["hash", "offset_difference", "song_id"])
    total_results = found_hashes.shape[0]

    # we will take 2 parameters into account:
    # - the variance in the offset difference
    # - the number of fingerprints
    
    # first song with less variance
    found_hashes_var = found_hashes.groupby(by=["song_id"]).var()
    found_hashes_var = found_hashes_var.sort_values(by='offset_difference', ascending=False)
    first_choice_var = found_hashes_var.index.values[0]
    found_hashes_var.to_csv("found_var.csv")

    sorted_hashes = found_hashes["song_id"].value_counts()
    sorted_hashes.to_csv("sorted_found.csv")

    # we can compute the confidence level of the most similar song
    confidence = int(sorted_hashes[first_choice_var]) / total_results
    
    if confidence < 0.35:
        # we take a 20% confidence threshold in order to consider the song as a valid answer
        song_guessed = db.songs.find_one({"_id" : ObjectId(first_choice_var)}, {"name" : 1, "artists" : 1, "_id" : 0})
        print(song_guessed)
        return "No result", confidence

    song = db.songs.find_one({"_id" : ObjectId(first_choice_var)}, {"name" : 1, "artists" : 1, "_id" : 0})
    

    print(f"result : {song}, confidence : {confidence}")
    return song, confidence

