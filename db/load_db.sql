-- Use the LMS database
USE LMS;
GO

USE master;
GO

DROP DATABASE LMS;

SELECT * FROM users.account;
SELECT * FROM users.history;
SELECT * FROM users.guest;
SELECT * FROM books.bookMarc;
SELECT * FROM books.book;
GO



UPDATE books.book SET isbn = '0000' WHERE isbn = '9780743273565';
UPDATE books.bookMarc SET isbn = '0000' WHERE isbn = '9780743273565';


GO
sp_help 'users.account';
GO 
sp_help 'users.history';
GO
sp_help 'users.guest';
GO
sp_help 'books.bookMarc';
GO
sp_help 'books.book';
GO

DELETE FROM users.account;
GO
DELETE FROM users.history;
GO
DELETE FROM users.guest;
GO
DELETE FROM books.bookMarc;
GO
DELETE FROM books.book;
GO



-- Insert sample data into user.account
INSERT INTO users.account (admin_id, [password], admin_name) VALUES
('1','1','Nam'),
('2','2','Hoa'),
('3','3','Lan'),
('4','4','Hai'),
('5','5','Dung');
GO

-- Insert sample data into user.history
INSERT INTO users.history (admin_id, book_id, isbn, warehouse_id, [timestamp]) VALUES
('1', 1, '9780743273565', 1, '2023-01-01 09:00:00'),
('2', 2, '9780061120084', 2, '2023-01-02 10:00:00'),
('3', 3, '9780451524935', 3, '2023-01-03 11:00:00'),
('4', 4, '9781503290563', 4, '2023-01-04 12:00:00'),
('5', 5, '9780316769488', 5, '2023-01-05 13:00:00');



-- Insert sample data into user.guest
INSERT INTO users.guest (guest_id, guest_name, [timestamp]) VALUES
(1, 'Hoa', '2023-01-01 09:00:00'),
(2, 'Nam', '2023-01-02 10:00:00'),
(3, 'Lan', '2023-01-03 11:00:00'),
(4, 'Hai', '2023-01-04 12:00:00'),
(5, 'Dung', '2023-01-05 13:00:00');
GO

-- Insert data into books.bookMarc
INSERT INTO books.bookMarc (title, author, public_year, public_comp, isbn) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 1925, 'Scribner', '9780743273565'),
('To Kill a Mockingbird', 'Harper Lee', 1960, 'J.B. Lippincott & Co.', '9780061120084'),
('1984', 'George Orwell', 1949, 'Secker & Warburg', '9780451524935'),
('Pride and Prejudice', 'Jane Austen', 1813, 'T. Egerton', '9781503290563'),
('The Catcher in the Rye', 'J.D. Salinger', 1951, 'Little, Brown and Company', '9780316769488'),
('The Hobbit', 'J.R.R. Tolkien', 1937, 'George Allen & Unwin', '9780547928227'),
('Fahrenheit 451', 'Ray Bradbury', 1953, 'Ballantine Books', '9781451673319'),
('Moby-Dick', 'Herman Melville', 1851, 'Harper & Brothers', '9781503280786'),
('War and Peace', 'Leo Tolstoy', 1869, 'The Russian Messenger', '9781400079988'),
('The Odyssey', 'Homer', -800, 'Penguin Classics', '9780140268867');


-- Insert data into books.book
INSERT INTO books.book (book_id, isbn, quantity, stage) VALUES
(1, '9780743273565', 100, 'Available'),
(2, '9780061120084', 150, 'Available'),
(3, '9780451524935', 200, 'Available'),
(4, '9781503290563', 120, 'Available'),
(5, '9780316769488', 180, 'Available'),
(6, '9780547928227', 90, 'Available'),
(7, '9781451673319', 220, 'Available'),
(8, '9781503280786', 130, 'Available'),
(9, '9781400079988', 110, 'Available'),
(10, '9780140268867', 75, 'Available');
