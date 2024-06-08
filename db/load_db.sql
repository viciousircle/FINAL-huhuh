-- Use the LMS database
USE LMS;
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

-- Insert sample data into user.account
INSERT INTO users.account (admin_id, [password], admin_name) VALUES
(1, 'password123', 'Vu Minh Quy'),
(2, 'password456', 'Do Hoang Dung');
GO

-- Insert sample data into user.history
INSERT INTO users.history (edit_id, admin_id, book_id, [timestamp]) VALUES
(1, 1, 1, '2023-01-01 10:00:00'),
(2, 2, 2, '2023-01-02 11:00:00'),
(3, 1, 3, '2023-01-03 12:00:00');
GO


-- Insert sample data into user.guest
INSERT INTO users.guest (guest_id, guest_name, [timestamp]) VALUES
(1, 'Charlie Brown', '2023-01-01 09:00:00'),
(2, 'Daisy Miller', '2023-01-02 10:00:00');
GO

-- Insert sample data into book.bookMarc
INSERT INTO books.bookMarc (book_id, title, author, public_year, public_comp, isbn) VALUES
(1, 'To Kill a Mockingbird', 'Harper Lee', 1960, 'J.B. Lippincott & Co.', '978-0061120084'),
(2, '1984', 'George Orwell', 1949, 'Secker & Warburg', '978-0451524935'),
(3, 'The Great Gatsby', 'F. Scott Fitzgerald', 1925, 'Charles Scribners Sons', '978-0743273565');
GO

-- Insert sample data into book.books
INSERT INTO books.book (book_id, warehouse_id, quantity, stage) VALUES
(1, 101, 10, 'Available'),
(2, 102, 5, 'Unavailable'),
(3, 103, 2, 'Available');
GO