from typing import Any 
from repositories.db import get_pool


def does_email_exist(email: str) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                         SELECT
                           user_id
                         FROM
                            user
                         WHERE email = %s
                         ''', [email])
            user_id = cur.fetchone()
            return user_id is not None
        
        
  
def create_user(email: str,password: str) -> dict[str, Any]:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        INSERT INTO app_user(email, password)
                        VALUES (%s, %s)
                        RETURNING user_id
                        ''', [email, password]
            )
            
            user_id = cur.fetchone()
            if user_id is None:
                return Exception('failed to create user')
            return {
                'user_id': user_id,
                'email': email
            } 