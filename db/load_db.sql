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

DROP TABLE users.account;
DROP TABLE users.history;
DROP TABLE users.guest;
DROP TABLE books.bookMarc;
DROP TABLE books.book;




GO
-- Insert sample data into user.account
INSERT INTO users.account (admin_id, password, admin_name) VALUES
(100001, '5', 'John Doe'),
(100002, '7', 'Jane Smith'),
(100003, '2', 'Michael Johnson'),
(100004, '9', 'Emily Davis'),
(100005, '4', 'Chris Wilson'),
(100006, '1', 'Sarah Brown'),
(100007, '8', 'David Martinez'),
(100008, '3', 'Jessica Thompson'),
(100009, '6', 'Kevin Garcia'),
(100010, '0', 'Lisa Miller');

INSERT INTO users.history (admin_id, book_id, isbn, warehouse_id, [timestamp]) VALUES
(100001, 1, '9780618640157', 1, GETDATE()),
(100002, 2, '9780156907392', 2, GETDATE()),
(100003, 3, '9780060883287', 3, GETDATE()),
(100004, 4, '9780143039433', 4, GETDATE()),
(100005, 5, '9780143035008', 5, GETDATE()),
(100006, 6, '9780374528379', 6, GETDATE()),
(100007, 7, '9780393964813', 7, GETDATE()),
(100008, 8, '9781503290204', 8, GETDATE()),
(100009, 9, '9780140280493', 9, GETDATE()),
(100010, 10, '9780679734505', 10, GETDATE()),
(100001, 11, '9780141439556', 11, GETDATE()),
(100002, 12, '9780060934347', 12, GETDATE()),
(100003, 13, '9780307265432', 13, GETDATE()),
(100004, 14, '9780142437209', 14, GETDATE()),
(100005, 15, '9780385333849', 15, GETDATE()),
(100006, 16, '9780141180144', 16, GETDATE()),
(100007, 17, '9780316921176', 17, GETDATE()),
(100008, 18, '9780141439549', 18, GETDATE()),
(100009, 19, '9780486282114', 19, GETDATE()),
(100010, 20, '9780805210106', 20, GETDATE()),
(100001, 21, '9780743273565', 21, GETDATE()),
(100002, 22, '9780061120084', 22, GETDATE()),
(100003, 23, '9780451524935', 23, GETDATE()),
(100004, 24, '9781503290563', 24, GETDATE()),
(100005, 25, '9780316769488', 25, GETDATE()),
(100006, 26, '9780547928227', 26, GETDATE()),
(100007, 27, '9781451673319', 27, GETDATE()),
(100008, 28, '9781503280786', 28, GETDATE()),
(100009, 29, '9781400079988', 29, GETDATE()),
(100010, 30, '9780140268867', 30, GETDATE()),
(100001, 31, '9780747538493', 31, GETDATE()),
(100002, 32, '9780385121675', 32, GETDATE()),
(100003, 33, '9780385490818', 33, GETDATE()),
(100004, 34, '9780062315007', 34, GETDATE()),
(100005, 35, '9780671250676', 35, GETDATE()),
(100006, 36, '9780195014761', 36, GETDATE()),
(100007, 37, '9780307269751', 37, GETDATE()),
(100008, 38, '9780486280615', 38, GETDATE()),
(100009, 39, '9780385199574', 39, GETDATE()),
(100010, 40, '9780060850524', 40, GETDATE()),
(100001, 41, '9780140444308', 41, GETDATE()),
(100002, 42, '9780375842207', 42, GETDATE()),
(100003, 43, '9780393312836', 43, GETDATE()),
(100004, 44, '9780226320557', 44, GETDATE()),
(100005, 45, '9780486280486', 45, GETDATE()),
(100006, 46, '9780553561745', 46, GETDATE()),
(100007, 47, '9780486264646', 47, GETDATE()),
(100008, 48, '9780571081783', 48, GETDATE()),
(100009, 49, '9780141392463', 49, GETDATE()),
(100010, 50, '9780679412716', 50, GETDATE());



-- Insert sample data into user.guest
INSERT INTO users.guest (guest_id, guest_name, [timestamp]) VALUES
(1, 'Hoa', '2023-01-01 09:00:00'),
(2, 'Nam', '2023-01-02 10:00:00'),
(3, 'Lan', '2023-01-03 11:00:00'),
(4, 'Hai', '2023-01-04 12:00:00'),
(5, 'Dung', '2023-01-05 13:00:00');
GO

