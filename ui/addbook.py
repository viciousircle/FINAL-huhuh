
# ------ IMPORTS ------------------------------------------
from PyQt6.QtWidgets import QPushButton, QMessageBox, QComboBox, QLineEdit, QDateEdit, QSpinBox
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
    input_quantityAdd  : QSpinBox
    input_stageAdd     : QComboBox
    
    submit_btn      : QPushButton
    clear_btn       : QPushButton
    enter_btn       : QPushButton
    
    
    def __init__(self, ui, db_session: DBSession):
        self.ui         = ui
        self.db_session = db_session
        
        # from ui import ShowFile_UI
        # self.showfile   = ShowFile_UI(self.ui, self.db_session)
        
        self.ui.submit_btn.clicked.connect(self.addBookInformation)
        self.ui.enter_btn.clicked.connect(self.getBookInformation)
        
        self.ui.clear_btn.clicked.connect(self.clearInputFields)
        
        self.disableInputFields()
        
        
    def getBookInformation(self):
        try:
            isbn = self.ui.input_isbnAdd.text().strip()

            if not isbn:
                QMessageBox.critical(self.ui, "Error", "ISBN is required")
                return

            existing_book, error = self.db_session.getBookByISBN(isbn)
            print(existing_book)
            print(error)

            if existing_book:
                self.populateInputFields(existing_book)
                self.disableInputFields()

            else:
                self.clearInputFields()  # Clear other input fields if book not found
                self.enableInputFields()  # Enable other input fields if book not found

        except Exception as e:
            QMessageBox.critical(self.ui, "Error", str(e))
            print(str(e))

    def addBookInformation(self):
        try:
            isbn = self.ui.input_isbnAdd.text().strip()
            quantity = self.ui.input_quantityAdd.value() 
            stage = self.ui.input_stageAdd.currentText().strip()

            if not isbn:
                QMessageBox.critical(self.ui, "Error", "ISBN is required")
                return

            if quantity <= 0:
                QMessageBox.critical(self.ui, "Error", "Quantity must be greater than 0")
                return

            existing_book, error = self.db_session.getBookByISBN(isbn)

            if existing_book:
                # Retrieve the book_id from existing_book (if it's correct)
                book_id = existing_book.book_id
                bookData = BooksBookData(
                    quantity=quantity,
                    stage=stage,
                    isbn=isbn
                )
                result = self.db_session.addBook(book_id, None, bookData)
                print(result)
            else:
                bookMarcData = BooksBookMarcData(
                    title=self.ui.input_titleAdd.text().strip(),
                    author=self.ui.input_authorAdd.text().strip(),
                    public_year=self.ui.input_yearAdd.date().year(),
                    public_comp=self.ui.input_compAdd.text().strip(),
                    isbn=isbn
                )
                book_id = self.db_session.insertBookMarc(bookMarcData)
                bookData = BooksBookData(
                    quantity=quantity,
                    stage=stage,
                    isbn=isbn
                )
                result = self.db_session.addBook(book_id, bookMarcData, bookData)
                print(result)
            
            if result[0]:
                QMessageBox.information(self.ui, "Success", "Book added successfully")
                from ui import ShowFile_UI
                self.showfile = ShowFile_UI(self.ui, self.db_session)
                self.showfile.updateBookMarcTable()
                self.showfile.updateBookTable()
                self.clearInputFields()
            else:
                QMessageBox.critical(self.ui, "Error", result[1])
                print(result[1])

        except AttributeError:
            # Handle the case where existing_book is None
            QMessageBox.critical(self.ui, "Error", "Book not found")
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
        # Create a confirmation message box
        reply = QMessageBox.question(
            self.ui, 'Message',
            "Are you sure you want to clear all fields?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        # Check the user's response
        if reply == QMessageBox.StandardButton.Yes:
            # Clear input fields
            self.ui.input_isbnAdd.clear()
            self.ui.input_titleAdd.clear()
            self.ui.input_authorAdd.clear()
            self.ui.input_compAdd.clear()
            self.ui.input_yearAdd.setDate(QDate(2000, 1, 1))
            self.ui.input_quantityAdd.setValue(0)
            self.ui.input_stageAdd.setCurrentIndex(0)
            
            # Disable input fields
            self.disableInputFields()
        else:
            # If the user chooses not to clear the fields, do nothing
            return

        
    def populateInputFields(self, book):
        # Populate input fields with book information
        self.ui.input_titleAdd.setText(book.title)
        self.ui.input_authorAdd.setText(book.author)
        self.ui.input_compAdd.setText(book.public_comp)
        self.ui.input_yearAdd.setDate(QDate(book.public_year, 1, 1))    
        
