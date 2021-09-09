import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries

''' 
    Function will drop the following tables from redshift databse
    
    staging_events
    staging_songs
    song_plays
    users
    songs
    artists
    time
    
    Takes cursor for database connection and connection to instances as input 
    
'''
def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

''' 
    Function will create the tables in redshift database
    staging_events
    staging_songs
    song_plays
    users
    songs
    artists
    time
    Takes cursor for database connection and connection to instances as input  
'''
def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

''' 
    Function will connect to redshift cluster using dwh.cfg file 
    Function will call drop_tables and create_tables for dropping and creating table in REdshift database 
'''
def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()