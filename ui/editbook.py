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

class EditBook_UI:
    
    input_find_2        : QLineEdit
    find_btn_2          : QPushButton
    
    book_id_text        : QLabel
    warehouse_id_text   : QLabel
    
    input_title_2       : QLineEdit
    input_author_2      : QLineEdit
    input_isbn_2        : QLineEdit
    input_comp_2        : QLineEdit
    input_year_2        : QDate
    input_quantity_2    : QLineEdit
    input_stage_2       : QComboBox
    
    
    def __init__(self, ui, db_session: DBSession):
        self.ui = ui
        self.db_session = db_session
    
    def editBookInformation(self):
        print("Edit Book Information")
        try:
            book_id = int(self.ui.input_find_2.text().strip())
            print("Book ID:", book_id)
            
            get_book = self.db_session.getBookById(book_id)
            print(get_book)
            
            if get_book:
                bookMarcData, bookData = get_book
                self.ui.book_id_text.setText(str(bookMarcData.book_id))
                self.ui.input_title_2.setText(bookMarcData.title if bookMarcData.title else "")
                self.ui.input_author_2.setText(bookMarcData.author if bookMarcData.author else "")
                self.ui.input_isbn_2.setText(bookMarcData.isbn if bookMarcData.isbn else "")
                self.ui.input_comp_2.setText(bookMarcData.public_comp if bookMarcData.public_comp else "")
                self.ui.input_year_2.setDate(QDate(bookMarcData.public_year, 1, 1) if bookMarcData.public_year else QDate(2000, 1, 1))
                
                self.ui.warehouse_id_text.setText(str(bookData.warehouse_id) if bookData.warehouse_id else "")
                self.ui.input_quantity_2.setValue(bookData.quantity if bookData.quantity else 0)
                
                stage_options = ["Available", "Unavailable"]

                # Set the current index based on bookData.stage
                if bookData.stage in stage_options:
                    self.ui.input_stage_2.setCurrentIndex(stage_options.index(bookData.stage))
                else:
                    self.ui.input_stage_2.setCurrentIndex(0)
                    
                
            else:
                QMessageBox.warning(self.ui, "Search", "No results found.")
                
        except ValueError:
            QMessageBox.warning(self.ui, "Search", "Please enter a valid Book ID")
        
        except Exception as e:
            print("Error:", e)
    
    def saveBookInformation(self):
        try:
            book_id = int(self.ui.input_find_2.text().strip())
            
            old_book_data = self.db_session.getBookById(book_id)
            
            if old_book_data:
                old_bookMarcData, old_bookData = old_book_data
            
                new_bookMarcData = BooksBookMarcData(
                    title = self.ui.input_title_2.text().strip(),
                    author= self.ui.input_author_2.text().strip(),
                    public_year= self.ui.input_year_2.date().year(),
                    public_comp= self.ui.input_comp_2.text().strip(),
                    isbn= self.ui.input_isbn_2.text().strip(),
                    book_id= book_id
                )
                
                new_bookData = BooksBookData(
                    quantity= self.ui.input_quantity_2.value(),
                    stage= self.ui.input_stage_2.currentText().strip(),
                    book_id= book_id,
                    warehouse_id= old_book_data[1].warehouse_id
                )

                result, error = self.db_session.updateBook(new_bookMarcData, new_bookData, old_bookMarcData, old_bookData)
                
                if result:
                    QMessageBox.information(self.ui, "Success", "Book information updated successfully.")
                    self.updateBookMarcTable()
                    self.updateBookTable()
                else:
                    QMessageBox.critical(self.ui, "Database Error", f"An error occurred: {error}")
            else:
                QMessageBox.warning(self.ui, "Search", "No results found.")

        except ValueError:
            QMessageBox.warning(self.ui, "Error","Invalid input in one or more fields")
        
        except Exception as e:
            print("Error:", e)
