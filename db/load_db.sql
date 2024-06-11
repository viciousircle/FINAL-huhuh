-- Use the LMS database
USE LMS;
GO

SELECT * FROM users.account;
SELECT * FROM users.history;
SELECT * FROM users.guest;
SELECT * FROM books.bookMarc;
SELECT * FROM books.book;

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
INSERT INTO users.history (edit_id, admin_id, book_id, [timestamp]) VALUES
(1, '1', 1, '2023-01-01 09:00:00'),
(2, '2', 2, '2023-01-02 10:00:00'),
(3, '3', 3, '2023-01-03 11:00:00'),
(4, '4', 4, '2023-01-04 12:00:00'),
(5, '5', 5, '2023-01-05 13:00:00');
GO


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
('The Odyssey', 'Homer', -800, 'Penguin Classics', '9780140268867'),
('Crime and Punishment', 'Fyodor Dostoevsky', 1866, 'The Russian Messenger', '9780486415871'),
('The Divine Comedy', 'Dante Alighieri', 1320, 'Penguin Classics', '9780140448955'),
('The Brothers Karamazov', 'Fyodor Dostoevsky', 1880, 'The Russian Messenger', '9780374528379'),
('Brave New World', 'Aldous Huxley', 1932, 'Chatto & Windus', '9780060850524'),
('Jane Eyre', 'Charlotte Bronte', 1847, 'Smith, Elder & Co.', '9780142437209'),
('Wuthering Heights', 'Emily Bronte', 1847, 'Thomas Cautley Newby', '9780141439556'),
('The Iliad', 'Homer', -750, 'Penguin Classics', '9780140275360'),
('Les Misérables', 'Victor Hugo', 1862, 'A. Lacroix, Verboeckhoven & Cie', '9780451419438'),
('Anna Karenina', 'Leo Tolstoy', 1878, 'The Russian Messenger', '9780143035008'),
('One Hundred Years of Solitude', 'Gabriel Garcia Marquez', 1967, 'Harper & Row', '9780060883287'),
('Madame Bovary', 'Gustave Flaubert', 1857, 'Michel Lévy Frères', '9780140449129'),
('The Great Expectations', 'Charles Dickens', 1861, 'Chapman & Hall', '9780141439563'),
('The Kite Runner', 'Khaled Hosseini', 2003, 'Riverhead Books', '9781594631931'),
('Slaughterhouse-Five', 'Kurt Vonnegut', 1969, 'Delacorte Press', '9780440180296'),
('The Scarlet Letter', 'Nathaniel Hawthorne', 1850, 'Ticknor, Reed & Fields', '9780142437261'),
('Dracula', 'Bram Stoker', 1897, 'Archibald Constable and Company', '9780486411095'),
('The Sun Also Rises', 'Ernest Hemingway', 1926, 'Scribner', '9780743297332'),
('Heart of Darkness', 'Joseph Conrad', 1899, 'Blackwoods Magazine', '9780486264646'),
('The Metamorphosis', 'Franz Kafka', 1915, 'Kurt Wolff Verlag', '9780553213690'),
('Emma', 'Jane Austen', 1815, 'John Murray', '9780141439587'),
('Great Expectations', 'Charles Dickens', 1861, 'Chapman & Hall', '9780141439563'),
('David Copperfield', 'Charles Dickens', 1850, 'Bradbury & Evans', '9780140439441'),
('The Count of Monte Cristo', 'Alexandre Dumas', 1844, 'Penguin Classics', '9780140449266'),
('Frankenstein', 'Mary Shelley', 1818, 'Lackington, Hughes, Harding, Mavor & Jones', '9780486282114'),
('The Picture of Dorian Gray', 'Oscar Wilde', 1890, 'Lippincotts Monthly Magazine', '9780141439570'),
('Sense and Sensibility', 'Jane Austen', 1811, 'Thomas Egerton', '9780141439662'),
('The Old Man and the Sea', 'Ernest Hemingway', 1952, 'Charles Scribners Sons', '9780684801223'),
('The Sound and the Fury', 'William Faulkner', 1929, 'Jonathan Cape and Harrison Smith', '9780679732242'),
('Invisible Man', 'Ralph Ellison', 1952, 'Random House', '9780679732761'),
('Don Quixote', 'Miguel de Cervantes', 1605, 'Francisco de Robles', '9780060934347'),
('Mansfield Park', 'Jane Austen', 1814, 'Thomas Egerton', '9780141439808'),
('Middlemarch', 'George Eliot', 1871, 'William Blackwood', '9780141439549'),
('Ulysses', 'James Joyce', 1922, 'Sylvia Beach', '9780141182803'),
('Gullivers Travels', 'Jonathan Swift', 1726, 'Benjamin Motte', '9780141439495'),
('The Call of the Wild', 'Jack London', 1903, 'Macmillan', '9780486264721'),
('Robinson Crusoe', 'Daniel Defoe', 1719, 'William Taylor', '9780486404271'),
('The Three Musketeers', 'Alexandre Dumas', 1844, 'Penguin Classics', '9780140449266'),
('Treasure Island', 'Robert Louis Stevenson', 1883, 'Cassell & Co.', '9780141439822'),
('Moby-Dick', 'Herman Melville', 1851, 'Harper & Brothers', '9781503280786');
GO


-- Insert sample data into books.book without specifying warehouse_id
INSERT INTO books.book (book_id, quantity, stage) VALUES
(1, 10, 'Available'),
(2, 5, 'Unavailable'),
(3, 8, 'Available'),
(4, 12, 'Unavailable'),
(5, 15, 'Available'),
(6, 7, 'Available'),
(7, 3, 'Unavailable'),
(8, 9, 'Available'),
(9, 11, 'Unavailable'),
(10, 14, 'Available'),
(11, 6, 'Available'),
(12, 4, 'Unavailable'),
(13, 13, 'Available'),
(14, 10, 'Unavailable'),
(15, 5, 'Available'),
(16, 7, 'Available'),
(17, 8, 'Unavailable'),
(18, 11, 'Available'),
(19, 9, 'Unavailable'),
(20, 15, 'Available'),
(21, 14, 'Available'),
(22, 12, 'Unavailable'),
(23, 3, 'Available'),
(24, 6, 'Unavailable'),
(25, 13, 'Available'),
(26, 10, 'Available'),
(27, 5, 'Unavailable'),
(28, 8, 'Available'),
(29, 7, 'Unavailable'),
(30, 9, 'Available'),
(31, 4, 'Available'),
(32, 11, 'Unavailable'),
(33, 15, 'Available'),
(34, 14, 'Unavailable'),
(35, 13, 'Available'),
(36, 12, 'Available'),
(37, 10, 'Unavailable'),
(38, 9, 'Available'),
(39, 8, 'Unavailable'),
(40, 7, 'Available'),
(41, 6, 'Available'),
(42, 5, 'Unavailable'),
(43, 4, 'Available'),
(44, 3, 'Unavailable'),
(45, 11, 'Available'),
(46, 15, 'Available'),
(47, 14, 'Unavailable'),
(48, 13, 'Available'),
(49, 12, 'Unavailable'),
(50, 10, 'Available');
GO


