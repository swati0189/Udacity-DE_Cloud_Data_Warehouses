
# Project description
 Sparkify is a music streaming startup with a growing user base and song database.

The user activity and songs metadata data resides in json files in amazon S3 . The goal of the project is to build an ETL pipeline that extracts the data from S3 bucket and stages them in Redshift, and transforms the data into fact and dimension tables for finding insights in what songs the users are listening to.

# How to RUN
To run this project, the following information needs to be filled, and save it as dwh.cfg in the project root folder.
[AWS]
KEY=
SECRET=

[DWH] 
DWH_CLUSTER_TYPE=multi-node
DWH_NUM_NODES=4
DWH_NODE_TYPE=dc2.large

DWH_IAM_ROLE_NAME=
DWH_CLUSTER_IDENTIFIER=
DWH_DB_USER=
DWH_DB_PASSWORD=
DWH_PORT=5439

[CLUSTER]
host=
DB_NAME=dwh
DB_USER=
DB_PASSWORD=
DB_PORT=5439

[IAM_ROLE]
ARN=

[S3]
LOG_DATA='s3://udacity-dend/log_data'
LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
SONG_DATA='s3://udacity-dend/song_data'

# python clustercreation.ipynb
To connect to the cluster and later for clearing the resources .

# python create_tables.py

Finally, run the etl script to extract data from the files in S3 bucket, stage it in redshift, and finally store it in the dimension tables and fact table.

# python create_tables.py

Project structure
This project includes three script files:

create_table.py : fact and dimension tables for the star schema in Redshift are created.
etl.py: Data(JSON files) gets loaded from S3 into staging tables on Redshift and then processed into the fact and dimension tables on Redshift.
sql_queries.py : SQL statements are defined, which are then used by etl.py, create_table.py and analytics.py.



### Staging Tables

### Staging Songs table
 
- *Name:* `staging_songs `
- *Type:* STaging Table

  
| Column | Type | Description |
| ------ | ---- | ----------- |
| `num_song` | `INT` | 
| `artist_id` | `VARCHAR` | The identification of the artist of the song that was played. | 
| `artist_latitude` | `DECIMAL` | The latitude of the location |
| `artist_longitude` | `DECIMAL` | The longitude of the location.  |
| `artist_location` | `VARCHAR` | The location of the artist |
| `artist_name` | `VARCHAR` | The name of the artist  |
| `song_id` | `VARCHAR` | The identification of the song that was played. |
| `title` | `INTEGER NOT NULL` | The title of the song |
| `duration` | `FLOAT` | The duration of the song  |
| `year` | `INT` | The year that this song was made |

### Staging Events Table

- *Name:* `staging_events`
- *Type:* Staging Table


| Column | Type | Description |
| ------ | ---- | ----------- |
| `artist` | `VARCHAR`| The name of the artist | 
| `auth` | `VARCHAR` | The authorisation of user eg.loggedin , logged out etc |
| `first_name` | `VARCHAR` | The first_name of the user  |
| `gender` | `CHARACTER` | The gender of the user |
| `iteminSession` | `INT` | The number of items user has in one session  |
| `lastName` | `VARCHAR` | The last_name of user |
| `length` | `DECIMAL` | The total time user listened to songs in a session |
| `level` | `VARCHAR` | The level of the user, free or paid  |
| `location` | `VARCHAR` | The location of user of our app |
| `method` | `VARCHAR` | The method used, get or put  |
| `page` | `VARCHAR` | The page on the app that the user is currently present, Eg.Home , next_song |
| `registration` | `VARCHAR` | The registration number of the user |
| `sessionId` | `INT` | The session id of user on the app  |
| `song` | `VARCHAR` | The song that the user is playing |
| `status` | `INT` | The status of the user  |
| `ts` | `BIGINT` | Timestamp of the user |
| `userAgent` | `VARCHAR` | The browser that the user has used for logging into our app, eg. firefox,internetexplorer etc |
| `userId` | `INT` | The user id of the user  |



