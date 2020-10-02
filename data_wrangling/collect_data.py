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
        tracks_info.append(info)

    with open(output_file, "w") as f:
        json.dump(tracks_info, f, indent=2)

def save_data_to_db(songs_json):
    """
    Collect song information to store them in a MongoDB Atlas Instance
    """

    with open(songs_json, "r") as f:
        data = json.load(f)
    
    print(data)
    client = MongoClient(f"mongodb+srv://{config.mongo_user}:{config.mongo_pwd}@{config.mongo_host}/?retryWrites=true&w=majority")

    # sezame db
    db = client.sezame

    # songs collection
    collection = db.songs


if __name__ == "__main__":
    # keep_relevant_spotify_info("spotify_playlist.json", "spotify_playist_info.json")
    save_data_to_db("../data/spotify_playist_info.json")