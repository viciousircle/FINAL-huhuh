
# -------IMPORTS------------------------------------------
import pyodbc
from typing import Optional, Generator, Tuple
from datetime import datetime
from lms_types import UsersAccountData, UsersHistoryData, UsersGuestData, BooksBookMarcData, BooksBookData, ExecuteResult
# ---------------------------------------------------------

# nhớ chỉnh lại cái username
# -------CONNECT TO DATABASE------------------------------------------
DRIVER_NAME = "SQL Server"
SERVER_NAME = "DESKTOP-BS6RK24\\SQLEXPRESS"
DATABASE_NAME = "LMS"

connection_string = f"""
    DRIVER={DRIVER_NAME};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trusted_Connection = yes;
"""
# ---------------------------------------------------------------   

# -------DBSESSION CLASS------------------------------------------
class DBSession:
    # Define the connection and cursor as class variables
    connection  : pyodbc.Connection
    cursor      : pyodbc.Cursor
    
    connection  = pyodbc.connect(connection_string)
    cursor      = connection.cursor()
    print("DBSession initialized")

    def __init__(self) -> None:
        pass
    
    # --- LOG IN FUNCTION ------------------------------------------
    def logIn(self, admin_id: str, password: str) -> Optional[UsersAccountData]:
        try:
            query = "SELECT * FROM users.account WHERE admin_id = ? AND password = ?"
            self.cursor.execute(query, (admin_id, password))
            row = self.cursor.fetchone()
            if row:
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
            raise err
        
    def showFileBook(self) -> Generator[BooksBookData, None, None]:
        try:
            query = "SELECT * FROM books.book"
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                yield BooksBookData(*row)
        except Exception as err:
            raise err
        
     
    # --- ADD BOOK FUNCTION ------------------------------------------
    def addBook(self, bookMarcData: BooksBookMarcData, bookData: BooksBookData) -> ExecuteResult[None]:
        try:
            # Check if the ISBN is already in the database
            self.cursor.execute("SELECT * FROM books.bookMarc WHERE isbn = ?", (bookMarcData.isbn,))

            existing_book = self.cursor.fetchone()
            
            if existing_book:
                # If ISBN exists, get Book by ISBN
                bookMarcData = BooksBookMarcData(
                    title=existing_book[1],
                    author=existing_book[2],
                    public_year=existing_book[3],
                    public_comp=existing_book[4],
                    isbn=existing_book[5]
                )
                
                book_id = existing_book[0]
                
                # Insert data into BookData table
                self.cursor.execute(
                    "INSERT INTO books.book (book_id, isbn ,quantity, stage) VALUES (?, ?, ?)",
                    (book_id, bookMarcData.isbn , bookData.quantity, bookData.stage)
                )
                self.connection.commit()
                
                return (True, None)
            else:
                # If ISBN does not exist, insert new Book
                # Insert data into BookMarcData table
                self.cursor.execute(
                    "INSERT INTO books.bookMarc (title, author, isbn, public_year, public_comp) VALUES (?, ?, ?, ?, ?)",
                    (bookMarcData.title, bookMarcData.author, bookMarcData.isbn, bookMarcData.public_year, bookMarcData.public_comp)
                )

                print("BookMarcData inserted")

                # Get the last inserted book ID using SCOPE_IDENTITY()
                self.cursor.execute("SELECT SCOPE_IDENTITY()")
                book_id = self.cursor.fetchone()[0]
                print("Book ID:", book_id)
                
                # Insert data into BookData table
                self.cursor.execute(
                    "INSERT INTO books.book (book_id, isbn ,quantity, stage) VALUES (?, ?, ?)",
                    (book_id, bookMarcData.isbn , bookData.quantity, bookData.stage)
                )
                self.connection.commit()
                print("BookData inserted")

                # Get the last inserted warehouse ID using SCOPE_IDENTITY()
                self.cursor.execute("SELECT SCOPE_IDENTITY()")
                warehouse_id = self.cursor.fetchone()[0]
                print("Warehouse ID:", warehouse_id)
                return (True, None)
            
        except pyodbc.Error as err:
            self.connection.rollback()
            if "duplicate key" in str(err).lower():
                return (False, "Duplicate book ID or warehouse ID detected.")
            else:
                return (False, str(err))

        except Exception as err:
            self.connection.rollback()
            return (False, str(err))
            
    
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
            print("Row:", row)
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
                    book_id=row[0]
                )
                print("Book found")
                return (bookMarcData, bookData)
            else:
                return None
        except Exception as err:
            return None            

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
                if bookMarcData.public_comp != old_bookMarcData.public_comp:
                    update_query += "public_comp = ?, "
                    params.append(bookMarcData.public_comp)

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
    
    # --- SEARCH BOOK FUNCTION ------------------------------------------
    def searchBook(self, filter_criteria: Optional[str] = None, filter_value: Optional[str] = None) -> Generator[Tuple[str, int, str], None, None]:
        try:
            # Define the base query with the common columns
            query = """
                SELECT BD.book_id, BM.title 
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
            print("Query:", query)
            # Add WHERE clause based on the filter criteria and value
            if filter_criteria and filter_value:
                query += f" WHERE BM.{filter_criteria} = ? "
                params.append(filter_value)
            print("Query:", query)
            print("Params:", params)

            

            self.cursor.execute(query, params)
            print("Query executed")
            for row in self.cursor.fetchall():
                yield row
            print("Rows fetched")
                
            
        except Exception as err:
            return err
    

        
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

