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

DROP TABLE users.account;
DROP TABLE users.history;
DROP TABLE users.guest;
DROP TABLE books.bookMarc;
DROP TABLE books.book;


-- Create the account table for users
CREATE TABLE users.account (
    admin_id    VARCHAR(20) PRIMARY KEY,
    [password]  VARCHAR(20),
    admin_name  VARCHAR(100)
);
GO

-- Create the history_edit table for user edits
CREATE TABLE users.history (
    admin_id    VARCHAR(20),
    book_id     INT,
    isbn        VARCHAR(25),
    warehouse_id    INT,
    [timestamp] DATETIME,
    FOREIGN KEY (admin_id) REFERENCES users.account(admin_id)
);
GO

-- Create the guest table
CREATE TABLE users.guest (
    guest_id    INT PRIMARY KEY,
    guest_name  VARCHAR(100),
    [timestamp] DATETIME
);
GO

-- Create the bookMarc table for book details
CREATE TABLE books.bookMarc (
    book_id     INT IDENTITY(1,1),
    title       VARCHAR(255),
    author      VARCHAR(255),
    public_year INT,
    public_comp VARCHAR(255),
    isbn        VARCHAR(25),
    PRIMARY KEY (book_id)
);
GO

-- Create the book table for book inventory
CREATE TABLE books.book (
    warehouse_id    INT PRIMARY KEY IDENTITY(1,1),
    book_id         INT NOT NULL,
    isbn            VARCHAR(25),
    quantity        INT NOT NULL,
    stage           VARCHAR(100),
    FOREIGN KEY (book_id) REFERENCES books.bookMarc(book_id)
);
GO
