# Data manipulation
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity


import sys
sys.path.append('../')

# Database connection
from pymongo import MongoClient
import data_wrangling.config as config
from bson.objectid import ObjectId


def connect_to_mongo():
    # save data to database
    uri_local = f"mongodb://{config.mongo_local_user}:{config.mongo_local_pwd}@{config.mongo_localhost}:{config.mongo_local_port}/?authSource=admin&readPreference=primary&ssl=false"
    
    client = MongoClient(uri_local)
    db = client.sezame
    
    return db

def get_songs(db, matched_song_id=None):
    """
    Get songs from the database with relevant features for cosine similarity operation

    Parameters
    ===============
    db : MongoDB database hosting the data
    matched_song_id : matched song MongoDB id 

    Output
    ===============
    The program returns the songs features and their names
    """

    songs = db.songs

    if matched_song_id is None:
        query = {}
    else :
        query = {"_id" : { "$ne" : ObjectId(matched_song_id) }} 

    songs = list(songs.find(query))
    
    return songs

def preprocessing(df, enc=None):
    # one-hot encode genre
    if enc is None:
        enc = OneHotEncoder(handle_unknown='error', drop='first')
        enc.fit(df[["genre"]])

    genres = enc.transform(df[["genre"]]).toarray()
    encoded_genres = pd.DataFrame(genres, columns=enc.categories_[0][1:])

    encoded_df = pd.concat([df, encoded_genres], axis=1)
    encoded_df.drop("genre", axis=1, inplace=True)

    return encoded_df.values, enc

def get_most_similar_songs(db, recognized_song):

    # keep only useful features for the matched song
    features = [
        "duration",
        "explicit",
        "genre",
        "acousticness",
        "danceability",
        "energy",
        "instrumentalness",
        "key",
        "liveness",
        "loudness",
        "mode",
        "speechiness",
        "tempo",
        "time_signature",
        "valence",
    ]

    song_info_keys = ["name", "artists", "genre"]

    matched_song_id = str(recognized_song["_id"])

    matched_song = dict()
    for feature in features:
        matched_song[feature] = recognized_song[feature]

    # transform the matched_song values into a DataFrame
    matched_song_df = pd.DataFrame(matched_song, index=[0])

    # get all songs from the database
    songs = get_songs(db, matched_song_id)

    songs_features_list = []
    songs_names = []

    for song in songs:
        song_features = { k:v for (k, v) in song.items() if k in features}
        song_info = list(map(song.get, song_info_keys))
        songs_features_list.append(song_features)
        songs_names.append(song_info)

    song_features_df = pd.DataFrame(songs_features_list)

    # preprocessing
    encoded_songs, enc = preprocessing(song_features_df)
    encoded_matched_song, _ = preprocessing(matched_song_df, enc)
    
    # compute cosine similarity scores
    cosine_simil_scores = np.array(cosine_similarity(encoded_songs, encoded_matched_song.reshape(1, -1)))
    indexed_most_similar_songs = np.argsort(np.hstack(cosine_simil_scores))[::-1][:10]

    # get similar songs names and genres
    similar_songs = []
    
    for idx in indexed_most_similar_songs:
        similar_songs.append(songs_names[idx])
        print(songs_names[idx])

    return similar_songs
    

if __name__ == "__main__":
    db = connect_to_mongo()

    recognized_song = db.songs.find_one({"_id" : ObjectId("5f7d91439fcf6858e3cae166")}) # afro
    similar_songs = get_most_similar_songs(db, recognized_song)





