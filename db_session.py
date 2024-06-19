
# -------IMPORTS------------------------------------------
import pyodbc
from typing import Optional, Generator, Tuple
from datetime import datetime
from lms_types import UsersAccountData, UsersHistoryData, UsersGuestData, BooksBookMarcData, BooksBookData, ExecuteResult

# nhớ chỉnh lại cái username
# -------CONNECT TO DATABASE------------------------------------------
DRIVER_NAME = "sql"  # Adjust the driver name if necessary
SERVER_NAME = "8d7c731e1269"  # Replace with your actual SQL Server hostname or IP
DATABASE_NAME = "LMS"  # Replace with your actual database name

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=127.0.0.1,1433;"
    "DATABASE=LMS;"
    "UID=SA;"
    "PWD=MyStrongPass123;"
    "Timeout=30;"
)



# -------DBSESSION CLASS------------------------------------------
class DBSession:
    # Define the connection and cursor as class variables
    connection  : pyodbc.Connection
    cursor      : pyodbc.Cursor
    
    connection  = pyodbc.connect(connection_string)
    cursor      = connection.cursor()
    print("DBSession initialized....................")

    def __init__(self) -> None:
        pass
    
    # --- LOG IN FUNCTION ------------------------------------------
    def logIn(self, admin_id: str, password: str) -> Optional[UsersAccountData]:
        try:
            print("Logging in....")
            query = "SELECT * FROM users.account WHERE admin_id = ? AND password = ?"
            self.cursor.execute(query, (admin_id, password))
            row = self.cursor.fetchone()
            if row:
                print("Login successful")
                return UsersAccountData(*row)
            else:
                print("Login failed")
                return None
        except pyodbc.Error as err:
            print("Database error:", err)  
            return None
        except Exception as err:
            print("Unexpected error:", err)  
            raise err

    
    def getAdmin(self, admin_id: int) -> Optional[UsersAccountData]:
        try:
            self.cursor.execute("SELECT * FROM users.admin WHERE admin_id = ?", (admin_id))
            row = self.cursor.fetchone()
            if row:
                return UsersAccountData(*row)
            else:
                return None
        except Exception as err:
            return None        

    def recordGuestLogIn(self, guest_name: str) -> ExecuteResult[None]:
        try:
            self.cursor.execute("INSERT INTO users.guest (guest_name, timestamp) VALUES (?, ?)", (guest_name, datetime.now()))
            self.connection.commit()
            return (True, None)
        except pyodbc.Error as err:
            self.connection.rollback()
            return (False, str(err))
        except Exception as err:
            return (False, str(err))
        
    # --- SHOW FILE FUNCTION ------------------------------------------
    def showFileBookMarc(self) -> Generator[BooksBookMarcData, None, None]:
        try:
            query = "SELECT * FROM books.bookMarc"
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                yield BooksBookMarcData(*row)
        except Exception as err:
            print("Error:", err)
            raise err
        
    def showFileBook(self) -> Generator[BooksBookData, None, None]:
        try:
            query = "SELECT * FROM books.book"
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                yield BooksBookData(*row)
        except Exception as err:
            print("Error:", err)
            raise err
        
    # --- ADD BOOK FUNCTION ------------------------------------------
    def addBook(self, admin_id: int,isbn, bookMarcData: Optional[BooksBookMarcData], bookData: BooksBookData) -> ExecuteResult[None]:
        try:

            existing_book, error = self.getBookByISBN(isbn)

            if existing_book:
                book_id = existing_book.book_id
                print(book_id)
            else:
                book_id = self.insertBookMarc(bookMarcData)
                print(book_id)

            print("Added book marc")
            self.insertBook(book_id, bookData)

            # Log the addition in history
            # self.logHistory(admin_id, book_id, bookData.isbn, bookData.warehouse_id, datetime.now())

            self.connection.commit()
            return (True, None)
        
        except pyodbc.Error as err:
            self.connection.rollback()
            print(5)
            return (False, str(err))
        
        except Exception as err:
            self.connection.rollback()
            print(6)
            return (False, str(err))
        
    def insertBookMarc(self, bookMarcData: BooksBookMarcData) -> int:
        try:
            self.cursor.execute(
                "INSERT INTO books.bookMarc (title, author, public_year, public_comp, isbn) VALUES (?, ?, ?, ?, ?)",
                (bookMarcData.title, bookMarcData.author, bookMarcData.public_year, bookMarcData.public_comp, bookMarcData.isbn)
            )
            self.connection.commit()
            self.cursor.execute("SELECT book_id FROM books.bookMarc WHERE isbn = ?", bookMarcData.isbn)
            book_id = self.cursor.fetchone()[0]
            return book_id

            
        except pyodbc.Error as err:
            self.connection.rollback()
            print("Database error:", err)
            raise err
        except Exception as err:
            self.connection.rollback()
            print("Unexpected error:", err)
            raise err

    def insertBook(self, book_id: int, bookData: BooksBookData) -> None:
        # Insert bookData into the book table
        self.cursor.execute(
            "INSERT INTO books.book (book_id, isbn, quantity, stage) VALUES (?, ?, ?, ?)",
            (book_id, bookData.isbn, bookData.quantity, bookData.stage)
        )          
        self.connection.commit()
        
                
    # --- EDIT BOOK FUNCTION ------------------------------------------
    def getBookById(self, book_id: int) -> Optional[Tuple[BooksBookMarcData, BooksBookData]]:
        try:
            query = """
                SELECT BM.book_id, BM.title, BM.author, BM.isbn, BM.public_year, BM.public_comp, BD.warehouse_id, BD.quantity, BD.stage
                FROM books.bookMarc BM
                JOIN books.book BD ON BM.book_id = BD.book_id
                WHERE BM.book_id = ?
            """
            self.cursor.execute(query, (book_id,))
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
        except Exception as err:
            print("Error:", err)
            return None            


    def getBookByISBN(self, isbn: str) -> Optional[Tuple[BooksBookMarcData, None]]:
        try:
            self.cursor.execute("SELECT * FROM books.bookMarc WHERE isbn = ?", (isbn,))
            
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
                return (None,'Book not found')
            

        except pyodbc.Error as err:
            print(f"Database error: {err}")
            return None
        except Exception as err:
            print(f"Error: {err}")
            return None
           
    def getBookByIdAndWarehouseId(self, book_id: int, warehouse_id: int) -> Optional[Tuple[BooksBookMarcData, BooksBookData]]:
        try:
            query = """
                SELECT BM.book_id, BM.title, BM.author, BM.isbn, BM.public_year, BM.public_comp, BD.warehouse_id, BD.quantity, BD.stage
                FROM books.bookMarc BM
                JOIN books.book BD ON BM.book_id = BD.book_id
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
        except Exception as err:
            print("Error:", err)
            return None
  

    def updateBook(self, admin_id: int, bookMarcData: BooksBookMarcData, bookData: BooksBookData, old_bookMarcData: Optional[BooksBookMarcData] = None, old_bookData: Optional[BooksBookData] = None) -> ExecuteResult[None]:
        try:
            # Start a transaction by ensuring auto-commit is off
            self.connection.autocommit = False

            # Update BookData if old data is provided and there are changes
            if old_bookData is not None:
                if bookData.isbn != old_bookData.isbn:   
                    update_query = "UPDATE books.book SET isbn = ? WHERE isbn = ?"
                    self.cursor.execute(update_query, (bookData.isbn, old_bookData.isbn))
                update_query = "UPDATE books.book SET "
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
                update_query = "UPDATE books.bookMarc SET "
                params = []
                if bookMarcData.title != old_bookMarcData.title:
                    update_query += "title = ?, "
                    params.append(bookMarcData.title)
                if bookMarcData.author != old_bookMarcData.author:
                    update_query += "author = ?, "
                    params.append(bookMarcData.author)
                if bookMarcData.isbn != old_bookMarcData.isbn:
                    # Check if the new ISBN is already in the database
                    self.cursor.execute("SELECT COUNT(*) FROM books.bookMarc WHERE isbn = ? AND book_id != ?", (bookMarcData.isbn, old_bookMarcData.book_id))
                    if self.cursor.fetchone()[0] > 0:
                        self.connection.rollback()
                        return (False, f"ISBN {bookMarcData.isbn} is already assigned to another book.")
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
            self.connection.commit()

        except pyodbc.Error as err:
            self.connection.rollback()
            return (False, str(err))
        except Exception as err:
            self.connection.rollback()
            return (False, str(err))
        finally:
            # Ensure auto-commit is turned back on
            self.connection.autocommit = True

        return (True, None)
    
    def deleteBook(self, admin_id: int, bookMarcData: BooksBookMarcData, bookData: BooksBookData) -> ExecuteResult[None]:
        try:
            isbn = bookMarcData.isbn
            warehouse_id = bookData.warehouse_id

            print(isbn)
            print(warehouse_id)

            # Check how many entries exist for the given ISBN
            query = "SELECT warehouse_id FROM books.book WHERE isbn = ?"
            self.cursor.execute(query, (isbn,))
            rows = self.cursor.fetchall()

            if not rows:
                # No books found with the given ISBN
                return (False, f"Book with ISBN {isbn} not found")

            if len(rows) > 1:
                # Multiple entries found, delete only from the specified warehouse
                query = "DELETE FROM books.book WHERE warehouse_id = ? AND isbn = ?"
                self.cursor.execute(query, (warehouse_id, isbn))
            else:
                query = "DELETE FROM books.book WHERE isbn = ?"
                self.cursor.execute(query, (isbn,))
                # Single entry found, delete from both book and bookMarc tables
                query = "DELETE FROM books.bookMarc WHERE isbn = ?"
                self.cursor.execute(query, (isbn,))

            self.connection.commit()
            return (True, "Book deleted successfully")

        except pyodbc.Error as err:
            self.connection.rollback()
            return (False, str(err))

        except Exception as err:
            self.connection.rollback()
            return (False, str(err))


    # --- SEARCH BOOK FUNCTION ------------------------------------------
    def searchBook(self, filter_criteria: Optional[str] = None, filter_value: Optional[str] = None) -> Generator[Tuple[int, str, str, int, Optional[str]], None, None]:
        try:
            additional_column = None
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
                        FROM books.bookMarc BM
                        JOIN books.book B ON BM.book_id = B.book_id
                        WHERE {table}.{filter_criteria} LIKE ?
                    """
                else:
                    query = f"""
                        SELECT BM.book_id, BM.title, BM.isbn, B.warehouse_id
                        FROM books.bookMarc BM
                        JOIN books.book B ON BM.book_id = B.book_id
                        WHERE {table}.{filter_criteria} LIKE ?
                    """
                params = (f"%{filter_value}%",)
            else:
                # If no filter criteria, search in every relevant column in both tables
                query = """
                    SELECT BM.book_id, BM.title, BM.isbn, B.warehouse_id
                    FROM books.bookMarc BM
                    JOIN books.book B ON BM.book_id = B.book_id
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

        except pyodbc.Error as err:
            print(f"Database error: {err}")
        except Exception as err:
            print(f"Error: {err}")

            
    # --- SHOW HISTORY FUNCTION ------------------------------------------
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
    
    
    def logHistory(self, admin_id: int, book_id: Optional[int], isbn: Optional[str], warehouse_id: Optional[int], timestamp: datetime):
        try:
            self.cursor.execute("""
                INSERT INTO users.history (admin_id, book_id, isbn, warehouse_id, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (admin_id, book_id, isbn, warehouse_id, timestamp))
            self.connection.commit()

        except pyodbc.Error as err:
            self.connection.rollback()
            raise err
        except Exception as err:
            raise err   

    # --- SHOW USERS FUNCTION ------------------------------------------
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
        
    def countNumberOfBooks(self) -> int:
        try:
            self.cursor.execute("SELECT COUNT(*) FROM books.bookMarc")
            return self.cursor.fetchone()[0]
        except Exception as err:
            raise err
        
    def countQuantityOfBooks(self) -> int:
        try:
            self.cursor.execute("SELECT SUM(quantity) FROM books.book")
            return self.cursor.fetchone()[0]
        except Exception as err:
            raise err
        
    def get10NewAddedBooks(self) -> Generator[BooksBookMarcData, None, None]:
        try:
            query = "SELECT * FROM books.bookMarc ORDER BY book_id DESC LIMIT 10"
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                yield BooksBookMarcData(*row)
        except Exception as err:
            raise err
        

    def close(self) -> None:
        self.cursor.close()
        self.connection.close()

