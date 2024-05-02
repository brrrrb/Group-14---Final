CREATE TABLE app_user (
  user_id SERIAL PRIMARY KEY,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  username VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  company_name VARCHAR(255),
  ein_number VARCHAR(9) UNIQUE
);

-- Create Posts table
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    country VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    posted_at TIMESTAMP NOT NULL,
    type VARCHAR(50) NOT NULL,
    image_filename VARCHAR(255),

    -- Business-specific fields
    address_line_1 VARCHAR(255),
    address_line_2 VARCHAR(255),
    city VARCHAR(100),
    zip_code VARCHAR(20),
    state VARCHAR(100),
    website_link VARCHAR(255),
    phone_number VARCHAR(20),
    email VARCHAR(100),
    hours_of_operation TEXT,

    -- Personal-specific fields
    trip_purpose VARCHAR(100),
    time_of_visit VARCHAR(50),
    rating VARCHAR(50)
);

-- Create Comments table
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL,
    username VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    edited BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
);

-- Create Countries table
CREATE TABLE IF NOT EXISTS Countries (
    CountryID INT PRIMARY KEY,
    countryName VARCHAR(255)
);

-- Itinerary Table
CREATE TABLE Itinerary (
    itinerary_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    destination VARCHAR(255) NOT NULL,
    disembark_date DATE NOT NULL,
    days INTEGER NOT NULL
);

-- Activities Table for Itinerary
CREATE TABLE Activity (
    itinerary_id INTEGER NOT NULL,
    day INTEGER NOT NULL,
    activity VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    PRIMARY KEY (itinerary_id, day),
    FOREIGN KEY (itinerary_id) REFERENCES Itinerary(itinerary_id) ON DELETE CASCADE
);


