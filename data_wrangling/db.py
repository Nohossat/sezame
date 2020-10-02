"""
Database class to connect, disconnect, made some queries to a Postgresql database
"""
from sqlalchemy import create_engine
import config

class Database():
    def __init__(self):
        self.connection = None
        print("DB instance created")

    def insert_song(self, song_name, artist):
        query = self.connection.execute("""
                INSERT INTO songs(song_name, artist)
                VALUES (%s %s)
            """, (song_name, artist))

    def get_last_record_day(self):
        query = self.connection.execute("""
            SELECT DISTINCT record_day FROM companies_prices 
            ORDER BY record_day DESC LIMIT 1;
        """)
        return query.fetchall()[0][0]
    
    def close_connection(self):
        self.connection.close()