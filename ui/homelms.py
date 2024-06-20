from typing import Callable, Optional, Any
from datetime import datetime


from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget, QPushButton, QMessageBox, QComboBox, QLabel, QListWidget, QStackedWidget, QWidget, QLineEdit, QHeaderView
from PyQt6 import uic
from PyQt6 import QtCore
from PyQt6.QtCore import QDate, Qt

import sys
from pathlib import Path
import os

# Ensure the project root is in the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.db_session import DBSession
from db.lms_types import UsersAccountData, UsersHistoryData, UsersGuestData, BooksBookMarcData, BooksBookData, ExecuteResult

class Home_UI:

    number_books: QLabel
    quantity_books: QLabel

    def __init__(self, ui, db_session: DBSession):
        self.ui         = ui
        self.db_session = db_session

        self.showNumberOfBooks()
        self.showQuantityOfBooks()
        # self.showNumberOfGuestsInMonth()
        self.showNewAddedBooks()

    def showNumberOfBooks(self):
        number_books = self.db_session.countNumberOfBooks()
        self.ui.number_books.setText(str(number_books))

    def showQuantityOfBooks(self):
        quantity_books = self.db_session.countQuantityOfBooks()
        self.ui.quantity_books.setText(str(quantity_books))


    def showNewAddedBooks(self):
        data = list(self.db_session.get10NewAddedBooks())
        self.ui.new_books_table.setRowCount(len(data))

        column_headers = ["Book ID", "Title", "Author", "Public Year", "Public Company", "ISBN"]

        self.ui.new_books_table.setColumnCount(len(column_headers))

        for col_idx, header in enumerate(column_headers):
            item = QTableWidgetItem(header)
            font = item.font()
            font.setBold(True)
            item.setFont(font)
            self.ui.new_books_table.setHorizontalHeaderItem(col_idx, item)

        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(BooksBookMarcData.__annotations__):
                value = getattr(row_data, cell_data)
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ui.new_books_table.setItem(row_idx, col_idx, item)
        
        self.ui.new_books_table.resizeColumnsToContents()
        self.adjustColumnWidths(self.ui.new_books_table)



    def adjustColumnWidths(self, table_widget: QTableWidget):
        # Set the header to resize to fill the available space
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Optionally, resize rows to fit content
        table_widget.resizeRowsToContents()

