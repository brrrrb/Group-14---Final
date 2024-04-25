from psycopg_pool import ConnectionPool
import os


pool = None

def get_pool():
    global pool
    if pool is None:
        connection_string = os.getenv('DB_CONNECTION_STRING', '')
        if connection_string == '':
            raise Exception('Database connection string is not configured.')
        pool = ConnectionPool(conninfo=connection_string)
    return pool