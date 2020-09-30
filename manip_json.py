"""
We get the Spotify Top 50 songs main info. We previously got the songs info with a CURL command. 
"""

import json

with open("spotify_playlist.json", "r") as f:
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

print(tracks_info)

with open("spotify_playist_info.json", "w") as f:
    json.dump(tracks_info, f, indent=2)
