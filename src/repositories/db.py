import os
from psycopg_pool import ConnectionPool

pool = None

def get_pool():
    global pool
    if pool is None:
        # Get the connection string from environment variables
        conninfo = os.getenv('DB_CONNECTION_STRING')
        if not conninfo:
            raise ValueError("DB_CONNECTION_STRING environment variable is not set.")
        pool = ConnectionPool(conninfo=conninfo)
    return pool
