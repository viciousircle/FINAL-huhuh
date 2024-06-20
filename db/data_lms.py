import sqlite3
import pickle
import os

# Absolute path to the LMS.db database file
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../db/LMS.db'))

def dbBookMarcToBinFile():
    """
    This function reads data from the books_bookMarc table in the LMS.db database
    and writes that data to a binary file named bookMarc.bin.
    """
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Execute a query to retrieve all data from the books_bookMarc table
    cursor.execute("SELECT * FROM books_bookMarc")
    rows = cursor.fetchall()  # Fetch all the resulting rows
    
    # Write the data to a binary file named bookMarc.bin
    with open('bookMarc.bin', 'wb') as binFile:
        pickle.dump(rows, binFile)
    
    # Close the database connection
    conn.close()

def dbBookToBinFile():
    """
    This function reads data from the books_book table in the LMS.db database
    and writes that data to a binary file named book.bin.
    """
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Execute a query to retrieve all data from the books_book table
    cursor.execute("SELECT * FROM books_book")
    rows = cursor.fetchall()  # Fetch all the resulting rows
    
    # Write the data to a binary file named book.bin
    with open('book.bin', 'wb') as binFile:
        pickle.dump(rows, binFile)
    
    # Close the database connection
    conn.close()
