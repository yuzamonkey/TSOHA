CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    Username TEXT UNIQUE,
    Password TEXT,
    Admin BOOLEAN,
    Suspended BOOLEAN
);
CREATE TABLE Categories (
    id SERIAL PRIMARY KEY,
    Category TEXT
);
CREATE TABLE Counties (
    id SERIAL PRIMARY KEY,
    County TEXT
);
CREATE TABLE Images (
    id SERIAL PRIMARY KEY,
    Name TEXT,
    Data BYTEA
);
CREATE TABLE Events (
    id SERIAL PRIMARY KEY,
    Name TEXT,
    User_id INTEGER REFERENCES Users,
    Category_id INTEGER REFERENCES Categories,
    County_id INTEGER REFERENCES Counties,
    Locale TEXT,
    City TEXT,
    Address TEXT,
    Description TEXT,
    Starting_time TIMESTAMP,
    Ending_time TIMESTAMP,
    Price TEXT,
    Image_id INTEGER REFERENCES Images
);
CREATE TABLE Reports (
    id SERIAL PRIMARY KEY, 
    Title TEXT, 
    Content TEXT, 
    Unread BOOLEAN
);