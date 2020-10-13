import pytest
import librosa
import numpy as np
from skimage.feature.peak import peak_local_max
import hashlib
import re
import os
import sys

from data_wrangling.fingerprinting import generate_fingerprints, fingerprint_song
from data_wrangling.db import MongoDatabase

def test_generate_fingerprints():
    main_dir = os.getcwd()
    filepath = os.path.join(main_dir, "data/songs/WAP (feat. Megan Thee Stallion).wav")
    samples, sr = librosa.load(filepath, sr=44100)
    hashes = generate_fingerprints(samples)
    assert len(hashes) == 9492, "the number of hashes should be 9492"

def test_fingerprint_song():
    main_dir = os.getcwd()
    filepath = os.path.join(main_dir, "data/songs/WAP (feat. Megan Thee Stallion).wav")
    mongo = MongoDatabase()
    mongo.connect()
    hashes = fingerprint_song(filepath, mongo.db, save_to_mongo=False)
    assert len(hashes) == 9492, "the number of hashes should be 9492"
    assert hashes[0][0] == "5f7d934a37d3e67dcca32476", "the song_id is 5f7d934a37d3e67dcca32476"
    