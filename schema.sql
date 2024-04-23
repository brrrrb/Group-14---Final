-- Create User table
CREATE TABLE User (
    UserID INT PRIMARY KEY,
    username VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255)
);

-- Create Post table
CREATE TABLE Post (
    ID INT PRIMARY KEY,
    userID INT,
    Title VARCHAR(255),
    Content TEXT,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (userID) REFERENCES User(UserID)
);

-- Create Comments table
CREATE TABLE Comments (
    commentId INT PRIMARY KEY,
    postID INT,
    userID INT,
    comment TEXT,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (postID) REFERENCES Post(ID),
    FOREIGN KEY (userID) REFERENCES User(UserID)
);

-- Create Countries table
CREATE TABLE Countries (
    CountryID INT PRIMARY KEY,
    countryName VARCHAR(255)
);

