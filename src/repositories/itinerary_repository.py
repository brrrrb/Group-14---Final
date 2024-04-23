from random import randint
from typing import Dict
from src.models.itinerary import Itinerary

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