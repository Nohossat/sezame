# Sezame

## Goal

Sezame is a Shazam similar application. It captures a sound and tries to match it with a song in the database and gives back recommendations for the user.

## Installation

For the main application, we used Next.js and for the audio recognition we used the Flask framework.

Docker install

## How does it work ?

Click on the play button to start recording the surrounding sounds. The application streams the sound : it sends some seconds to be analyzed by the Flask API. This API will try to match the sample with the fingerprints in the database. If a good match occurs (confidence level at 60%), the song and similar songs are returned to the main application.


## Metrics

We used 100 samples from several songs to test the fingerprinting matching. 

TBD