-- Create User table
CREATE TABLE IF NOT EXISTS User (
    UserID INT PRIMARY KEY,
    username VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255)
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

