# Flask
from flask import Flask, url_for, request, render_template, jsonify
from reco_system import app
from reco_system.fingerprint import fingerprint_song, match_song
import time
import os
import random

# we will use this endpoint to fetch the song matched
@app.route('/recognize', methods=['POST'])
def recognize(): 
    start = time.time()

    # load file
    file_path = request.json[1]['audio']['path']
    print(file_path)

    confidence_threshold = float(request.json[0]["confidence_thres"])
    filename = open(file_path, 'rb')
    
    # create wav file
    current_dir = os.getcwd()
    rand_nb = int(round(random.random(), 4) * 10000)

    # for testing purposs
    # path = f"reco_system/uploads/ONE OF US-[AudioTrimmer.com]-{rand_nb}.wav"
    path = f"reco_system/uploads/sample-{rand_nb}.wav"
    new_file = os.path.join(current_dir, path)

    with open(new_file, "wb") as aud:
        aud_stream = filename.read()
        aud.write(aud_stream)

    # extract fingerprints
    fingerprints = fingerprint_song(new_file)

    # remove the file 
    os.remove(new_file)
  
    # get matched song
    song, confidence, most_similar_songs = match_song(fingerprints, confidence_threshold)

    end = time.time()

    return jsonify({"matched_song" : song, "time" : end - start, "confidence" : confidence, "similar_songs" : most_similar_songs})