### Song Plays table

- *Name:* `songplays`
- *Type:* Fact table

| Column | Type | Description |
| ------ | ---- | ----------- |
| `songplay_id` | `SERIAL NOT NULL` | Unique Identifier for Song_Plays Table | 
| `start_time` | `TIMESTAMP NOT NULL` | The timestamp that this song play log happened |
| `user_id` | `INTEGER REFERENCES users (user_id)` | The user id that triggered this song play log. It cannot be null, as we don't have song play logs without being triggered by an user.  |
| `level` | `VARCHAR NOT NULL` | The level of the user that triggered this song play log |
| `song_id` | `VARCHAR REFERENCES songs (song_id)` | The identification of the song that was played. It can be null.  |
| `artist_id` | `VARCHAR REFERENCES artists (artist_id)` | The identification of the artist of the song that was played. |
| `session_id` | `INTEGER NOT NULL` | The session_id of the user on the app |
| `location` | `VARCHAR` | The location where this song play log was triggered  |
| `user_agent` | `TEXT` | The user agent of our app |

### Users table

- *Name:* `users`
- *Type:* Dimension table

| Column | Type | Description |
| ------ | ---- | ----------- |
| `user_id` | `INTEGER CONSTRAINT users_pk PRIMARY KEY NOT NULL` | Unique Identifier for a user |
| `first_name` | `VARCHAR NOT NULL` | First name of the user |
| `last_name` | `VARCHAR NOT NULL` | Last name of the user. |
| `gender` | `CHAR(1)` | The gender is stated with just one character `M` (male) or `F` (female) |
| `level` | `VARCHAR NOT NULL` | The level stands for the user app plans (`premium` or `free`) |



### Songs table

- *Name:* `songs`
- *Type:* Dimension table

| Column | Type | Description |
| ------ | ---- | ----------- |
| `song_id` | `VARCHAR  CONSTRAINT songs_pk PRIMARY KEY NOT NULL` | Unique Identfier for a song | 
| `title` | `VARCHAR NOT NULL` | Title of the Song. |
| `artist_id` | `VARCHAR REFERENCES artists (artist_id)` |Artist Identifier |
| `year` | `INTEGER` | The year that this song was made |
| `duration` | `FLOAT` | The duration of the song |




### Artists table

- *Name:* `artists`
- *Type:* Dimension table

| Column | Type | Description |
| ------ | ---- | ----------- |
| `artist_id` | `VARCHAR CONSTRAINT artist_pk PRIMARY KEY NOT NULL` | Unique Identifier of an artist |
| `name` | `VARCHAR NOT NULL` | The name of the artist |
| `location` | `VARCHAR` | Location of artist |
| `latitude` | `DECIMAL(9,6)` | The latitude of the location |
| `longitude` | `DECIMAL(9,6)` | The longitude of the location |


### Time table

- *Name:* `time`
- *Type:* Dimension table

| Column | Type | Description |
| ------ | ---- | ----------- |
| `start_time` | `TIMESTAMP CONSTRAINT start_time_pk PRIMARY KEY` | Song Start Time  |
| `hour` | `INTEGER NOT NULL` | The hour from the timestamp  |
| `day` | `INTEGER NOT NULL` | The day of the month from the timestamp |
| `week` | `INTEGER NOT NULL` | The week of the year from the timestamp |
| `month` | `INTEGER NOT NULL` | The month of the year from the timestamp |
| `year` | `INTEGER NOT NULL` | The year from the timestamp |
| `weekday` | `VARCHAR NOT NULL` | The week day from the timestamp |


Steps followed on this project
## The project file structure

We have a small list of files, easy to maintain and understand:
 - `sql_queries.py` - Files consist of all the sql script required to create, load, drop tables and query lists which are being used in etl.py &     create_tables.py
 - `create_tables.py` -Python code to create and drop tables in Redshift.
 - `etl.py` - It's perform main ETL process
 - `clustercreation.ipynb` - The python notebook to make the cluster available and later shutting down the resources.
 

