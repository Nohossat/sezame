from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient
import config
import pandas as pd
import numpy as np

def connect_to_mongo():
    # save data to database
    uri_local = f"mongodb://{config.mongo_local_user}:{config.mongo_local_pwd}@{config.mongo_localhost}:{config.mongo_local_port}/?authSource=admin&readPreference=primary&ssl=false"
    
    client = MongoClient(uri_local)
    db = client.sezame
    
    return db

def get_songs(db):
    songs = db.songs
    features = {
        "acousticness" : 1,
        "danceability" : 1,
        "duration" : 1,
        "energy" : 1,
        "explicit" : 1, 
        "instrumentalness" : 1,
        "key" : 1, 
        "liveness" : 1,
        "loudness" : 1,
        "mode" : 1,
        "speechiness" : 1,
        "tempo" : 1,
        "time_signature" : 1,
        "valence" : 1,
        "_id" : 0
    }

    songs_names = list(songs.find({}, {"name" : 1, "artists" : 1, "genre" : 1, "_id" : 0}))
    songs = list(songs.find({}, features))
    df_songs = pd.DataFrame(songs)
    
    return df_songs, songs_names

def preprocessing(df):
    # one-hot encode explicit
    encoded_df = pd.get_dummies(df.explicit, prefix='explicit')

    # merge with full dataset
    full_df = pd.concat([df, encoded_df], axis=1)
    full_df.drop("explicit", axis=1, inplace=True)
    
    return full_df

def get_most_similar_songs(recognized_song, df_array):
    cosine_simil_scores = np.array(cosine_similarity(df_array, recognized_song))
        
    indexed_most_similar_songs = np.argsort(np.hstack(cosine_simil_scores))[::-1][:10]

    similar_songs = []
    for idx in indexed_most_similar_songs:
        similar_songs.append(songs_names[idx])

    return similar_songs
    

if __name__ == "__main__":
    db = connect_to_mongo()
    df_songs, songs_names = get_songs(db)
    encoded_df = preprocessing(df_songs)

    df_array = encoded_df.values

    # here I just have to get the correct format for the recognized song
    # create an auth code for spotify
    # get audio features
    # format like below and get similar songs
    recognized_song = np.array([0.539, 0.713, 369462, 0.725, 0.886, 6, 0.111, -9.951, 1, 0.0385, 122.041, 4, 0.240, 1, 0]).reshape(1, -1) # Bonobo - Linked
    similar_songs = get_most_similar_songs(recognized_song, df_array)

    print(similar_songs)





