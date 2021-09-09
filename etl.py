import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries

'''Function loads data into staging tables from Amazon S3 
   Takes cursor and connection as input
'''
def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()

'''Function inserts data into fact and dimension tables from staging tables  
   Takes cursor and connection as input
'''
def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()
        
        
''' Function will configure the cluster, calls load_staging_table function and insert_tables function
    Function reads the dwh.cfg file to input values
'''

def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()