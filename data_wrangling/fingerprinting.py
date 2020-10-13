import librosa
import numpy as np
from skimage.feature.peak import peak_local_max
import hashlib
import re
import os
import sys
import argparse

sys.path.append('../')
from data_wrangling.db import MongoDatabase


def generate_fingerprints(samples, min_dist=14, fan_value=22, n_fft=4096, is_dict=False):
    """
    Create the spectrogram of song, compute the highest peaks, create the fingerprints and hash them before storage

    Parameters
    ==============
    samples : the sample of the song
    min_dist : the minimum distance in pixels between 2 peaks
    fan_value : how many peaks can be connected to one
    n_fft : value used for the STFT
    is_dict : if indicates if a dictionary with hash as key must be returned

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
    MIN_HASH_TIME_DELTA = 10
    MAX_HASH_TIME_DELTA = 200
    
    # the hash can be pretty long so we will only keep the first 30 characters
    FINGERPRINT_REDUCTION = 30
    
    if is_dict :
        hashes = {}
    else : 
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
                    if is_dict :
                        hashes[h.hexdigest()[0:FINGERPRINT_REDUCTION]] = int(t1) # {hash : time_offset}
                    else : 
                        hashes.append((h.hexdigest()[0:FINGERPRINT_REDUCTION], int(t1))) # (hash, time_offset)
    if is_dict:
        return hashes
    return set(hashes)

def fingerprint_song(file, db, sr=44100, save_to_mongo=False):
    """
    Wrapper function for fingerprinting songs in a folder. This function link fingerprints with the song id.

    Parameters
    =============
    file : song to fingerprint
    db : MongoDB database
    sr : sample_rate used for generating the spectrogram hence the fingerprints

    Output
    =============
    Returns the hashes associated with their song_id
    """

    # get valid song name
    file_elements = file.split("/")
    filename = file_elements[len(file_elements) - 1]
    pattern = re.compile(r"(.+?).wav")
    result = pattern.search(filename)
    
    if result is None:
        raise Exception("the filename isn't valid")
         
    song_name = result.group(1)

    # get song id to see if we can proceed with fingerprinting
    song_id = db.songs.find_one({"name" : song_name}, projection={"_id": 1})
    
    if song_id is None:
        print(song_name, "no match in database")
        print("==========")
        return False
    
    print(result.group(1), song_id)
    
    # do fingerprinting
    samples, sr = librosa.load(file, sr=sr)
    fingerprints = []
    hashes = generate_fingerprints(samples)
        
    for hsh, offset in hashes:
        fingerprints.append((str(song_id["_id"]), hsh, offset))

    # save to mongo if necessary
    if save_to_mongo and fingerprints:
        # store fingerprints into the corresponding collection
        db.fingerprints.insert_many([{'song_id': song_id, 'hash': hash_value, 'offset' : offset} for song_id, hash_value, offset in fingerprints])
        # get fingerprints number
        db.songs.update_one({"name" : song_name}, { "$set": { "nb_fingerprints": len(fingerprints) } })

    print(len(fingerprints))
    return fingerprints

def batch_fingerprinting(folder="data/songs/"):
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
    for file in files:
        filename, extension = os.path.splitext(file)
        
        if extension == ".wav":
            fingerprints_song = fingerprint_song(os.path.join(songs_path, file), mongo.db, save_to_mongo=True)
            if fingerprints_song:
                print(fingerprints_song[0], len(fingerprints_song))
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fingerprint Songs\n")
    
    parser.add_argument(
        '-f', '--file', help='fingerprint the song at this location', default=False)
    parser.add_argument(
        '-d', '--directory', help='fingerprint songs lcoated in a folder', default=False)
    
    args = parser.parse_args()

    if args.file:
        assert(os.path.exists(args.file)), "The file doesn't exist"
        filename, extension = os.path.splitext(args.file)
        assert(os.path.isfile(args.file) and extension == ".wav"), "It must be a WAV file"

        mongo = MongoDatabase()
        mongo.connect()
        fingerprint_song(args.file, mongo.db, save_to_mongo=True)

    elif args.directory:
        main_dir = os.path.dirname(os.getcwd())
        songs_path = os.path.join(main_dir, args.directory)
        assert(os.path.exists(songs_path)), "The directory doesn't exist"
        batch_fingerprinting(folder=args.directory)