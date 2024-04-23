class Itinerary:
    """A itinerary holds a name, destination, disembark date, days, and activities."""
    def __init__(self, itinerary_id: int, name: str, destination: str, disembark_date: str, days: int)->None:
        self.name = name
        self.itinerary_id = itinerary_id
        self.destination = destination
        self.disembark_date = disembark_date
        self.days = days
        self.activities = {}
    
    def add_activity(self, day: int, activity: str, description: str):
        """Add an activity to a particular day."""
        if day not in self.activities:
            self.activities[day] = []
        self.activities[day].append({"activity": activity, "description": description})