-- Insert data into books.bookMarc for 50 books
INSERT INTO books.bookMarc (title, author, public_year, public_comp, isbn) 
VALUES
('The Lord of the Rings', 'J.R.R. Tolkien', 1954, 'George Allen & Unwin', '9780618640157'),
('To the Lighthouse', 'Virginia Woolf', 1927, 'The Hogarth Press', '9780156907392'),
('One Hundred Years of Solitude', 'Gabriel García Márquez', 1967, 'Harper & Row', '9780060883287'),
('The Grapes of Wrath', 'John Steinbeck', 1939, 'The Viking Press', '9780143039433'),
('Anna Karenina', 'Leo Tolstoy', 1877, 'The Russian Messenger', '9780143035008'),
('The Brothers Karamazov', 'Fyodor Dostoevsky', 1880, 'The Russian Messenger', '9780374528379'),
('The Sound and the Fury', 'William Faulkner', 1929, 'Jonathan Cape & Harrison Smith', '9780393964813'),
('The Picture of Dorian Gray', 'Oscar Wilde', 1890, 'Ward, Lock, and Company', '9781503290204'),
('Beloved', 'Toni Morrison', 1987, 'Alfred A. Knopf', '9780140280493'),
('Crime and Punishment', 'Fyodor Dostoevsky', 1866, 'The Russian Messenger', '9780679734505'),
('Wuthering Heights', 'Emily Brontë', 1847, 'Thomas Cautley Newby', '9780141439556'),
('Don Quixote', 'Miguel de Cervantes', 1605, 'Francisco de Robles', '9780060934347'),
('The Road', 'Cormac McCarthy', 2006, 'Knopf', '9780307265432'),
('Jane Eyre', 'Charlotte Brontë', 1847, 'Smith, Elder & Co.', '9780142437209'),
('Slaughterhouse-Five', 'Kurt Vonnegut', 1969, 'Delacorte Press', '9780385333849'),
('The Master and Margarita', 'Mikhail Bulgakov', 1967, 'Harvill Press', '9780141180144'),
('Infinite Jest', 'David Foster Wallace', 1996, 'Little, Brown and Company', '9780316921176'),
('Middlemarch', 'George Eliot', 1871, 'William Blackwood and Sons', '9780141439549'),
('Frankenstein', 'Mary Shelley', 1818, 'Lackington, Hughes, Harding, Mavor, & Jones', '9780486282114'),
('The Trial', 'Franz Kafka', 1925, 'S. Fischer Verlag', '9780805210106'),
('The Great Gatsby', 'F. Scott Fitzgerald', 1925, 'Scribner', '9780743273565'),
('To Kill a Mockingbird', 'Harper Lee', 1960, 'J.B. Lippincott & Co.', '9780061120084'),
('1984', 'George Orwell', 1949, 'Secker & Warburg', '9780451524935'),
('Pride and Prejudice', 'Jane Austen', 1813, 'T. Egerton', '9781503290563'),
('The Catcher in the Rye', 'J.D. Salinger', 1951, 'Little, Brown and Company', '9780316769488'),
('The Hobbit', 'J.R.R. Tolkien', 1937, 'George Allen & Unwin', '9780547928227'),
('Fahrenheit 451', 'Ray Bradbury', 1953, 'Ballantine Books', '9781451673319'),
('Moby-Dick', 'Herman Melville', 1851, 'Harper & Brothers', '9781503280786'),
('War and Peace', 'Leo Tolstoy', 1869, 'The Russian Messenger', '9781400079988'),
('The Odyssey', 'Homer', 800, 'Penguin Classics', '9780140268867'),
('Harry Potter and the Chamber of Secrets', 'J.K. Rowling', 1998, 'Bloomsbury Publishing', '9780747538493'),
('The Shining', 'Stephen King', 1977, 'Doubleday', '9780385121675'),
('The Handmaid''s Tale', 'Margaret Atwood', 1985, 'McClelland and Stewart', '9780385490818'),
('The Alchemist', 'Paulo Coelho', 1988, 'HarperCollins', '9780062315007'),
('The Road Less Traveled', 'M. Scott Peck', 1978, 'Simon & Schuster', '9780671250676'),
('The Art of War', 'Sun Tzu', 500, 'Oxford University Press', '9780195014761'),
('The Girl with the Dragon Tattoo', 'Stieg Larsson', 2005, 'Norstedts förlag', '9780307269751'),
('The Adventures of Huckleberry Finn', 'Mark Twain', 1884, 'Chatto & Windus', '9780486280615'),
('The Stand', 'Stephen King', 1978, 'Doubleday', '9780385199574'),
('Brave New World', 'Aldous Huxley', 1932, 'Chatto & Windus', '9780060850524'),
('Les Misérables', 'Victor Hugo', 1862, 'A. Lacroix, Verboeckhoven & Cie.', '9780140444308'),
('The Book Thief', 'Markus Zusak', 2005, 'Knopf', '9780375842207'),
('A Clockwork Orange', 'Anthony Burgess', 1962, 'William Heinemann', '9780393312836'),
('The Road to Serfdom', 'Friedrich Hayek', 1944, 'Routledge', '9780226320557'),
('The Scarlet Letter', 'Nathaniel Hawthorne', 1850, 'Ticknor, Reed & Fields', '9780486280486'),
('The Brothers K', 'David James Duncan', 1992, 'Bantam Books', '9780553561745'),
('Heart of Darkness', 'Joseph Conrad', 1899, 'Blackwood''s Magazine', '9780486264646'),
('The Bell Jar', 'Sylvia Plath', 1963, 'Heinemann', '9780571081783'),
('The Count of Monte Cristo', 'Alexandre Dumas', 1844, 'Pétion et compère', '9780141392463'),
('Meditations', 'Marcus Aurelius', 180, 'Various', '9780679412716');
GO



