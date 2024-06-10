from typing import Callable, Optional, Any
from datetime import datetime


from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget, QPushButton, QMessageBox, QComboBox, QLabel, QListWidget, QStackedWidget, QWidget, QLineEdit
from PyQt6 import uic
from PyQt6 import QtCore
from PyQt6.QtCore import QDate

import sys
from pathlib import Path
import os

# Ensure the project root is in the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_session import DBSession
from lms_types import UsersAccountData, UsersHistoryData, UsersGuestData, BooksBookMarcData, BooksBookData, ExecuteResult

class SearchBook_UI:
    # Search page
    input_choose            : QComboBox
    input_find              : QLabel
    find_btn                : QPushButton
    search_table            : QTableWidget
    
    book_id_text_2          : QLabel
    warehouse_id_text_2     : QLabel
    input_title_3           : QLineEdit
    input_author_3          : QLineEdit
    input_isbn_3            : QLineEdit
    input_comp_3            : QLineEdit
    input_year_3            : QLineEdit
    
    def __init__(self, ui, db_session: DBSession):
        self.ui = ui
        self.db_session = db_session
        
    def searchBookInformation(self):
        try:
            # Clear previous search results from the table
            self.ui.search_table.clearContents()
            self.ui.search_table.setRowCount(0)

            column_mapping = {
                "Book ID": "book_id",
                "Warehouse ID": "warehouse_id",
                "Title": "title",
                "Author": "author",
                "Public Year": "public_year",
                "Public Company": "public_comp",
                "ISBN": "isbn",
                "Quantity": "quantity",
                "Stage": "stage"
            }

            filter_criteria = self.ui.input_choose.currentText()
            print(filter_criteria)
            column_name = column_mapping[filter_criteria]
            print(column_name)
            search_query = self.ui.input_find.text().strip()
            print(search_query)
    
    
            search_results = list(self.db_session.searchBook(column_name, search_query))
            
            print(search_results)

            if search_results:
                self.ui.search_table.setRowCount(len(search_results))
                column_count = len(search_results[0])  # Assuming all rows have the same length
                self.ui.search_table.setColumnCount(column_count)
                
                if filter_criteria != "Book ID" and filter_criteria != "Title":
                    header_labels = ['Book ID','Title', filter_criteria]
                else:
                    header_labels = ['Book ID','Title']
                    
                self.ui.search_table.setHorizontalHeaderLabels(header_labels)

                for row_idx, row_data in enumerate(search_results):
                    for col_idx, value in enumerate(row_data):
                        self.ui.search_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

                self.ui.search_table.resizeColumnsToContents()
            else:
                QMessageBox.warning(self.ui, "Search", "No results found.")
        except Exception as e:
            QMessageBox.critical(self.ui, "Error", str(e))

