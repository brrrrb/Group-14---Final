from typing import Any
from repositories.db import get_pool
from psycopg.rows import dict_row


def does_username_exist(username: str) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        SELECT
                            user_id
                        FROM
                            app_user
                        WHERE username = %s
                        ''', [username])
            user_id = cur.fetchone()
            return user_id is not None


def create_user(first_name: str, last_name: str, username: str, password: str) -> dict[str, Any]:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        INSERT INTO app_user (first_name, last_name, username, password)
                        VALUES (%s, %s, %s, %s)
                        RETURNING user_id
                        ''', [first_name, last_name, username, password])
            user_id = cur.fetchone()
            if user_id is None:
                raise Exception('Failed to create user')
            return {
                'user_id': user_id[0],
                'username': username,
                'first_name': first_name, 
                'last_name': last_name
            }
            
            
    



def get_user_by_username(username: str) -> dict[str, Any] | None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT user_id, username, password AS hashed_password, first_name, last_name, company_name
                        FROM app_user
                        WHERE username = %s
                        ''', [username])
            return cur.fetchone()


def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT user_id, username, first_name, last_name, company_name
                        FROM app_user
                        WHERE user_id = %s
                        ''', [user_id])
            return cur.fetchone()






def create_business_user(company_name, ein_number, username, password) -> dict[str, Any]:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            # Ensure username and EIN are unique before insertion
            cur.execute('SELECT user_id FROM app_user WHERE username = %s OR ein_number = %s', (username, ein_number))
            if cur.fetchone() is not None:
                raise Exception('Username or EIN already exists')

            # Insert new business user
            cur.execute('''
                        INSERT INTO app_user (company_name, ein_number, username, password)
                        VALUES (%s, %s, %s, %s)
                        RETURNING user_id
                        ''', (company_name, ein_number, username, password))
            user_id = cur.fetchone()
            if user_id is None:
                raise Exception('Failed to create business user')
            return {
                'user_id': user_id[0],
                'username': username,
                'company_name': company_name
            }
