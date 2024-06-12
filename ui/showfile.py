# -------IMPORTS------------------------------------------
from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget, QPushButton, QStackedWidget, QWidget, QHeaderView

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_session import DBSession
from lms_types import BooksBookMarcData, BooksBookData
# ---------------------------------------------------------

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
        self.ui         = ui
        self.db_session = db_session
        
        self.buttons_open = [
            self.ui.show_file_BookMarc,
            self.ui.show_file_Book,
        ]
        
        # Link database to the table files
        self.showFileBookMarc()
        self.showFileBook()
        
        # Show file_page
        self.ui.show_file_BookMarc.clicked.connect(lambda: self.ui.files_stackedWidget.setCurrentWidget(self.ui.bookMarc_page))
        self.ui.show_file_Book.clicked.connect(lambda: self.ui.files_stackedWidget.setCurrentWidget(self.ui.book_page))
        
        
    def showFileBookMarc(self):
        data = list(self.db_session.showFileBookMarc())

        self.ui.bookMarc_table.setRowCount(len(data))

        column_count = len(BooksBookMarcData.__annotations__)
        self.ui.bookMarc_table.setColumnCount(column_count)  

        for row_idx, book_marc_data in enumerate(data):
            for col_idx, field_name in enumerate(BooksBookMarcData.__annotations__):
                value = getattr(book_marc_data, field_name)
                self.ui.bookMarc_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        
        self.ui.bookMarc_table.resizeColumnsToContents()
        self.adjustColumnWidth(self.ui.bookMarc_table)

    def showFileBook(self):
        
        data = list(self.db_session.showFileBook())

        self.ui.book_table.setRowCount(len(data))

        column_count = len(BooksBookData.__annotations__)
        self.ui.book_table.setColumnCount(column_count)  

        for row_idx, book_data in enumerate(data):
            for col_idx, field_name in enumerate(BooksBookData.__annotations__):
                value = getattr(book_data, field_name)
                self.ui.book_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        
        self.ui.book_table.resizeColumnsToContents()
        self.adjustColumnWidth(self.ui.book_table)

    def adjustColumnWidth(self, table_widget: QTableWidget):
        # Set the header to resize to fill the available space
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Optionally, resize rows to fit content
        table_widget.resizeRowsToContents()


    def updateBookMarcTable(self):
        self.ui.bookMarc_table.clearContents()
        self.showFileBookMarc()
    
    def updateBookTable(self):
        self.ui.book_table.clearContents()
        self.showFileBook()
