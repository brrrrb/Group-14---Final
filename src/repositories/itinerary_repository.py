import os
from typing import Dict, List, Optional
from src.models.itinerary import Itinerary
from src.repositories.db import get_pool
from psycopg.rows import dict_row
from random import randint


_itinerary_repo = None

def get_itinerary_repo():
    global _itinerary_repo
    
    class ItineraryRepository:
        """In memory database which is a simple dict of itineraries."""

        def __init__(self) -> None:
            self._db: Dict[int, Itinerary] = {}
            
        def get_all_itineraries(self) -> Dict[int, Itinerary]:
            return self._db.copy()
            
        def get_itinerary_by_id(self, itinerary_id: int) -> Itinerary | None:
            return self._db.get(itinerary_id)
        
        def create_itinerary(self, name: str, destination: str, disembark_date: str, days: int) -> Itinerary:
            """"Create a new itinerary and return it."""
            new_id = randint(0, 100_000)
            itinerary = Itinerary(new_id, name, destination, disembark_date, days)
            self._db[new_id] = itinerary
            return itinerary
        
        # update the activities of an itinerary with data from the form
        def update_itinerary(self, itinerary_id: int, activities: list) -> Itinerary | None:
            """Update the activities of an itinerary with data from the form."""
            itinerary: Itinerary | None = self.get_itinerary_by_id(itinerary_id)
            if itinerary is not None:
                itinerary.activities = activities
                return itinerary
            return None
        
        def delete_itinerary(self, itinerary_id: int):
            """Delete an itinerary by id."""
            if itinerary_id in self._db:
                del self._db[itinerary_id]
        
    #What Copoilt added  
    _itinerary_repo = ItineraryRepository()
    return _itinerary_repo


# def get_all_itineraries():
#         pool = get_pool()
#         with pool.connection() as conn:
#             with conn.cursor(cursor_factory=dict_row) as cur:
#                 cur.execute('''
#                             SELECT
#                                 itinerary_id,
#                                 name,
#                                 destination,
#                                 disembark_date,
#                                 days
#                             FROM
#                                 Itinerary
#                             ''')
#                 itineraries = cur.fetchall()
#                 return itineraries
            
# def create_itinerary(name: str, destination: str, disembark_date: str, days: int):
#         pool = get_pool()
#         with pool.connection() as conn:
#             with conn.cursor() as cur:
#                 cur.execute('''
#                             INSERT INTO Itinerary(name, destination, disembark_date, days)
#                             VALUES (%s, %s, %s, %s)
#                             RETURNING itinerary_id
#                             ''', [name, destination, disembark_date, days])
#                 itinerary_id = cur.fetchone()
#                 itinerary = Itinerary(itinerary_id, name, destination, disembark_date, days)
#                 conn.commit()
#                 return itinerary

#Not correct
# def update_itinerary(itinerary_id: int, activities: list):
#         pool = get_pool()
#         with pool.connection() as conn:
#             with conn.cursor() as cur:
#                 cur.execute('''
#                             UPDATE
#                                 Activity
#                             SET
#                                 activities = %s
#                             WHERE
#                                 itinerary_id = %s
#                             ''', [activities, itinerary_id])
#                 return True


# def get_itinerary_by_id(itinerary_id: int):
#         pool = get_pool()
#         with pool.connection() as conn:
#             with conn.cursor(row_factory=dict_row) as cur:
#                 cur.execute('''
#                             SELECT
#                                 itinerary_id,
#                                 name,
#                                 destination,
#                                 disembark_date,
#                                 days
#                             FROM
#                                 Itinerary
#                             WHERE itinerary_id = %s
#                             ''', [itinerary_id])
                
#                 return cur.fetchone()[0]
            
            
# def delete_itinerary(itinerary_id: int):
#         pool = get_pool()
#         with pool.connection() as conn:
#             with conn.cursor() as cur:
#                 cur.execute('''
#                             DELETE FROM
#                                 Itinerary
#                             WHERE
#                                 itinerary_id = %s
#                             ''', [itinerary_id])
#                 return True