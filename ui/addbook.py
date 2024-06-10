
# ------ IMPORTS ------------------------------------------
from PyQt6.QtWidgets import QPushButton, QMessageBox, QComboBox, QLineEdit
from PyQt6.QtCore import QDate

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_session import DBSession
from lms_types import BooksBookMarcData, BooksBookData
# ---------------------------------------------------------

# ------ ADDBOOK_UI CLASS ---------------------------------
class AddBook_UI:
    # List of objects in .ui file related to this module
    input_title     : QLineEdit
    input_author    : QLineEdit
    input_isbn      : QLineEdit
    input_comp      : QLineEdit
    input_year      : QDate
    input_quantity  : QLineEdit
    input_stage     : QComboBox
    
    submit_btn      : QPushButton
    
    
    def __init__(self, ui, db_session: DBSession):
        self.ui         = ui
        self.db_session = db_session
        
        from ui import ShowFile_UI
        self.showfile   = ShowFile_UI(self.ui, self.db_session)
    
    def addBookInformation(self):
        try:
            title       = self.ui.input_title.text().strip()
            author      = self.ui.input_author.text().strip()
            public_year = self.ui.input_year.date().year()
            public_comp = self.ui.input_comp.text().strip()
            isbn        = self.ui.input_isbn.text().strip()
            quantity    = self.ui.input_quantity.value()
            stage       = self.ui.input_stage.currentText().strip()

            print(title, author, public_year, public_comp, isbn, quantity, stage)

            if not title or not author or not public_comp or not isbn:
                QMessageBox.warning(self.ui, "Warning", "Please fill in all fields")
                return

            if quantity <= 0:
                QMessageBox.warning(self.ui, "Warning", "Please enter a valid quantity")
                return

            bookMarcData = BooksBookMarcData(
                title           =   title,
                author          =   author,
                public_year     =   public_year,
                public_comp     =   public_comp,
                isbn            =   isbn
            )

            bookData = BooksBookData(
                quantity        =   quantity,
                stage           =   stage
            )

            result = self.db_session.addBook(bookMarcData, bookData)
            
            print(result)

            if result[0]:
                QMessageBox.information(self.ui, "Success", "Book information added successfully.")
                self.showfile.updateBookMarcTable()
                self.showfile.updateBookTable()
            else:
                QMessageBox.critical(self.ui, "Database Error", f"An error occurred: {result[1]}")
        except Exception as e:
            print("Error:", e)

# ---------------------------------------------------------
  