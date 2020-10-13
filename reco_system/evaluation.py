from fingerprint import fingerprint_song, match_song
import re
import os
import sys
import pandas as pd

sys.path.append('../')


def get_metrics(folder="../data/songs/samples_test", output="predictions.csv"):
    """
    Evaluate the model on samples
    """
    # get filenames
    files = os.listdir(folder)
    tests = []
    
    for file in files:
        filename, extension = os.path.splitext(file)

        if extension == ".wav":
            # do fingerprinting
            filepath = os.path.join(folder, file)
            fingerprints = fingerprint_song(filepath)

            # do matching
            song, confidence, most_similar_songs = match_song(fingerprints)

            # get song name
            pattern = re.compile(r"(.+)-\[AudioTrimmer.com\]")
            result = pattern.search(filename)
            real_name = result.group(1)

            # save results
            tests.append({"song_name" : real_name, "prediction" : song["name"], "confidence" : confidence, "correct_guess" : real_name == song["name"]})

    predictions = pd.DataFrame(tests)
    predictions.to_csv(output, index=False)

    metrics = predictions["correct_guess"].value_counts(normalize=True) * 100
    accuracy = metrics[True]

    return accuracy


if __name__ == '__main__':
    accuracy_original_songs = get_metrics()
    print(accuracy_original_songs)
    accuracy_recorded_songs = get_metrics(folder="../data/songs/samples_recorded", output="predictions_recorded.csv")
    print(accuracy_recorded_songs)