import librosa
import numpy as np
from skimage.feature.peak import peak_local_max
import hashlib
import re
import os
import sys

sys.path.append('../')
from data_wrangling.db import MongoDatabase


def generate_fingerprints(samples, min_dist=4, fan_value=20, n_fft=4096):
    """
    Create the spectrogram of song, compute the highest peaks, create the fingerprints and hash them before storage

    Parameters
    ==============
    samples : the sample of the song
    min_dist : the minimum distance in pixels between 2 peaks
    fan_value : how many peaks can be connected to one
    n_fft : value used for the STFT

    Output
    ==============
    Returns the hashed fingerprints
    """

    # transform data from time-domain to frequency domain
    signal = np.abs(librosa.stft(samples, n_fft=n_fft))
    
    # get spectrograms
    signal_db = librosa.power_to_db(signal**2, ref=np.max)
    
    # get spectrograms peaks
    peaks = peak_local_max(signal_db, min_distance=min_dist)
    
    # extract fingerprints and create hashes
    idx_freq = 0
    idx_time = 1
    
    # the fingerprints must have a minimum time distance to be linked
    MIN_HASH_TIME_DELTA = 0
    MAX_HASH_TIME_DELTA = 200
    
    # the hash can be pretty long so we will only keep the first 30 characters
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

def fingerprint_song(file, song_collection, sr=44100):
    """
    Wrapper function for fingerprinting songs in a folder. This function link fingerprints with the song id.

    Parameters
    =============
    file : song to fingerprint
    song_collection : MongoDB collection to use to verify the existence of the song in the database
    sr : sample_rate used for generating the spectrogram hence the fingerprints

    Output
    =============
    Returns the hashes associated with their song_id
    """

    # get valid song name
    pattern = re.compile(r"../songs/(.+?).wav")
    result = pattern.search(file)
    
    if result is None:
        raise Exception("the filename isn't valid")
         
    song_name = result.group(1)

    # get song id to see if we can proceed with fingerprinting
    song_id = song_collection.find_one({"name" : song_name}, projection={"_id": 1})
    
    if song_id is None:
        print(result.group(1), "no match in database")
        print("==========")
        return False
    
    print(result.group(1), song_id)
    
    # do fingerprinting
    samples, sr = librosa.load(file, sr=sr)
    fingerprints = []
    hashes = generate_fingerprints(samples)
        
    for hsh, offset in hashes:
        fingerprints.append((str(song_id["_id"]), hsh, offset))
    
    return fingerprints

def batch_fingerprinting(folder="songs/"):
    """
    Fingerprint several songs in a folder

    Parameters
    ===========
    folder : location of the songs to fingerprints

    Output
    ===========
    Save the fingerprints in the fingerprints collection and update the nb of fingerprints per song
    """
    # connect to database
    mongo = MongoDatabase()
    mongo.connect()

    # get songs in WAV format
    main_dir = os.path.dirname(os.getcwd())
    songs_path = os.path.join(main_dir, folder)
    files = os.listdir(songs_path)

    # extract fingerprints from WAV files
    for file in files[5:]:
        
        filename, extension = os.path.splitext(file)
        
        if extension == ".wav":
            fingerprints_song = fingerprint_song(os.path.join(songs_path, file), mongo.db.songs)
            
            if fingerprints_song:
                print(fingerprints_song[0], len(fingerprints_song))
                
                # store fingerprints into the corresponding collection
                mongo.db.fingerprints.insert_many([{'song_id': song_id, 'hash': hash_value, 'offset' : offset} for song_id, hash_value, offset in fingerprints_song])
                
                # get fingerprints number
                mongo.db.songs.update_one({"name" : filename}, { "$set": { "nb_fingerprints": len(fingerprints_song) } })
            

if __name__ == "__main__":
    batch_fingerprinting()