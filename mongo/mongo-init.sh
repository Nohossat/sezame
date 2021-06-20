#!/bin/sh

mongo --eval "db.createUser({ user: '$MONGO_INITDB_ROOT_USERNAME', pwd: '$MONGO_INITDB_ROOT_PASSWORD', roles: [{ role: 'readWrite', db: '$MONGO_INITDB_DATABASE' }] });"
mongoimport --drop songs.json -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase $MONGO_INITDB_DATABASE --db $DB_NAME --collection songs --jsonArray
mongoimport --drop fingerprints.json -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase $MONGO_INITDB_DATABASE --db $DB_NAME --collection fingerprints --jsonArray
mongo --eval "db = db.getSiblingDB('$DB_NAME'); db.fingerprints.createIndex({ hash : -1 });"