
# ------ IMPORTS ------------------------------------------
from PyQt6.QtWidgets import QPushButton, QMessageBox, QComboBox, QLineEdit, QDateEdit
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
    input_isbnAdd      : QLineEdit
    
    input_titleAdd     : QLineEdit
    input_authorAdd    : QLineEdit
    input_compAdd      : QLineEdit
    input_yearAdd      : QDateEdit
    input_quantityAdd  : QLineEdit
    input_stageAdd     : QComboBox
    
    submit_btn      : QPushButton
    reset_btn       : QPushButton
    enter_btn       : QPushButton
    
    
    def __init__(self, ui, db_session: DBSession):
        self.ui         = ui
        self.db_session = db_session
        
        # from ui import ShowFile_UI
        # self.showfile   = ShowFile_UI(self.ui, self.db_session)
        
        self.ui.submit_btn.clicked.connect(self.addBookInformation)
        self.ui.enter_btn.clicked.connect(self.getBookInformation)
        
        
    def getBookInformation(self):
        try:
            isbn = self.ui.input_isbnAdd.text().strip()

            if not isbn:
                QMessageBox.critical(self.ui, "Error", "ISBN is required")
                return

            existing_book, error = self.db_session.getBookByISBN(isbn)

            if existing_book:
                title = existing_book.title
                author = existing_book.author
                public_year = existing_book.public_year
                public_comp = existing_book.public_comp

                self.ui.input_titleAdd.setText(title)
                self.ui.input_authorAdd.setText(author)
                self.ui.input_compAdd.setText(public_comp)
                self.ui.input_yearAdd.setDate(QDate(public_year, 1, 1))

                self.disableInputFields()  # Disable input fields after fetching book information

            else:
                self.clearInputFields()  # Clear other input fields if book not found
                self.enableInputFields()  # Enable other input fields if book not found

        except Exception as e:
            QMessageBox.critical(self.ui, "Error", str(e))
            print(str(e))


    
    
    def addBookInformation(self):
        try:
            isbn = self.ui.input_isbnAdd.text().strip()
            quantity = int(self.ui.input_quantityAdd.text().strip())
            stage = self.ui.input_stageAdd.currentText().strip()

            if not isbn:
                QMessageBox.critical(self.ui, "Error", "ISBN is required")
                return

            if quantity <= 0:
                QMessageBox.critical(self.ui, "Error", "Quantity must be greater than 0")
                return

            bookData = BooksBookData(
                quantity=quantity,
                stage=stage,
                isbn=isbn
            )

            existing_book, error = self.db_session.getBookByISBN(isbn)

            if not existing_book:
                bookMarcData = BooksBookMarcData(
                    title=self.ui.input_titleAdd.text().strip(),
                    author=self.ui.input_authorAdd.text().strip(),
                    public_year=self.ui.input_yearAdd.date().year(),
                    public_comp=self.ui.input_compAdd.text().strip(),
                    isbn=isbn
                )

                result = self.db_session.addBook(bookMarcData, bookData)

            else:
                result = self.db_session.addBook(None, bookData)

            if result[0]:
                QMessageBox.information(self.ui, "Success", "Book added successfully")
                from ui import ShowFile_UI
                self.showfile = ShowFile_UI(self.ui, self.db_session)
                self.showfile.updateBookMarcTable()
                self.showfile.updateBookTable()

                self.clearInputFields()

            else:
                QMessageBox.critical(self.ui, "Error", result[1])

        except Exception as e:
            QMessageBox.critical(self.ui, "Error", str(e))
            print(str(e))
            
    def disableInputFields(self):
        # Disable input fields
        self.ui.input_titleAdd.setEnabled(False)
        self.ui.input_authorAdd.setEnabled(False)
        self.ui.input_compAdd.setEnabled(False)
        self.ui.input_yearAdd.setEnabled(False)

    def enableInputFields(self):
        # Enable input fields
        self.ui.input_titleAdd.setEnabled(True)
        self.ui.input_authorAdd.setEnabled(True)
        self.ui.input_compAdd.setEnabled(True)
        self.ui.input_yearAdd.setEnabled(True)
        
    def clearInputFields(self):
        # Clear and disable input fields
        self.ui.input_titleAdd.clear()
        self.ui.input_authorAdd.clear()
        self.ui.input_compAdd.clear()
        self.ui.input_yearAdd.clear()
        self.ui.input_quantityAdd.clear()
        self.ui.input_stageAdd.setCurrentIndex(0)
        # self.ui.input_isbnAdd.clear()
        self.disableInputFields()