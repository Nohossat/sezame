import pytest
from reco_system.fingerprint import fingerprint_song, send_not_found, match_song
import os

def test_fingerprint_song():
    main_dir = os.getcwd()
    filepath = os.path.join(main_dir, "data/songs/WAP (feat. Megan Thee Stallion).wav")
    fingerprints = fingerprint_song(filepath)
    assert len(fingerprints) == 9470, "the fingerprints format isn't correct"

def test_send_not_found():
    song_info, confidence, similar_songs = send_not_found(confidence=None)
    assert similar_songs == [], "the list of similar songs should be empty"
    assert song_info["name"] == "No result", "the song name should be No result"
    assert confidence == 0, "the confidence level should be at 0"

def test_match_song():
    main_dir = os.getcwd()
    filepath = os.path.join(main_dir, "data/songs/WAP (feat. Megan Thee Stallion).wav")
    fingerprints = fingerprint_song(filepath)
    song_info, confidence, most_similar_songs = match_song(fingerprints)
    assert song_info["name"] == "WAP (feat. Megan Thee Stallion)", "the song name should be Back Door"