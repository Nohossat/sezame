# Music processing
from skimage.feature.peak import peak_local_max
import librosa

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

sys.path.append('../')
import data_wrangling.config as config
from data_wrangling.fingerprinting import generate_fingerprints
from data_wrangling.db import MongoDatabase
from .recommendation import get_most_similar_songs


def fingerprint_song(file):
    """
    Fingerprint the recorded song

    Parameters
    =============
    file : the path of the file recorded

    Output
    =============
    Returns the fingerprints of the recorded song
    """

    samples, _ = librosa.load(file, sr=44100)

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
    The song matched with confidence level and some recommendations
    """

    # connect to database
    db = MongoDatabase()
    db.connect()

    found_hashes = []

    # a sample fingerprint is like (hash, offset)
    for fingerprint in fingerprints:
        result = db.fingerprints.find({"hash" : fingerprint[0]})

        if result is not None:
            for element in result:
                found_hashes.append([fingerprint[0], fingerprint[1] - element["offset"], element["song_id"]])


    found_hashes = pd.DataFrame(found_hashes, columns=["hash", "offset_difference", "song_id"])
    total_results = found_hashes.shape[0]
    
    # first song with less variance in the offset differences
    found_hashes_var = found_hashes.groupby(by=["song_id"]).var()
    found_hashes_var = found_hashes_var.sort_values(by='offset_difference', ascending=False)
    first_choice_var = found_hashes_var.index.values[0]
    found_hashes_var.to_csv("found_var.csv")

    sorted_hashes = found_hashes["song_id"].value_counts()
    sorted_hashes.to_csv("sorted_found.csv")

    # we can compute the confidence level of the matched song
    confidence = int(sorted_hashes[first_choice_var]) / total_results
    
    if confidence < 0.20:
        # we take a 20% confidence threshold in order to consider the song as a valid answer
        song_guessed = db.songs.find_one({"_id" : ObjectId(first_choice_var)})
        most_similar_songs = get_most_similar_songs(db, song_guessed)
        
        song_info = {
           "name": "No result", 
           "artists" : "Anonymous", 
           "genre" : "None",
           "preview" : 0,
           "cover" : "https://m.media-amazon.com/images/I/71OFozfY-cL._SS500_.jpg"
        }

        print(f"result : {song_info}, confidence : {confidence}, recommendation : {most_similar_songs}")
        return  song_info, confidence, most_similar_songs

    song = db.songs.find_one({"_id" : ObjectId(first_choice_var)})
    
    # get most_similar songs
    most_similar_songs = get_most_similar_songs(db, song)
    
    song_info = {
           "name": song["name"], 
           "artists" : song["artists"], 
           "genre" : song["genre"],
           "preview" : song["preview"],
           "cover" : song["image"]
    }
    
    print(f"song_matched : {song_info}, confidence : {confidence}, recommendation : {most_similar_songs}")
    return song_info, confidence, most_similar_songs

