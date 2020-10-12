# Sezame

## Goal

Sezame is a Shazam similar application. It captures a sound and tries to match it with a song in the database and gives back recommendations for the user.

## How does it work ?

Click on the play button to start recording the surrounding sounds. The application streams the sound : it sends some seconds to be analyzed by the Flask API. This API will try to match the sample with the fingerprints in the database. If a good match occurs (confidence level at 60%), the song and similar songs are returned to the main application.

## Installation

Main application : Next.js
Audio recognition API : Flask
Database : MongoDB

We contained the application with Docker. So make sure to have it installed before launching the application.

```shell
git clone https://github.com/Nohossat/sezame.git
cd sezame
docker-compose up --build
```

This commands will fetch the GitHub repository and create the application. The database will be populated with 1371 songs, among them 100 with fingerprints. The audio recognition only works on them. 

From there, you can go to http://localhost:3000 and use the application. To know which songs can be matched, you can see it in mongoDB, with the following commands: 

```js
{'nb_fingerprints' : { $exists : true }}
```

You can also see the default fingerprinted songs in the file : **songs_fingerprinted.json**.

## Customize your application

### How to add songs to the MongoDB database ?

If you want to populate your databases with more songs, you can either fetch more song information to have a better recommendation system or add more fingerprints to match more songs.

#### How to fetch new songs from Spotify API ?

##### Get a Spotify Token

We use the Spotify API to get information about the songs we want to store. 
Please follow this [link](https://developer.spotify.com/documentation/web-api/quick-start/) to get the authorization token needed to communicate with the API.

##### Get some info about the songs

During the project, I decided to use Playlists Ids to fetch several songs at once but you can also do it with any Spotify ID.

You can store the playlists IDs in a JSON with the following format : 

```json
[
    {
        "name": "African Heat",
        "id": "37i9dQZF1DWYkaDif7Ztbp",
        "genre" : "afro"
    },
    {
        "name": "Top Pop",
        "id": "37i9dQZF1DX92MLsP3K1fI",
        "genre" : "pop"
    }
]
```

To get the information, run the following command : 

**For a song :**

```shell
python collect_data.py -s "10lGufP5RmCsUwKDTcPpxs" -g "downtempo" # track id for Hedron from the artist Bonobo
```

**For a playlist :**

```shell
python collect_data.py -s "/data/playlists_ids.json" # file with the playlists ids
```

#### Get songs fingerprints

To get the fingerprints for any song, you need to get the song in a WAV format first.

```shell
python fingerprinting.py -f "/path/to/song" # fingerprint a song
python fingerprinting.py -d "/path/to/folder_songs" # fingerprints several songs
```
