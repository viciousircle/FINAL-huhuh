# FULL NAME: Vũ Thị Minh Quý
# MSSV: 20227257
# CLASS: 150328
# PROJECT: 04 - Library Management System
# DATE: 20/06/2024 
# -----IMPORTS------------------------------------
from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget, QPushButton, QStackedWidget, QWidget, QHeaderView
from PyQt6.QtCore import Qt
from typing import Optional
import sys
import os

# Ensure the project root is in the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import database related modules and types
from db.db_session import DBSession
from db.lms_types import BooksBookMarcData, BooksBookData

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
        """
        Initialize the ShowFile_UI instance.

        Args:
        - ui: The UI instance containing necessary widgets.
        - db_session: Database session object for querying data.
        """
        # Connect objects in the .ui file to the variables in this module
        self.ui = ui
        # Connect database session
        self.db_session = db_session
        
        # Define list of buttons for navigation
        self.buttons_open = [
            self.ui.show_file_BookMarc,
            self.ui.show_file_Book,
        ]
        
        # Initialize last clicked page button
        self.lastClickedPageButton: Optional[QPushButton] = None
        
        # Connect each button to pageButtonClicked function
        for button in self.buttons_open:
            button.clicked.connect(lambda checked, b=button: self.pageButtonClicked(b))

        # Link database to the table files
        self.ui.show_file_BookMarc.clicked.connect(self.showFileBookMarc)
        self.ui.show_file_Book.clicked.connect(self.showFileBook)
        
        # Show file_page based on button click
        self.ui.show_file_BookMarc.clicked.connect(lambda: self.ui.files_stackedWidget.setCurrentWidget(self.ui.bookMarc_page))
        self.ui.show_file_Book.clicked.connect(lambda: self.ui.files_stackedWidget.setCurrentWidget(self.ui.book_page))
        
        
    def showFileBookMarc(self):
        """
        Retrieve and display book MARC data in the bookMarc_table.
        """
        data = list(self.db_session.showFileBookMarc())

        self.ui.bookMarc_table.setRowCount(len(data))

        # Set the column headers explicitly
        column_headers = ["Book ID", "Title", "Author", "Public Year", "Public Company", "ISBN"]
        self.ui.bookMarc_table.setColumnCount(len(column_headers))

        # Set column headers with bold font
        for col_idx, header in enumerate(column_headers):
            item = QTableWidgetItem(header)
            font = item.font()
            font.setBold(True)
            item.setFont(font)
            self.ui.bookMarc_table.setHorizontalHeaderItem(col_idx, item)

        # Populate table with retrieved data
        for row_idx, book_marc_data in enumerate(data):
            for col_idx, field_name in enumerate(BooksBookMarcData.__annotations__):
                value   = getattr(book_marc_data, field_name)
                item    = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ui.bookMarc_table.setItem(row_idx, col_idx, item)

        # Resize columns to fit content
        self.ui.bookMarc_table.resizeColumnsToContents()
        self.adjustColumnWidths(self.ui.bookMarc_table)

    def showFileBook(self):
        """
        Retrieve and display book data in the book_table.
        """
        print("Show File Book.....")
        data = list(self.db_session.showFileBook())

        self.ui.book_table.setRowCount(len(data))

        # Set the column headers explicitly
        column_headers = ["Warehouse ID", "Book ID", "ISBN", "Quantity", "Stage"]
        self.ui.book_table.setColumnCount(len(column_headers))

        # Set column headers with bold font
        for col_idx, header in enumerate(column_headers):
            item = QTableWidgetItem(header)
            font = item.font()
            font.setBold(True)
            item.setFont(font)
            self.ui.book_table.setHorizontalHeaderItem(col_idx, item)

        # Populate table with retrieved data
        for row_idx, book_data in enumerate(data):
            for col_idx, field_name in enumerate(BooksBookData.__annotations__):
                value   = getattr(book_data, field_name)
                item    = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ui.book_table.setItem(row_idx, col_idx, item)

        # Resize columns to fit content
        self.ui.book_table.resizeColumnsToContents()
        self.adjustColumnWidths(self.ui.book_table)
    
    def adjustColumnWidths(self, table_widget: QTableWidget):
        """
        Adjust column widths of the given table widget to fit content.
        
        Args:
        - table_widget: The QTableWidget instance to adjust.
        """
        # Set the header to resize to fill the available space
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Optionally, resize rows to fit content
        table_widget.resizeRowsToContents()

    def updateBookMarcTable(self):
        """
        Update the bookMarc_table with refreshed data.
        """
        self.ui.bookMarc_table.clearContents()
        self.showFileBookMarc()
    
    def updateBookTable(self):
        """
        Update the book_table with refreshed data.
        """
        self.ui.book_table.clearContents()
        self.showFileBook()

    def pageButtonClicked(self, button):
        """
        Handle the click event of page navigation buttons.
        
        Args:
        - button: The QPushButton instance that was clicked.
        """
        # Reset style and enable the last clicked button (if exists)
        if self.lastClickedPageButton is not None:
            self.lastClickedPageButton.setStyleSheet("""
                QPushButton{
                    border: 2px solid black;
                    color: black;
                }
                QPushButton:hover{
                    border: 2px solid #560bad;
                    color: #560bad;
                }
            """)
            self.lastClickedPageButton.setDisabled(False)
        
        # Set the style and disable the clicked button
        button.setStyleSheet("""
            QPushButton{
                border: 2px solid grey;
                color: grey;
            }
        """)
        button.setDisabled(True)
        
        # Update the last clicked button to the current one
        self.lastClickedPageButton = button
