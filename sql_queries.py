import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS song_plays "
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events (
    artist VARCHAR(200),
    auth VARCHAR(100),
    firstName VARCHAR(100),
    gender CHARACTER(1),
    iteminSession INT,
    lastName VARCHAR(100),
    length DECIMAL(10,5),
    level VARCHAR(25),
    location VARCHAR(200),
    method VARCHAR(25),
    page VARCHAR(25),
    registration VARCHAR(200),
    sessionId INT,
    song VARCHAR(200),
    status INT,
    ts BIGINT,
    userAgent VARCHAR(200),
    userId INT
)
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs (
    num_songs INT,
    artist_id VARCHAR(100),
    artist_latitude DECIMAL(9,6),
    artist_longitude DECIMAL(9,6),
    artist_location VARCHAR(200),
    artist_name VARCHAR(200),
    song_id VARCHAR(100), 
    title VARCHAR(200), 
    duration FLOAT,
    year INT)
""")

songplay_table_create = ("""
     CREATE TABLE IF NOT EXISTS song_plays (
     songplay_id BIGINT IDENTITY(0,1) PRIMARY KEY,
     start_time TIMESTAMP NOT NULL ,
     user_id INT REFERENCES users(user_id),
     level VARCHAR NOT NULL,
     song_id VARCHAR REFERENCES songs(song_id),
     artist_id VARCHAR REFERENCES artists(artist_id),
     session_id INT NOT NULL, 
     location VARCHAR,
     user_agent TEXT)
""")

user_table_create = ("""
     CREATE TABLE IF NOT EXISTS  users (
     user_id INT PRIMARY KEY,
     first_name  VARCHAR NOT NULL,
     last_name  VARCHAR NOT NULL,
     gender  CHAR(1),
     level VARCHAR NOT NULL)
""")

song_table_create = ("""
     CREATE TABLE  IF NOT EXISTS songs (
     song_id VARCHAR PRIMARY KEY,
     title  VARCHAR NOT NULL,
     artist_id  VARCHAR,
     year INT,
     duration FLOAT)
""")

artist_table_create = ("""
     CREATE TABLE  IF NOT EXISTS artists (
     artist_id VARCHAR PRIMARY KEY,
     name VARCHAR NOT NULL,
     location VARCHAR,
     latitude DECIMAL(9,6),
     longitude DECIMAL(9,6))
""")

time_table_create = ("""
     CREATE TABLE IF NOT EXISTS  time (
     start_time TIMESTAMP PRIMARY KEY,
     hour INT NOT NULL ,
     day INT NOT NULL ,
     week INT NOT NULL ,
     month INT NOT NULL ,
     year INT NOT NULL ,
     weekday smallint NOT NULL
)""")



# STAGING TABLES

staging_events_copy = ("""
    copy staging_events from 's3://udacity-dend/log_data/'
    credentials 'aws_iam_role=arn:aws:iam::313450712181:role/dwhRole'
    compupdate off region 'us-west-2'
    FORMAT AS JSON 's3://udacity-dend/log_json_path.json';

""")

staging_songs_copy = ("""
    copy staging_songs from 's3://udacity-dend/song_data'
    credentials 'aws_iam_role=arn:aws:iam::313450712181:role/dwhRole'
    compupdate off region 'us-west-2'
    FORMAT AS JSON 'auto';
""")

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO song_plays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT
    TIMESTAMP 'epoch' + se.ts/1000 *INTERVAL '1 second', se.userId, se.level, ss.song_id, ss.artist_id, se.sessionId, se.location, se.userAgent
    FROM staging_events se 
    LEFT JOIN staging_songs ss
    ON se.artist=ss.artist_name AND se.song= ss.title
    WHERE se.page='NextSong'
    AND ss.artist_id IS NOT NULL
""")


user_table_insert = ("""
    INSERT INTO users
    SELECT DISTINCT userId, firstName, lastName, gender, level FROM staging_events
    WHERE userId IS NOT NULL AND userId NOT IN ( SELECT DISTINCT userId from users)
                         
""")


song_table_insert = ("""
        INSERT INTO songs
        SELECT DISTINCT song_id, title, artist_id, year, duration FROM staging_songs
        WHERE song_id IS NOT NULL
                         
""")

artist_table_insert = ("""
        INSERT INTO artists
        SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude,
        artist_longitude FROM staging_songs
        WHERE artist_id IS NOT NULL
                         
""")
time_table_insert = ("""
        INSERT INTO time 
        SELECT  DISTINCT timestamp 'epoch' + ts/1000 * interval '1 second' AS start_time,
                EXTRACT(HOUR FROM timestamp 'epoch' + ts/1000 * interval '1 second') AS hour,
                EXTRACT(DAY FROM  timestamp 'epoch' + ts/1000 * interval '1 second') AS DAY,
                EXTRACT(WEEK FROM  timestamp 'epoch' + ts/1000 * interval '1 second') AS week,
                EXTRACT(MONTH FROM  timestamp 'epoch' + ts/1000 * interval '1 second') AS month,
                EXTRACT(YEAR FROM  timestamp 'epoch' + ts/1000 * interval '1 second') AS year,
                EXTRACT(WEEKDAY FROM  timestamp 'epoch' + ts/1000 * interval '1 second') AS weekday
                FROM staging_events
                         
""")


# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create,songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
