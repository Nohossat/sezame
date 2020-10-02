/* add query to create a database */

CREATE TABLE IF NOT EXISTS songs(
    song_id SERIAL PRIMARY KEY,
    song_name VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    nb_fingerprints BIGINT,
    date_created TIMESTAMP NOT NULL DEFAULT NOW(),
    date_modified TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS fingerprints(
    f_hash BYTEA,
    song_id INT NOT NULL,
    offset_time INT NOT NULL,
    date_created TIMESTAMP NOT NULL DEFAULT NOW(),
    date_modified TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_fk UNIQUE (song_id, offset_time, f_hash),
    CONSTRAINT fk_song
        FOREIGN KEY(song_id)
            REFERENCES songs(song_id)
); 

CREATE INDEX IF NOT EXISTS hash_idx ON fingerprints(f_hash);
