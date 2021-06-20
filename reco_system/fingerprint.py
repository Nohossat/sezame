# Music processing
import librosa
from skimage.feature.peak import peak_local_max

# Utils
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
from reco_system.recommendation import get_most_similar_songs


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

    fingerprints = generate_fingerprints(samples, is_dict=True)
    print(f"nb fingerprints : {len(fingerprints)}")

    return fingerprints


def send_not_found(confidence=None):
    """
    Return a not found object

    Parameters
    =============
    confidence : if this parameter is None, we reset it to 0

    Output
    =============
    A not found object
    """

    if confidence is None:
        confidence = 0

    song_info = {
        "name": "No result",
        "artists": "Anonymous",
        "genre": "None",
        "preview": 0,
        "cover": "https://m.media-amazon.com/images/I/71OFozfY-cL._SS500_.jpg"
    }

    print(f"result : {song_info}")
    return song_info, confidence, []


def match_song(fingerprints, confidence_thres=0.002):
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
    mongo = MongoDatabase()
    mongo.connect()

    found_hashes = []

    # save matched fingerprints and offsets differences in found hashes array
    hashes = list(fingerprints.keys())
    total_results = list(mongo.db.fingerprints.find({"hash": {"$in": hashes}}))
    differences = []

    for result in total_results:
        sample_offset = fingerprints[result["hash"]]
        differences.append(result["offset"] - sample_offset)
        found_hashes.append([result["hash"], result["offset"] - sample_offset, result["song_id"]])

    nb_results = len(found_hashes)

    # if no result, we return a 404 not found
    if nb_results == 0:
        return send_not_found()

    # we will compare the song_id with the most hashes and the songId with the hashes the most aligned
    found_hashes = pd.DataFrame(found_hashes, columns=["hash", "offset_difference", "song_id"])
    found_hashes.to_csv("found_hashes.csv")

    # take the 5 songs with the most hashes matched
    sorted_hashes = found_hashes["song_id"].value_counts()
    sorted_hashes.to_csv("sorted_hashes.csv")
    sorted_hashes = sorted_hashes.head()
    most_matched_songs = sorted_hashes.index.values
    first_choice = most_matched_songs[0]
    print(first_choice)

    # we make a double verification with the offset difference
    selected_songs = found_hashes.loc[found_hashes["song_id"].isin(most_matched_songs)]
    found_hashes_groupedby_songid = selected_songs.groupby(by=["song_id", "offset_difference"]).size().to_frame('size')
    most_probable_song = found_hashes_groupedby_songid["size"].idxmax()[0]
    found_hashes_groupedby_songid.to_csv("hashes_grouped.csv")
    print(most_probable_song)

    if first_choice == most_probable_song:
        print("strong probability it is our guess")

    # we can compute the confidence level of the matched song
    confidence = round(int(sorted_hashes[first_choice]) / nb_results, 3)

    print(sorted_hashes[first_choice])
    print(confidence)
    if confidence < confidence_thres:
        return send_not_found(confidence=confidence)

    # Fetch recommendations if the confidence level is ok
    song = mongo.db.songs.find_one({"_id": ObjectId(first_choice)})
    most_similar_songs = get_most_similar_songs(mongo.db, song)

    song_info = {
        "name": song["name"],
        "artists": song["artists"],
        "genre": song["genre"],
        "preview": song["preview"],
        "cover": song["image"]
    }

    # print(f"song_matched : {song_info}, confidence : {confidence}, recommendation : {most_similar_songs}")
    return song_info, confidence, most_similar_songs
