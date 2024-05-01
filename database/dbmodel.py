import psycopg2
from typing import List, Dict
from src.models.itinerary import Itinerary
from db_secrets import DB_PASS  # Import your database password from db_secrets.py

# Connect to the database for whoever sets it up
def connect():
    return psycopg2.connect(
        dbname='db name', # whoever connects
        user='user name', # whoever connects 
        password=DB_PASS,
        host='localhost',
        port='5432'
    )

# Create a new user
def create_user(username, email, password):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO User (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
    conn.commit()
    conn.close()

# Get all users
def get_all_users():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM User")
    users = cur.fetchall()
    conn.close()
    return users

# Create a new post
def create_post(userID, title, content):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO Post (userID, title, content) VALUES (%s, %s, %s)", (userID, title, content))
    conn.commit()
    conn.close()

# Get all posts
def get_all_posts():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Post")
    posts = cur.fetchall()
    conn.close()
    return posts



# Comments
def create_comment(postID, userID, comment):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO Comments (postID, userID, comment) VALUES (%s, %s, %s)", (postID, userID, comment))
    conn.commit()
    conn.close()

# Create a new country
def create_country(countryName):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO Countries (countryName) VALUES (%s)", (countryName,))
    conn.commit()
    conn.close()

# Get all countries
def get_all_countries():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Countries")
    countries = cur.fetchall()
    conn.close()
    return countries

# Create a new itinerary
def create_itinerary(name: str, destination: str, disembark_date: str, days: int) -> Itinerary:
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO Itinerary (name, destination, disembark_date, days) VALUES (%s, %s, %s, %s) RETURNING itinerary_id", (name, destination, disembark_date, days))
    itinerary_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return Itinerary(itinerary_id, name, destination, disembark_date, days)

# Get all itineraries
def get_all_itineraries() -> Dict[int, Itinerary]:
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Itinerary")
    rows = cur.fetchall()
    itineraries = {}
    for row in rows:
        itinerary_id, name, destination, disembark_date, days = row
        itineraries[itinerary_id] = Itinerary(itinerary_id, name, destination, disembark_date, days)
    conn.close()
    return itineraries

# Get an itinerary by id
def get_itinerary_by_id(itinerary_id: int) -> Itinerary:
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Itinerary WHERE itinerary_id = %s", (itinerary_id,))
    row = cur.fetchone()
    if row:
        itinerary_id, name, destination, disembark_date, days = row
        itinerary = Itinerary(itinerary_id, name, destination, disembark_date, days)
    else:
        itinerary = None
    conn.close()
    return itinerary

# Update an itinerary
def add_activities_to_itinerary(itinerary_id: int, activities: List[Dict[str, str]]) -> None:
    conn = connect()
    cur = conn.cursor()
    for activity in activities:
        day = activity['day']
        act = activity['activity']
        desc = activity['description']
        cur.execute("INSERT INTO Activity (itinerary_id, day, activity, description) VALUES (%s, %s, %s, %s)", (itinerary_id, day, act, desc))
    conn.commit()
    conn.close()
