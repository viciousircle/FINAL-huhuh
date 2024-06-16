
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
    def addBook(self, admin_id: int, book_id: Optional[int], bookMarcData: Optional[BooksBookMarcData], bookData: BooksBookData) -> ExecuteResult[None]:
        try:
            print("Adding book")

            # Check if the book with the given ISBN already exists in the BookMarc table
            existing_book, error = self.getBookByISBN(bookData.isbn)

            if existing_book:
                # If the book exists in BookMarc, use its book_id to insert into Book table
                book_id = existing_book.book_id
                print("Book ID:", book_id)
            else:
                # If the book doesn't exist in BookMarc, insert it and get the generated book_id
                book_id = self.insertBookMarc(bookMarcData)
                print("Book ID:", book_id)

            # Insert the book into the Book table using bookData
            self.insertBook(book_id, bookData)
            print("Book inserted successfully")

            # Log the addition in history
            self.logHistory(admin_id, book_id, bookData.isbn, bookData.warehouse_id, datetime.now())

            self.connection.commit()
            return (True, None)
        
        except pyodbc.Error as err:
            self.connection.rollback()
            print("Database error:", err)
            return (False, str(err))
        
        except Exception as err:
            self.connection.rollback()
            print("Unexpected error:", err)
            return (False, str(err))

    def insertBookMarc(self, bookMarcData: BooksBookMarcData) -> int:
        try:
            self.cursor.execute(
                "INSERT INTO books.bookMarc (title, author, public_year, public_comp, isbn) VALUES (?, ?, ?, ?, ?)",
                (bookMarcData.title, bookMarcData.author, bookMarcData.public_year, bookMarcData.public_comp, bookMarcData.isbn)
            )
            self.connection.commit()
            self.cursor.execute("SELECT SCOPE_IDENTITY()")
            
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
                    update_query += " WHERE book_id = ?"
                    params.append(old_bookMarcData.book_id)

                    self.cursor.execute(update_query, params)
                    self.connection.commit()

                    # Log the update in history
                    self.logHistory(admin_id, old_bookMarcData.book_id if old_bookMarcData else None, old_bookMarcData.isbn if old_bookMarcData else None, old_bookData.warehouse_id if old_bookData else None, datetime.now())

        except pyodbc.Error as err:
            self.connection.rollback()
            return (False, str(err))
        except Exception as err:
            return (False, str(err))

        return (True, None)

    def deleteBook(self, warehouse_id, book_id: int, admin_id: int) -> tuple[bool, str]:
        try:
            # Retrieve the ISBN and warehouse_ids from the books.book table before deletion
            self.cursor.execute("""
                SELECT BM.book_id, BM.isbn, B.warehouse_id
                FROM books.bookMarc BM
                JOIN books.book B ON BM.book_id = B.book_id
                WHERE BM.book_id = ?
            """, (book_id,))
            rows = self.cursor.fetchall()
            
            if not rows:
                return False, "Book not found."

            # Determine the number of distinct warehouse_ids associated with the book_id
            warehouse_ids = {row.warehouse_id for row in rows}

            if len(warehouse_ids) > 1:
                # More than one warehouse_id, delete only from books.book
                self.cursor.execute("DELETE FROM books.book WHERE book_id = ? AND isbn = ? AND warehouse_id = ?", (book_id, rows[0].isbn, warehouse_id))
                warehouse_id = None  # Set warehouse_id to None for history record
            else:
                # Only one warehouse_id, delete from both books.book and books.bookMarc
                self.cursor.execute("DELETE FROM books.book WHERE book_id = ? AND isbn = ?", (book_id, rows[0].isbn))
                self.cursor.execute("DELETE FROM books.bookMarc WHERE book_id = ? AND isbn = ?", (book_id, rows[0].isbn))
                warehouse_id = rows[0].warehouse_id  # Use the existing warehouse_id for history record

            # Insert the deletion record into users.history
            self.cursor.execute("""
                INSERT INTO users.history (admin_id, isbn, book_id, warehouse_id, timestamp)
                VALUES (?, ?, ?, ?, ?)   
            """, (admin_id, rows[0].isbn, None, warehouse_id, datetime.now()))

            self.connection.commit()
            return True, None

        except pyodbc.Error as err:
            self.connection.rollback()
            return False, str(err)

        except Exception as err:
            return False, str(err)
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
        

    def close(self) -> None:
        self.cursor.close()
        self.connection.close()

