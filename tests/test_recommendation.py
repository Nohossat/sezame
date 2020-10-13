import pytest
from reco_system.recommendation import get_songs, get_most_similar_songs
import os
from data_wrangling.db import MongoDatabase
from bson.objectid import ObjectId

def test_get_songs():
    mongo = MongoDatabase()
    mongo.connect()
    song = get_songs(mongo.db, "5f8076f63f80ec807d05ab89")
    assert song[0]["name"] == "THERE FOR YOU", "the song format isn't correct"


def test_get_most_similar_songs():
    mongo = MongoDatabase()
    mongo.connect()
    recognized_song = mongo.db.songs.find_one({"_id" : ObjectId("5f8076f63f80ec807d05ab89")})
    similar_songs = get_most_similar_songs(mongo.db, recognized_song)
    assert len(similar_songs) == 8, "We should have 8 recommended songs"
