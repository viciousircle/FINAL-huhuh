import sqlite3
import pyodbc
import pickle

def createDatabase():

    conn = sqlite3.connect('LMS.db')  
    cursor = conn.cursor()  

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users_account (
        admin_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_name  TEXT,
        password    TEXT
        );
    ''')  

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books_bookMarc (
        book_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        title       TEXT,
        author      TEXT,
        public_year INTEGER,
        public_comp TEXT,
        isbn        TEXT
        );
    ''')  
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books_book (
        warehouse_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id     INTEGER,
        isbn        TEXT,
        quantity    INTEGER,
        stage       TEXT,
        FOREIGN KEY (book_id) REFERENCES books_bookMarc(book_id)
        );
    ''')  
    conn.commit()
    conn.close()

def dbToBinFile():
    conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=127.0.0.1,1433;"
    "DATABASE=LMS;"
    "UID=SA;"
    "PWD=MyStrongPass123;"
    "Timeout=30;")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users.account")
    rows = cursor.fetchall()
    with open('account.bin', 'wb') as binFile:
        pickle.dump(rows, binFile)

    cursor.execute("SELECT * FROM books.bookMarc")
    rows = cursor.fetchall()
    with open('bookMarc.bin', 'wb') as binFile:
        pickle.dump(rows, binFile)

    cursor.execute("SELECT * FROM books.book")
    rows = cursor.fetchall()
    with open('book.bin', 'wb') as binFile:
        pickle.dump(rows, binFile)

    conn.close()


def dbBookMarcToBinFile():

    conn = sqlite3.connect('LMS.db')  
    cursor = conn.cursor()  

    cursor.execute("SELECT * FROM books_bookMarc")
    rows = cursor.fetchall()
    with open('bookMarc.bin', 'wb') as binFile:
        pickle.dump(rows, binFile)

    conn.close()

def dbBookToBinFile():
    
    conn = sqlite3.connect('LMS.db')  
    cursor = conn.cursor()  

    cursor.execute("SELECT * FROM books_book")
    rows = cursor.fetchall()
    with open('book.bin', 'wb') as binFile:
        pickle.dump(rows, binFile)

    conn.close()

def binFileToDb():
    conn = sqlite3.connect('LMS.db')  
    cursor = conn.cursor()  

    # with open('account.bin', 'rb') as binFile:
    #     rows = pickle.load(binFile)
    # for row in rows:
    #     cursor.execute("INSERT INTO users_account (admin_id, password, admin_name) VALUES (?, ?, ?)", row)


    # with open('bookMarc.bin', 'rb') as binFile:
    #     rows = pickle.load(binFile)
    # # Insert the data back into the database
    # for row in rows:
    #     cursor.execute("INSERT INTO books_bookMarc (book_id, title, author, public_year, public_comp, isbn) VALUES (?, ?, ?, ?, ?, ?)", row)

    with open('book.bin', 'rb') as binFile:
        rows = pickle.load(binFile)
    # Insert the data back into the database
    for row in rows:
        cursor.execute("INSERT INTO books_book (warehouse_id, book_id, isbn, quantity, stage) VALUES (?, ?, ?, ?, ?)", row)
    conn.commit()
    conn.close()

def deleteDatabase():
    conn = sqlite3.connect('LMS.db')  
    cursor = conn.cursor()  
    # cursor.execute("DROP TABLE users_account")
    # cursor.execute("DROP TABLE books_bookMarc")
    cursor.execute("DROP TABLE books_book")
    conn.commit()
    conn.close()
    
# binFileToDb()

# dbToBinFile()

# createDatabase()

# deleteDatabase()