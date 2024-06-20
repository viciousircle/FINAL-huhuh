import sqlite3
from typing import Optional, Generator, Tuple
from datetime import datetime
import os
from db.lms_types import UsersAccountData, BooksBookMarcData, BooksBookData
from db.data_lms import dbBookMarcToBinFile, dbBookToBinFile

class DBSession:
    """
    A class representing a database session for the LMS (Library Management System).
    """

    def __init__(self) -> None:
        """
        Initializes the DBSession object.
        """
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../db/LMS.db'))
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    # --- LOG IN FUNCTION ------------------------------------------------------

    def logIn(self, admin_id: str, password: str) -> Optional[UsersAccountData]:
        """
        Logs in a user given the admin_id and password.

        Returns:
            UsersAccountData: If login successful, returns the user account data.
            None: If login failed.
        """
        try:
            print("Logging in....")
            query = "SELECT * FROM users_account WHERE admin_id = ? AND password = ?"
            self.cursor.execute(query, (admin_id, password))
            row = self.cursor.fetchone()
            if row:
                print("Login successful")
                return UsersAccountData(*row)
            else:
                print("Login failed")
                return None
        except sqlite3.Error as err:
            print("Database error:", err)
            return None
        except Exception as err:
            print("Unexpected error:", err)
            raise err

    # --- SHOW FILE FUNCTION ---------------------------------------------------

    def showFileBookMarc(self) -> Generator[BooksBookMarcData, None, None]:
        """
        Retrieves and yields all bookmarc data from the database.

        Yields:
            Generator[BooksBookMarcData]: A generator yielding each BooksBookMarcData object.
        """
        try:
            query = "SELECT * FROM books_bookMarc"
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                yield BooksBookMarcData(*row)
        except sqlite3.Error as err:
            print("Error:", err)
            raise err

    def showFileBook(self) -> Generator[BooksBookData, None, None]:
        """
        Retrieves and yields all book data from the database.

        Yields:
            Generator[BooksBookData]: A generator yielding each BooksBookData object.
        """
        try:
            query = "SELECT * FROM books_book"
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                yield BooksBookData(*row)
        except sqlite3.Error as err:
            print("Error:", err)
            raise err

    # --- ADD BOOK FUNCTION ----------------------------------------------------

    def addBook(self, admin_id: int, isbn: str, bookMarcData: Optional[BooksBookMarcData], bookData: BooksBookData) -> Tuple[bool, Optional[str]]:
        """
        Adds a new book to the database.

        Args:
            admin_id (int): The ID of the admin adding the book.
            isbn (str): The ISBN of the book to add.
            bookMarcData (Optional[BooksBookMarcData]): Optional bookmarc data to insert.
            bookData (BooksBookData): Book data to insert.

        Returns:
            Tuple[bool, Optional[str]]: A tuple indicating success status and an error message if failed.
        """
        try:
            existing_book, error = self.getBookByISBN(isbn)

            if existing_book:
                book_id = existing_book.book_id
            else:
                book_id = self.insertBookMarc(bookMarcData)

            self.insertBook(book_id, bookData)

            self.connection.commit()
            dbBookMarcToBinFile()
            dbBookToBinFile()
            return True, None

        except sqlite3.Error as err:
            self.connection.rollback()
            print("SQLite error:", err)
            return False, str(err)

        except Exception as err:
            self.connection.rollback()
            print("Unexpected error:", err)
            return False, str(err)

    def insertBookMarc(self, bookMarcData: BooksBookMarcData) -> int:
        """
        Inserts bookmarc data into the database.

        Args:
            bookMarcData (BooksBookMarcData): The bookmarc data to insert.

        Returns:
            int: The ID of the inserted bookmarc.
        """
        try:
            self.cursor.execute(
                "INSERT INTO books_bookMarc (title, author, public_year, public_comp, isbn) VALUES (?, ?, ?, ?, ?)",
                (bookMarcData.title, bookMarcData.author, bookMarcData.public_year, bookMarcData.public_comp, bookMarcData.isbn)
            )
            self.connection.commit()

            self.cursor.execute("SELECT book_id FROM books_bookMarc WHERE isbn = ?", (bookMarcData.isbn,))
            book_id = self.cursor.fetchone()[0]
            return book_id

        except sqlite3.Error as err:
            self.connection.rollback()
            print("SQLite error:", err)
            raise err
        except Exception as err:
            self.connection.rollback()
            print("Unexpected error:", err)
            raise err

    def insertBook(self, book_id: int, bookData: BooksBookData) -> None:
        """
        Inserts book data into the database.

        Args:
            book_id (int): The ID of the book to insert.
            bookData (BooksBookData): The book data to insert.
        """
        try:
            self.cursor.execute(
                "INSERT INTO books_book (book_id, isbn, quantity, stage) VALUES (?, ?, ?, ?)",
                (book_id, bookData.isbn, bookData.quantity, bookData.stage)
            )
            self.connection.commit()

        except sqlite3.Error as err:
            self.connection.rollback()
            print("SQLite error:", err)
            raise err
        except Exception as err:
            self.connection.rollback()
            print("Unexpected error:", err)
            raise err

    # --- GET BOOK FUNCTION ----------------------------------------------------

    def getBookByISBN(self, isbn: str) -> Optional[Tuple[BooksBookMarcData, str]]:
        """
        Retrieves a book by its ISBN.

        Args:
            isbn (str): The ISBN of the book to retrieve.

        Returns:
            Optional[Tuple[BooksBookMarcData, str]]: A tuple containing bookmarc data and error message if failed.
        """
        try:
            self.cursor.execute("SELECT * FROM books_bookMarc WHERE isbn = ?", (isbn,))

            row = self.cursor.fetchone()
            if row:
                bookMarcData = BooksBookMarcData(
                    title=row[1],
                    author=row[2],
                    public_year=row[3],
                    public_comp=row[4],
                    isbn=row[5],
                    book_id=row[0]
                )

                return (bookMarcData, None)
            else:
                return (None, 'Book not found')

        except sqlite3.Error as err:
            print(f"SQLite error: {err}")
            return None, str(err)
        except Exception as err:
            print(f"Error: {err}")
            return None, str(err)

    def getBookByIdAndWarehouseId(self, book_id: int, warehouse_id: int) -> Optional[Tuple[BooksBookMarcData, BooksBookData]]:
        """
        Retrieves a book by its ID and warehouse ID.

        Args:
            book_id (int): The ID of the book to retrieve.
            warehouse_id (int): The ID of the warehouse.

        Returns:
            Optional[Tuple[BooksBookMarcData, BooksBookData]]: A tuple containing bookmarc and book data if found, else None.
        """
        try:
            query = """
                SELECT BM.book_id, BM.title, BM.author, BM.isbn, BM.public_year, BM.public_comp, BD.warehouse_id, BD.quantity, BD.stage
                FROM books_bookMarc BM
                JOIN books_book BD ON BM.book_id = BD.book_id
                WHERE BM.book_id = ? AND BD.warehouse_id = ?
            """
            self.cursor.execute(query, (book_id, warehouse_id))
            row = self.cursor.fetchone()
            if row:
                bookMarcData = BooksBookMarcData(
                    title=row[1],
                    author=row[2],
                    isbn=row[3],
                    public_year=row[4],
                    public_comp=row[5],
                    book_id=row[0]
                )
                bookData = BooksBookData(
                    warehouse_id=row[6],
                    quantity=row[7],
                    stage=row[8],
                    book_id=row[0],
                    isbn=row[3]
                )
                return (bookMarcData, bookData)
            else:
                return None

        except sqlite3.Error as err:
            print(f"SQLite error: {err}")
            return None
        except Exception as err:
            print(f"Error: {err}")
            return None

    # --- EDIT BOOK FUNCTION --------------------------------------------------
    
    def updateBook(self, admin_id: int, bookMarcData: BooksBookMarcData, bookData: BooksBookData, old_bookMarcData: Optional[BooksBookMarcData] = None, old_bookData: Optional[BooksBookData] = None) -> Tuple[bool, Optional[str]]:
        """
        Updates book and bookmarc data in the database.

        Args:
            admin_id (int): The ID of the admin updating the book.
            bookMarcData (BooksBookMarcData): The updated bookmarc data.
            bookData (BooksBookData): The updated book data.
            old_bookMarcData (Optional[BooksBookMarcData]): The old bookmarc data if provided.
            old_bookData (Optional[BooksBookData]): The old book data if provided.

        Returns:
            Tuple[bool, Optional[str]]: A tuple indicating success status and an error message if failed.
        """
        try:
            self.connection.isolation_level = None

            # Update BookData if old data is provided and there are changes
            if old_bookData is not None:
                if bookData.isbn != old_bookData.isbn:
                    update_query = "UPDATE books_book SET isbn = ? WHERE isbn = ?"
                    self.cursor.execute(update_query, (bookData.isbn, old_bookData.isbn))
                update_query = "UPDATE books_book SET "
                params = []
                if bookData.quantity != old_bookData.quantity:
                    update_query += "quantity = ?, "
                    params.append(bookData.quantity)
                if bookData.stage != old_bookData.stage:
                    update_query += "stage = ?, "
                    params.append(bookData.stage)
                if update_query.endswith(", "):
                    update_query = update_query[:-2]
                    update_query += " WHERE warehouse_id = ?"
                    params.append(bookData.warehouse_id)
                    self.cursor.execute(update_query, params)

            # Update BookMarcData if old data is provided and there are changes
            if old_bookMarcData is not None:
                params = []
                update_query = "UPDATE books_bookMarc SET "
                if bookMarcData.title != old_bookMarcData.title:
                    update_query += "title = ?, "
                    params.append(bookMarcData.title)
                if bookMarcData.author != old_bookMarcData.author:
                    update_query += "author = ?, "
                    params.append(bookMarcData.author)
                if bookMarcData.isbn != old_bookMarcData.isbn:
                    # Check if the new ISBN is already in the database
                    self.cursor.execute("SELECT COUNT(*) FROM books_bookMarc WHERE isbn = ? AND book_id != ?", (bookMarcData.isbn, old_bookMarcData.book_id))
                    if self.cursor.fetchone()[0] > 0:
                        self.connection.rollback()
                        return False, f"ISBN {bookMarcData.isbn} is already assigned to another book."
                    update_query += "isbn = ?, "
                    params.append(bookMarcData.isbn)
                if bookMarcData.public_year != old_bookMarcData.public_year:
                    update_query += "public_year = ?, "
                    params.append(bookMarcData.public_year)
                if bookMarcData.public_comp != old_bookMarcData.public_comp:
                    update_query += "public_comp = ?, "
                    params.append(bookMarcData.public_comp)
                if update_query.endswith(", "):
                    update_query = update_query[:-2]  # Remove the trailing comma and space
                    update_query += " WHERE isbn = ?"
                    params.append(old_bookMarcData.isbn)
                    self.cursor.execute(update_query, params)

            # Commit the transaction if all updates succeed
            dbBookMarcToBinFile()
            dbBookToBinFile()
            self.connection.commit()
            return True, None

        except sqlite3.Error as err:
            self.connection.rollback()
            return False, str(err)

        except Exception as err:
            self.connection.rollback()
            return False, str(err)

        finally:
            # Ensure auto-commit is turned back on
            self.connection.isolation_level = ""

    def deleteBook(self, admin_id: int, bookMarcData: BooksBookMarcData, bookData: BooksBookData) -> Tuple[bool, str]:
        """
        Deletes a book from the database.

        Args:
            admin_id (int): The ID of the admin deleting the book.
            bookMarcData (BooksBookMarcData): The bookmarc data to delete.
            bookData (BooksBookData): The book data to delete.

        Returns:
            Tuple[bool, str]: A tuple indicating success status and a message.
        """
        try:
            isbn = bookMarcData.isbn
            warehouse_id = bookData.warehouse_id

            # Check how many entries exist for the given ISBN
            query = "SELECT warehouse_id FROM books_book WHERE isbn = ?"
            self.cursor.execute(query, (isbn,))
            rows = self.cursor.fetchall()

            if not rows:
                # No books found with the given ISBN
                return False, f"Book with ISBN {isbn} not found"

            if len(rows) > 1:
                # Multiple entries found, delete only from the specified warehouse
                query = "DELETE FROM books_book WHERE warehouse_id = ? AND isbn = ?"
                self.cursor.execute(query, (warehouse_id, isbn))
            else:
                # Single entry found, delete from both book and bookMarc tables
                query = "DELETE FROM books_book WHERE isbn = ?"
                self.cursor.execute(query, (isbn,))
                query = "DELETE FROM books_bookMarc WHERE isbn = ?"
                self.cursor.execute(query, (isbn,))

            self.connection.commit()
            dbBookMarcToBinFile()
            dbBookToBinFile()
            return True, "Book deleted successfully"

        except sqlite3.Error as err:
            self.connection.rollback()
            return False, str(err)

        except Exception as err:
            self.connection.rollback()
            return False, str(err)

    # --- SEARCH BOOK FUNCTION -------------------------------------------------

    def searchBook(self, filter_criteria: Optional[str] = None, filter_value: Optional[str] = None) -> Generator[Tuple[int, str, str, int, Optional[str]], None, None]:
        """
        Searches for books in the database based on filter criteria.

        Args:
            filter_criteria (Optional[str]): The column name to filter by.
            filter_value (Optional[str]): The value to filter for.

        Yields:
            Generator[Tuple[int, str, str, int, Optional[str]]]: A generator yielding tuples of book information.
        """
        try:
            additional_column = None
            params = []

            if filter_criteria and filter_value:
                # Determine the table and column to filter by
                if filter_criteria in ['book_id', 'title', 'author', 'isbn', 'public_year', 'public_comp']:
                    table = 'BM'
                else:
                    table = 'B'

                if filter_criteria not in ['book_id', 'title', 'isbn', 'warehouse_id']:
                    additional_column = f"{table}.{filter_criteria}"
                    query = f"""
                        SELECT BM.book_id, BM.title, BM.isbn, B.warehouse_id, {additional_column}
                        FROM books_bookMarc BM
                        JOIN books_book B ON BM.book_id = B.book_id
                        WHERE {table}.{filter_criteria} LIKE ?
                    """
                else:
                    query = f"""
                        SELECT BM.book_id, BM.title, BM.isbn, B.warehouse_id
                        FROM books_bookMarc BM
                        JOIN books_book B ON BM.book_id = B.book_id
                        WHERE {table}.{filter_criteria} LIKE ?
                    """
                params = (f"%{filter_value}%",)
            else:
                # If no filter criteria, search in every relevant column in both tables
                query = """
                    SELECT BM.book_id, BM.title, BM.isbn, B.warehouse_id
                    FROM books_bookMarc BM
                    JOIN books_book B ON BM.book_id = B.book_id
                    WHERE BM.book_id LIKE ?
                    OR BM.title LIKE ?
                    OR BM.author LIKE ?
                    OR BM.isbn LIKE ?
                    OR BM.public_year LIKE ?
                    OR BM.public_comp LIKE ?
                    OR B.warehouse_id LIKE ?
                    OR B.quantity LIKE ?
                    OR B.stage LIKE ?
                """
                params = (
                    f"%{filter_value}%", f"%{filter_value}%", f"%{filter_value}%", f"%{filter_value}%", f"%{filter_value}%",
                    f"%{filter_value}%", f"%{filter_value}%", f"%{filter_value}%", f"%{filter_value}%"
                )

            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()

            for row in rows:
                if filter_criteria and filter_value and additional_column:
                    yield (row[0], row[1], row[2], row[3], row[4])
                else:
                    yield (row[0], row[1], row[2], row[3])

        except sqlite3.Error as err:
            print(f"Database error: {err}")
        except Exception as err:
            print(f"Error: {err}")

    def countNumberOfBooks(self) -> int:
        """
        Counts the number of books in the database.

        Returns:
            int: The count of books.
        """
        try:
            self.cursor.execute("SELECT COUNT(*) FROM books_bookMarc")
            return self.cursor.fetchone()[0]
        except sqlite3.Error as err:
            print(f"SQLite error: {err}")
            raise err

    def countQuantityOfBooks(self) -> int:
        """
        Counts the total quantity of books in the database.

        Returns:
            int: The total quantity of books.
        """
        try:
            self.cursor.execute("SELECT SUM(quantity) FROM books_book")
            return self.cursor.fetchone()[0] or 0
        except sqlite3.Error as err:
            print(f"SQLite error: {err}")
            raise err

    def get10NewAddedBooks(self) -> Generator[BooksBookMarcData, None, None]:
        """
        Retrieves the 10 most recently added books from the database.

        Yields:
            Generator[BooksBookMarcData, None, None]: A generator yielding BooksBookMarcData objects.
        """
        try:
            query = "SELECT * FROM books_bookMarc ORDER BY book_id DESC LIMIT 10"
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                yield BooksBookMarcData(*row)
        except sqlite3.Error as err:
            print(f"SQLite error: {err}")
            raise err

    def connect(self) -> None:
        """
        Connects to the SQLite database.
        """
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../db/LMS.db'))
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def close(self) -> None:
        """
        Closes the SQLite database connection.
        """
        self.cursor.close()
        self.connection.close()

