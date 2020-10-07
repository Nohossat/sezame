"""
We get the Spotify Top 50 songs main info. We previously got the songs info with a CURL command. 
"""

import json
from pymongo import MongoClient
import config


def keep_relevant_spotify_info(input_file, output_file):
    with open(input_file, "r") as f:
        data = json.load(f)

    tracks = data["tracks"]["items"]

    tracks_info = list()

    for track in tracks:
        info = dict()
        info["name"] = track["track"]["name"]
        info["artists"] = [artist["name"] for artist in track["track"]["artists"]]
        info["duration"] = track["track"]["duration_ms"]
        info["explicit"] = track["track"]["explicit"]
        info["image"] = track["track"]["album"]["images"][0]["url"]
        info["spotify_id"] = track["track"]["id"]
        info["preview"] = track["track"]["preview_url"]
        tracks_info.append(info)

    with open(output_file, "w") as f:
        json.dump(tracks_info, f, indent=2)

def get_tracks_id(playlist_id):
    """
    Get Spotify tracks id from Spotify Playlist Id
    """
    pass


def get_audio_features(track_id):
    
if __name__ == "__main__":
    keep_relevant_spotify_info("../data/spotify_playlist.json", "../data/spotify_playist_info.json")