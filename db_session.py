import pyodbc
from typing import Optional, Generator, Callable, Union, Tuple
from datetime import datetime
from lms_types import UsersAccountData, UsersHistoryData, UsersGuestData, BooksBookMarcData, BooksBookData, ExecuteResult

# from .lms_types import UserData, BookData, BookBorrowHistoryData, BookBorrowReviewData, BookReturnReviewData, ExecuteResult


# nhớ chỉnh lại cái username
# ----------------------------------------------
DRIVER_NAME = "SQL Server"
SERVER_NAME = "DESKTOP-BS6RK24\\SQLEXPRESS"
DATABASE_NAME = "LMS"

connection_string = f"""
    DRIVER={DRIVER_NAME};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trusted_Connection=yes;
"""

conn = pyodbc.connect(connection_string)
print("Connected to database")
print(conn)     
# ----------------------------------------------    

class DBSession:
    connection: pyodbc.Connection

    cursor: pyodbc.Cursor
    
    
    def __init__(self) -> None:
        """
        Initialize the DBSession class with a database connection and cursor.
        """
        self.connection = pyodbc.connect(connection_string)
        self.cursor = self.connection.cursor()
        
        # print("DBSession initialized")
        
    def addBook(self, bookMarcData: BooksBookMarcData, bookData: BooksBookData) -> ExecuteResult[None]:
        
        try:
            # Insert data into BookMarcData table
            self.cursor.execute(
                "INSERT INTO books.bookMarc (book_id, title, author, isbn, public_year, public_comp) VALUES (?, ?, ?, ?, ?, ?)",
                (bookMarcData.book_id, bookMarcData.title, bookMarcData.author, bookMarcData.isbn, bookMarcData.public_year, bookMarcData.public_company)
            )
            self.connection.commit()

            # Get the last inserted book ID
            self.cursor.execute("SELECT @@IDENTITY")
            book_id = self.cursor.fetchone()[0]

            # Insert data into BookData table
            self.cursor.execute(
                "INSERT INTO books.book (book_id, warehouse_id, quantity, stage) VALUES (?, ?, ?, ?)",
                (book_id, bookData.warehouse_id, bookData.quantity, bookData.stage)
            )
            self.connection.commit()

            return (True, book_id)

        except pyodbc.Error as err:
            # Check if the error is related to duplicate book_id or warehouse_id
            if "duplicate key" in str(err).lower():
                return (False, f"Duplicate book ID or warehouse ID detected.")
            else:
                self.connection.rollback()
                return (False, str(err))

        except Exception as err:
            return (False, str(err))
    
    
    def updateBook(self, bookMarcData: BooksBookMarcData, bookData: BooksBookData, old_bookMarcData: Optional[BooksBookMarcData] = None, old_bookData: Optional[BooksBookData] = None) -> ExecuteResult[None]:
        try:
            # Check if book_id exists
            if old_bookMarcData is not None and old_bookMarcData.book_id is not None:
                self.cursor.execute("SELECT COUNT(*) FROM books.bookMarc WHERE book_id = ?", (old_bookMarcData.book_id,))
                if self.cursor.fetchone()[0] == 0:
                    return (False, f"Book with ID {old_bookMarcData.book_id} does not exist.")

            # Update BookMarcData if old data is provided and there are changes
            if old_bookMarcData is not None:
                update_query = "UPDATE books.bookMarc SET "
                params = []
                if bookMarcData.title != old_bookMarcData.title:
                    update_query += "title = ?, "
                    params.append(bookMarcData.title)
                if bookMarcData.author != old_bookMarcData.author:
                    update_query += "author = ?, "
                    params.append(bookMarcData.author)
                if bookMarcData.isbn != old_bookMarcData.isbn:
                    update_query += "isbn = ?, "
                    params.append(bookMarcData.isbn)
                if bookMarcData.public_year != old_bookMarcData.public_year:
                    update_query += "public_year = ?, "
                    params.append(bookMarcData.public_year)
                if bookMarcData.public_company != old_bookMarcData.public_company:
                    update_query += "public_company = ?, "
                    params.append(bookMarcData.public_company)

                if update_query.endswith(", "):
                    update_query = update_query[:-2]  # Remove the trailing comma and space
                    update_query += " WHERE book_id = ?"
                    params.append(old_bookMarcData.book_id)

                    self.cursor.execute(update_query, params)
                    self.connection.commit()


            # Update BookData if old data is provided and there are changes
            if old_bookData is not None:
                update_query = "UPDATE books.book SET "
                params = []
                
                if bookData.warehouse_id is not None:
                    self.cursor.execute("SELECT COUNT(*) FROM books.book WHERE warehouse_id = ? AND book_id != ?", (bookData.warehouse_id, old_bookMarcData.book_id))
                    if self.cursor.fetchone()[0] > 0:
                        return (False, f"Warehouse ID {bookData.warehouse_id} is already assigned to another book.")
                if bookData.warehouse_id != old_bookData.warehouse_id:
                    update_query += "warehouse_id = ?, "
                    params.append(bookData.warehouse_id)
                if bookData.quantity != old_bookData.quantity:
                    update_query += "quantity = ?, "
                    params.append(bookData.quantity)
                if bookData.stage != old_bookData.stage:
                    update_query += "stage = ?, "
                    params.append(bookData.stage)

                if update_query.endswith(", "):
                    update_query = update_query[:-2]  # Remove the trailing comma and space
                    update_query += " WHERE book_id = ?"
                    params.append(bookMarcData.book_id)

                    self.cursor.execute(update_query, params)
                    self.connection.commit()

            return (True, None)
        
        except pyodbc.Error as err:
            self.connection.rollback()
            return (False, str(err))
        except Exception as err:
            return (False, str(err))
            
    def searchBook(self, filter_criteria: Optional[str] = None, filter_value: Optional[str] = None, order_by: Optional[str] = None) -> Generator[Tuple[str, int, str], None, None]:
        try:
            # Define the base query with the common columns
            query = """
                SELECT BM.title, BD.book_id
                FROM books.bookMarc BM
                JOIN books.book BD ON BM.book_id = BD.book_id
            """

            params = []

            # Adjust the SELECT statement based on the filter criteria
            if filter_criteria != "book_id" and filter_criteria != "title":
                query = f"""
                    SELECT BD.{filter_criteria}, BD.book_id, BM.title
                    FROM books.book BD
                    JOIN books.bookMarc BM ON BD.book_id = BM.book_id
                """

            # Add WHERE clause based on the filter criteria and value
            if filter_criteria and filter_value:
                query += f" WHERE BM.{filter_criteria} = ? "
                params.append(filter_value)

            # Add ORDER BY clause based on the order_by parameter
            if order_by:
                query += f" ORDER BY {order_by}"

            self.cursor.execute(query, params)
            for row in self.cursor.fetchall():
                yield row
        except Exception as err:
            return None
    
    def showFileBookMarc(self) -> Generator[BooksBookMarcData, None, None]:
        try:
            query = "SELECT * FROM books.bookMarc"
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                yield BooksBookMarcData(*row)
        except Exception as err:
            raise err
        
    def showFileBook(self) -> Generator[BooksBookData, None, None]:
        try:
            query = "SELECT * FROM books.book"
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                yield BooksBookData(*row)
        except Exception as err:
            raise err
        
    def showHistory(self) -> Generator[UsersHistoryData, None, None]:
        try:
            query = "SELECT * FROM users.history"
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                yield UsersHistoryData(*row)
        except Exception as err:
            raise err
        
    def showTop10History(self) -> Generator[UsersHistoryData, None, None]:
        try:
            query = "SELECT * FROM users.history ORDER BY timestamp DESC LIMIT 10"
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                yield UsersHistoryData(*row)
        except Exception as err:
            raise err
        
    def showGuest(self) -> Generator[UsersGuestData, None, None]:
        try:
            query = "SELECT * FROM users.guest"
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                yield UsersGuestData(*row)
        except Exception as err:
            raise err
    
    def showAdminHistory(self, admin_id: int) -> Generator[UsersHistoryData, None, None]:
        try:
            query = "SELECT * FROM users.history WHERE admin_id = ?"
            self.cursor.execute(query, (admin_id,))
            for row in self.cursor.fetchall():
                yield UsersHistoryData(*row)
        except Exception as err:
            raise err
            
        
        
    def getGuestCount(self) -> int:
        try:
            self.cursor.execute("SELECT COUNT(*) FROM users.guest")
            return self.cursor.fetchone()[0]
        except Exception as err:
            raise err
        
    def getAdmin(self, admin_id: int) -> Optional[UsersAccountData]:
        try:
            self.cursor.execute("SELECT * FROM users.admin WHERE admin_id = ?", (admin_id,))
            row = self.cursor.fetchone()
            if row:
                return UsersAccountData(*row)
            else:
                return None
        except Exception as err:
            return None    
        
    def close(self) -> None:
        self.cursor.close()
        self.connection.close()
    