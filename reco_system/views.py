# Flask
from flask import Flask, url_for, request, render_template, jsonify
from reco_system import app
from reco_system.fingerprint import fingerprint_song, match_song
import time

# we will use this endpoint to fetch the song matched
@app.route('/recognize', methods=['POST'])
def recognize(): 
    start = time.time()
    # load file
    file_path = request.json["audio"]["path"]
    file = open(file_path, 'rb')
   
    # create wav file
    with open("sample.wav", "wb") as aud:
        aud_stream = file.read()
        aud.write(aud_stream)

    # extract fingerprints
    fingerprints = fingerprint_song("sample.wav")

    # get matched song
    song, confidence = match_song(fingerprints)
    end = time.time()

    return jsonify({"song" : song, "time" : end - start, "confidence" : confidence})
