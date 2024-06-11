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
(030504, 'vuminhquy0305', 'Vu Minh Quy'),
(160105, 'dunghoang1601', 'Do Hoang Dung'),
(010101, 'viciousircle', 'Vicious Circle');
GO

-- Insert sample data into user.history
INSERT INTO users.history (edit_id, admin_id, book_id, [timestamp]) VALUES
(1, 030504, 1, '2023-01-01 09:00:00'),
(2, 160105, 2, '2023-01-02 10:00:00'),
(3, 010101, 3, '2023-01-03 11:00:00');
GO


-- Insert sample data into user.guest
INSERT INTO users.guest (guest_id, guest_name, [timestamp]) VALUES
(1, 'Nam', '2023-01-01 09:00:00'),
(2, 'Hoa', '2023-01-02 10:00:00'),
(3, 'Lan', '2023-01-03 11:00:00'),
(4, 'Hai', '2023-01-04 12:00:00'),
(5, 'Dung', '2023-01-05 13:00:00');
GO

-- Insert sample data into book.bookMarc
INSERT INTO books.bookMarc (title, author, public_year, public_comp, isbn) VALUES
('To Kill a Mockingbird', 'Harper Lee', 1960, 'J.B. Lippincott & Co.', '978-0061120084'),
('1984', 'George Orwell', 1949, 'Secker & Warburg', '978-0451524935'),
('The Great Gatsby', 'F. Scott Fitzgerald', 1925, 'Charles Scribners Sons', '978-0743273565'),
('The Catcher in the Rye', 'J.D. Salinger', 1951, 'Little, Brown and Company', '978-0316769488'),
('The Grapes of Wrath', 'John Steinbeck', 1939, 'The Viking Press', '978-0143039433'),
('The Lord of the Rings', 'J.R.R. Tolkien', 1954, 'Allen & Unwin', '978-0618640157'),
('The Hobbit', 'J.R.R. Tolkien', 1937, 'Allen & Unwin', '978-0618260300'),
('Pride and Prejudice', 'Jane Austen', 1813, 'T. Egerton', '978-1503290563'),
('Moby-Dick', 'Herman Melville', 1851, 'Harper & Brothers', '978-1503280786'),
('War and Peace', 'Leo Tolstoy', 1869, 'The Russian Messenger', '978-0199232765'),
('Ulysses', 'James Joyce', 1922, 'Shakespeare and Company', '978-0199535675'),
('The Odyssey', 'Homer', -800, 'Ancient Greece', '978-0140268867'),
('Madame Bovary', 'Gustave Flaubert', 1857, 'Revue de Paris', '978-0140449129'),
('The Divine Comedy', 'Dante Alighieri', 1320, 'Italy', '978-0142437223'),
('Alices Adventures in Wonderland', 'Lewis Carroll', 1865, 'Macmillan', '978-1503222687'),
('Wuthering Heights', 'Emily Brontë', 1847, 'Thomas Cautley Newby', '978-0141439556'),
('Crime and Punishment', 'Fyodor Dostoevsky', 1866, 'The Russian Messenger', '978-0143058144'),
('The Brothers Karamazov', 'Fyodor Dostoevsky', 1880, 'The Russian Messenger', '978-0374528379'),
('Great Expectations', 'Charles Dickens', 1861, 'Chapman & Hall', '978-0141439563'),
('One Hundred Years of Solitude', 'Gabriel García Márquez', 1967, 'Harper & Row', '978-0060883287'),
('Don Quixote', 'Miguel de Cervantes', 1615, 'Francisco de Robles', '978-0060934347'),
('The Sound and the Fury', 'William Faulkner', 1929, 'Jonathan Cape and Harrison Smith', '978-0679732242'),
('Catch-22', 'Joseph Heller', 1961, 'Simon & Schuster', '978-1451626650'),
('The Bell Jar', 'Sylvia Plath', 1963, 'Heinemann', '978-0060837020'),
('Brave New World', 'Aldous Huxley', 1932, 'Chatto & Windus', '978-0060850524'),
('Invisible Man', 'Ralph Ellison', 1952, 'Random House', '978-0679732760'),
('Beloved', 'Toni Morrison', 1987, 'Alfred A. Knopf', '978-1400033416'),
('Lolita', 'Vladimir Nabokov', 1955, 'Olympia Press', '978-0679723164'),
('The Stranger', 'Albert Camus', 1942, 'Gallimard', '978-0679720200'),
('Jane Eyre', 'Charlotte Brontë', 1847, 'Smith, Elder & Co.', '978-0142437209'),
('Anna Karenina', 'Leo Tolstoy', 1877, 'The Russian Messenger', '978-0143035008'),
('Fahrenheit 451', 'Ray Bradbury', 1953, 'Ballantine Books', '978-1451673319'),
('The Sun Also Rises', 'Ernest Hemingway', 1926, 'Scribner', '978-0743297332'),
('Middlemarch', 'George Eliot', 1871, 'William Blackwood and Sons', '978-0141439549'),
('Frankenstein', 'Mary Shelley', 1818, 'Lackington, Hughes, Harding, Mavor & Jones', '978-0486282114'),
('Dracula', 'Bram Stoker', 1897, 'Archibald Constable and Company', '978-0486411095'),
('The Picture of Dorian Gray', 'Oscar Wilde', 1890, 'Lippincotts Monthly Magazine', '978-0141439570'),
('Heart of Darkness', 'Joseph Conrad', 1899, 'Blackwoods Magazine', '978-0141441672'),
('The Metamorphosis', 'Franz Kafka', 1915, 'Kurt Wolff Verlag', '978-0553213690'),
('The Iliad', 'Homer', -750, 'Ancient Greece', '978-0140275360'),
('Les Misérables', 'Victor Hugo', 1862, 'A. Lacroix, Verboeckhoven & Cie.', '978-0451419439'),
('A Tale of Two Cities', 'Charles Dickens', 1859, 'Chapman & Hall', '978-0141439600'),
('Sense and Sensibility', 'Jane Austen', 1811, 'Thomas Egerton', '978-0141439662'),
('David Copperfield', 'Charles Dickens', 1850, 'Bradbury & Evans', '978-0140439441'),
('The Old Man and the Sea', 'Ernest Hemingway', 1952, 'Charles Scribners Sons', '978-0684801223'),
('Mansfield Park', 'Jane Austen', 1814, 'Thomas Egerton', '978-0141439808'),
('Emma', 'Jane Austen', 1815, 'John Murray', '978-0141439587'),
('The Scarlet Letter', 'Nathaniel Hawthorne', 1850, 'Ticknor, Reed & Fields', '978-0142437261'),
('Treasure Island', 'Robert Louis Stevenson', 1883, 'Cassell and Company', '978-0141439815'),
('The Count of Monte Cristo', 'Alexandre Dumas', 1844, 'Penguin Classics', '978-0140449266');
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


