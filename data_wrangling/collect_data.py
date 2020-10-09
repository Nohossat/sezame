"""
We get the Spotify Top 50 songs main info. We previously got the songs info with a CURL command. 
"""

import json
from pymongo import MongoClient
import config
import requests
import os

def fetch_data(url):
    """
    Fetch data from Spotify API

    Parameters
    ==============
    url : endpoint

    Output
    ==============
    JSON response
    """

    headers = {'Authorization': f'Bearer {config.spotify_auth}'}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise Exception('erreur: {}'.format(resp.status_code))
    else:
        result = resp.json()
    
    return result

def get_playlist_info(playlist_id, genre, filename=None):
    """
    Make an API call to get the Spotify Playlist Info

    Parameters
    ===========
    playlist_id : the Spotify ID to fetch
    genre : playlist genre
    filename : file to output the result to

    Output
    ===========
    None

    """
    result = fetch_data(url)
    keep_relevant_spotify_info(filename, data=result, genre=genre)

def keep_relevant_spotify_info(output_file=None, input_file=None, data=None, genre=None, save_mongo=True):
    """
    From Spotify API Playlist Response, keep the relevant info

    Parameters:
    =============
    output_file : JSON file to output the result
    input_file : Load data from an external JSON file
    data : JSON information about the playlist
    save_mongo : flag to keep the relevant directly to database

    Output
    =============
    Save in an external JSOn file or in a MongoDB colelction the info
    """

    if input_file is not None:
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
        try:
            info["image"] = track["track"]["album"]["images"][0]["url"]
        except :
            info["image"] = "N/A"

        info["spotify_id"] = track["track"]["id"]
        info["preview"] = track["track"]["preview_url"]
        info["genre"] = genre
        tracks_info.append(info)

    if save_mongo:
        # save data to database
        uri_local = f"mongodb://{config.mongo_local_user}:{config.mongo_local_pwd}@{config.mongo_localhost}:{config.mongo_local_port}/?authSource=admin&readPreference=primary&ssl=false"
        
        client = MongoClient(uri_local)
        db = client.sezame
        try:
            db.songs.insert_many(tracks_info, ordered=False)
        except Exception as e:
            print(e)
    else :
        with open(output_file, "w") as f:
            json.dump(tracks_info, f, indent=2)

def get_audio_features(track_id=None):
    """
    We will use the spotify API to get the audio features for all the songs in the database or for a given track_id

    Parameters:
    ================
    track_id : Spotify ID for a given track

    Output:
    ===============
    audio features saved in a mongoDB database
    """

    if track_id is None:
        # connect to MongoDB
        uri_local = f"mongodb://{config.mongo_local_user}:{config.mongo_local_pwd}@{config.mongo_localhost}:{config.mongo_local_port}/?authSource=admin&readPreference=primary&ssl=false"
        client = MongoClient(uri_local)
        db = client.sezame

        # get Spotify Tracks ids
        spotify_ids = db.songs.find({}, {"spotify_id" : 1, "_id" : 0})
        all_ids = [item["spotify_id"] for item in spotify_ids]
        limit = len(all_ids)
        
        # the url only accept 100 ids at a time, so we will use batch ids
        for i in range(0, 1370, 100):
            if i + 100 < limit:
                batch = ','.join(all_ids[i:i+100])
            else:
                batch = ','.join(all_ids[i:limit])

            url = f"https://api.spotify.com/v1/audio-features/?ids={batch}"
            
            # get audio features
            result = fetch_data(url)

            # keep relevant info 
            for audio_feat in result["audio_features"]:
                save_audio_features(audio_feat, db.songs)
    else:
        # get audio features and save to database
        url = "https://api.spotify.com/v1/audio-features/{track_id}"
        result = fetch_data(url)
        save_audio_features(result, db.songs)

def save_audio_features(result, collection):
    """
    Update the song document in MongoDB with its audio features

    Parameters
    ============
    result: the audio features fetched with a Spotify API call
    collection: collection to save the features in

    Output
    ============
    None - save data to given collection
    """
    result_id = result.pop("id")
    result.pop("type")
    result.pop("uri")
    result.pop("track_href")
    result.pop("analysis_url")

    # save to database
    try:
        collection.update_one({"spotify_id" : result_id}, { "$set" : result })
    except Exception as e:
        print(e)

def get_songs_from_playlists(filename="data/playlist_ids.json"):
    """
    Fetch a list of Spotify playlists Id 
    and get the songs relative information

    Parameters
    ============
    filename : path from which we can fetch the playlist Spotify Ids

    Output
    ============
    None
    """
    current_dir = os.path.dirname(os.getcwd())

    with open(os.path.join(current_dir, filename), "r") as fp:
        playlists = json.load(fp)

        for playlist in playlists:
            get_playlist_info(playlist_id=playlist["id"], genre=playlist["genre"])

if __name__ == "__main__":
    get_audio_features()