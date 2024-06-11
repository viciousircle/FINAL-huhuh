SELECT @@ServerName;
USE master;
-- Create the LMS database
CREATE DATABASE LMS;
GO

-- Use the LMS database
USE LMS;
GO


-- Create the user schema
CREATE SCHEMA users;
GO

-- Create the book schema
CREATE SCHEMA books;
GO

DROP DATABASE LMS;

-- Create the account table for users
CREATE TABLE users.account (
    admin_id INT PRIMARY KEY,
    [password] VARCHAR(255),
    admin_name VARCHAR(255)
);
GO

-- Create the history_edit table for user edits
CREATE TABLE users.history (
    edit_id INT PRIMARY KEY,
    admin_id INT,
    book_id INT,
    [timestamp] DATETIME,
    FOREIGN KEY (admin_id) REFERENCES users.account(admin_id),
    FOREIGN KEY (book_id) REFERENCES books.bookMarc(book_id)
);
GO

-- Create the guest table
CREATE TABLE users.guest (
    guest_id INT PRIMARY KEY,
    guest_name VARCHAR(255),
    [timestamp] DATETIME
);
GO

-- Create the bookMarc table for book details
CREATE TABLE books.bookMarc (
    book_id INT IDENTITY(1,1),
    title VARCHAR(255),
    author VARCHAR(255),
    public_year INT,
    public_comp VARCHAR(255),
    isbn VARCHAR(255) UNIQUE,
    PRIMARY KEY (book_id, isbn)
);
GO

-- Create the book table for book inventory
CREATE TABLE books.book (
    warehouse_id INT PRIMARY KEY IDENTITY(1,1),
    book_id INT,
    quantity INT,
    stage VARCHAR(255),
    FOREIGN KEY (book_id) REFERENCES books.bookMarc(book_id)
);
GO