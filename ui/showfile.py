# -------IMPORTS------------------------------------------
from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget, QPushButton, QStackedWidget, QWidget, QHeaderView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_session import DBSession
from lms_types import BooksBookMarcData, BooksBookData

# ------SHOWFILE_UI CLASS---------------------------------
class ShowFile_UI:
    
    # List of objects in .ui file related to this module
    show_file_BookMarc      : QPushButton
    show_file_Book          : QPushButton
    
    files_stackedWidget     : QStackedWidget
    blank_page              : QWidget 
    bookMarc_page           : QWidget
    book_page               : QWidget
    
    bookMarc_table          : QTableWidget
    book_table              : QTableWidget
    
    def __init__(self, ui, db_session: DBSession):
        # Connect objects in the .ui file to the variables in this module
        self.ui         = ui
        # Connect database session
        self.db_session = db_session
        
        self.buttons_open = [
            self.ui.show_file_BookMarc,
            self.ui.show_file_Book,
        ]
        
        # Link database to the table files
        self.ui.show_file_BookMarc.clicked.connect(self.showFileBookMarc)
        self.ui.show_file_Book.clicked.connect(self.showFileBook)
        
        # Show file_page
        self.ui.show_file_BookMarc.clicked.connect(lambda: self.ui.files_stackedWidget.setCurrentWidget(self.ui.bookMarc_page))
        self.ui.show_file_Book.clicked.connect(lambda: self.ui.files_stackedWidget.setCurrentWidget(self.ui.book_page))
        
        
    def showFileBookMarc(self):
        print("Show File BookMarc.....")
        data = list(self.db_session.showFileBookMarc())

        self.ui.bookMarc_table.setRowCount(len(data))

        # Set the column headers explicitly
        column_headers = ["Book ID", "Title", "Author", "Public Year", "Public Company", "ISBN"]
        self.ui.bookMarc_table.setColumnCount(len(column_headers))

        # Set column headers
        for col_idx, header in enumerate(column_headers):
            item = QTableWidgetItem(header)
            font = item.font()
            font.setBold(True)
            item.setFont(font)
            self.ui.bookMarc_table.setHorizontalHeaderItem(col_idx, item)

        for row_idx, book_marc_data in enumerate(data):
            for col_idx, field_name in enumerate(BooksBookMarcData.__annotations__):
                value   = getattr(book_marc_data, field_name)
                item    = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ui.bookMarc_table.setItem(row_idx, col_idx, item)

        self.ui.bookMarc_table.resizeColumnsToContents()
        self.adjustColumnWidths(self.ui.bookMarc_table)
        print("Done Show File BookMarc.....")

    def showFileBook(self):
        print("Show File Book.....")
        data = list(self.db_session.showFileBook())

        self.ui.book_table.setRowCount(len(data))

        # Set the column headers explicitly
        column_headers = ["Warehouse ID", "Book ID", "ISBN", "Quantity", "Stage"]
        self.ui.book_table.setColumnCount(len(column_headers))

        # Set column headers
        for col_idx, header in enumerate(column_headers):
            item = QTableWidgetItem(header)
            font = item.font()
            font.setBold(True)
            item.setFont(font)
            self.ui.book_table.setHorizontalHeaderItem(col_idx, item)

        for row_idx, book_data in enumerate(data):
            for col_idx, field_name in enumerate(BooksBookData.__annotations__):
                value   = getattr(book_data, field_name)
                item    = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ui.book_table.setItem(row_idx, col_idx, item)

        self.ui.book_table.resizeColumnsToContents()
        self.adjustColumnWidths(self.ui.book_table)
        print("Done Show File Book.....")
    
    def adjustColumnWidths(self, table_widget: QTableWidget):
        # Set the header to resize to fill the available space
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Optionally, resize rows to fit content
        table_widget.resizeRowsToContents()

    def updateBookMarcTable(self):
        print("Update BookMarc Table.....")
        self.ui.bookMarc_table.clearContents()
        self.showFileBookMarc()
        print("Done Update BookMarc Table.....")
    
    def updateBookTable(self):
        print("Update Book Table.....")
        self.ui.book_table.clearContents()
        self.showFileBook()
        print("Done Update Book Table.....")
