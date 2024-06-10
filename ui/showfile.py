# -------IMPORTS------------------------------------------
from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget, QPushButton, QStackedWidget, QWidget

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_session import DBSession
from lms_types import BooksBookMarcData, BooksBookData
# ---------------------------------------------------------

# ------SHOWFILE_UI CLASS---------------------------------
class ShowFile_UI:
    # List of objects in .ui file related to this module
    show_file_1             : QPushButton
    show_file_2             : QPushButton
    files_stackedWidget     : QStackedWidget
    blank_page              : QWidget 
    bookMarc_page           : QWidget
    book_page               : QWidget
    bookMarc_table          : QTableWidget
    book_table              : QTableWidget
    
    def __init__(self, ui, db_session: DBSession):
        self.ui         = ui
        self.db_session = db_session
        
        self.buttons_open = [
            self.ui.show_file_1,
            self.ui.show_file_2,
        ]
        
        # Link database to the table files
        self.showFileBookMarc()
        self.showFileBook()
        
        # Show file_page
        self.ui.show_file_1.clicked.connect(lambda: self.ui.files_stackedWidget.setCurrentWidget(self.ui.bookMarc_page))
        self.ui.show_file_2.clicked.connect(lambda: self.ui.files_stackedWidget.setCurrentWidget(self.ui.book_page))
        
    def showFileBookMarc(self):
        # Fetch data from the database
        data = list(self.db_session.showFileBookMarc())

        # Assuming you have a QTableWidget named bookMarc_table in your UI
        self.ui.bookMarc_table.setRowCount(len(data))

        # Set the column count based on the number of fields in BooksBookMarcData
        column_count = len(BooksBookMarcData.__annotations__)
        self.ui.bookMarc_table.setColumnCount(column_count)  

        for row_idx, book_marc_data in enumerate(data):
            for col_idx, field_name in enumerate(BooksBookMarcData.__annotations__):
                value = getattr(book_marc_data, field_name)
                self.ui.bookMarc_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        
        self.ui.bookMarc_table.resizeColumnsToContents()

    def showFileBook(self):
        # Fetch data from the database
        data = list(self.db_session.showFileBook())

        # Assuming you have a QTableWidget named book_table in your UI
        self.ui.book_table.setRowCount(len(data))

        # Set the column count based on the number of fields in BooksBookData
        column_count = len(BooksBookData.__annotations__)
        self.ui.book_table.setColumnCount(column_count)  

        for row_idx, book_data in enumerate(data):
            for col_idx, field_name in enumerate(BooksBookData.__annotations__):
                value = getattr(book_data, field_name)
                self.ui.book_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        
        self.ui.book_table.resizeColumnsToContents()

    
    def updateBookMarcTable(self):
        self.ui.bookMarc_table.clearContents()
        self.showFileBookMarc()
    
    def updateBookTable(self):
        self.ui.book_table.clearContents()
        self.showFileBook()
