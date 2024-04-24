import psycopg2
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