-- Insert data into books.book for 50 books
INSERT INTO books.book (book_id, isbn, quantity, stage) VALUES
(1, '9780618640157', 100, 'Available'),
(2, '9780156907392', 101, 'Available'),
(3, '9780060883287', 102, 'Available'),
(4, '9780143039433', 103, 'Available'),
(5, '9780143035008', 104, 'Available'),
(6, '9780374528379', 105, 'Available'),
(7, '9780393964813', 106, 'Available'),
(8, '9781503290204', 107, 'Available'),
(9, '9780140280493', 108, 'Available'),
(10, '9780679734505', 109, 'Available'),
(11, '9780141439556', 110, 'Available'),
(12, '9780060934347', 111, 'Available'),
(13, '9780307265432', 112, 'Available'),
(14, '9780142437209', 113, 'Available'),
(15, '9780385333849', 114, 'Available'),
(16, '9780141180144', 115, 'Available'),
(17, '9780316921176', 116, 'Available'),
(18, '9780141439549', 117, 'Available'),
(19, '9780486282114', 118, 'Available'),
(20, '9780805210106', 119, 'Available'),
(21, '9780743273565', 120, 'Available'),
(22, '9780061120084', 121, 'Available'),
(23, '9780451524935', 122, 'Available'),
(24, '9781503290563', 123, 'Available'),
(25, '9780316769488', 124, 'Available'),
(26, '9780547928227', 125, 'Available'),
(27, '9781451673319', 126, 'Available'),
(28, '9781503280786', 127, 'Available'),
(29, '9781400079988', 128, 'Available'),
(30, '9780140268867', 129, 'Available'),
(31, '9780747538493', 130, 'Available'),
(32, '9780385121675', 131, 'Available'),
(33, '9780385490818', 132, 'Available'),
(34, '9780062315007', 133, 'Available'),
(35, '9780671250676', 134, 'Available'),
(36, '9780195014761', 135, 'Available'),
(37, '9780307269751', 136, 'Available'),
(38, '9780486280615', 137, 'Available'),
(39, '9780385199574', 138, 'Available'),
(40, '9780060850524', 139, 'Available'),
(41, '9780140444308', 140, 'Available'),
(42, '9780375842207', 141, 'Available'),
(43, '9780393312836', 142, 'Available'),
(44, '9780226320557', 143, 'Available'),
(45, '9780486280486', 144, 'Available'),
(46, '9780553561745', 145, 'Available'),
(47, '9780486264646', 146, 'Available'),
(48, '9780571081783', 147, 'Available'),
(49, '9780141392463', 148, 'Available'),
(50, '9780679412716', 149, 'Available');

GO
