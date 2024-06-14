from PyQt6.QtWidgets import QPushButton, QMessageBox, QComboBox, QLineEdit, QDateEdit, QSpinBox
from PyQt6.QtCore import QDate
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_session import DBSession
from lms_types import BooksBookMarcData, BooksBookData

class AddBook_UI:
    # List of objects in .ui file related to this module
    input_isbnAdd      : QLineEdit
    messageAdd         : QLineEdit
    input_titleAdd     : QLineEdit
    input_authorAdd    : QLineEdit
    input_compAdd      : QLineEdit
    input_yearAdd      : QDateEdit
    input_quantityAdd  : QSpinBox
    input_stageAdd     : QComboBox
    submit_btn         : QPushButton
    clear_btn          : QPushButton
    enter_btn          : QPushButton
    
    def __init__(self, ui, db_session: DBSession):
        self.ui = ui
        self.db_session = db_session
        
        self.ui.submit_btn.clicked.connect(self.addBookInformation)
        self.ui.enter_btn.clicked.connect(self.getBookInformation)
        self.ui.clear_btn.clicked.connect(self.clearInputFields)
        
        self.disableInputFields()

        # Connect signals to check method
        self.ui.input_isbnAdd.textChanged.connect(self.checkInputFields)
        self.ui.input_titleAdd.textChanged.connect(self.checkInputFields)
        self.ui.input_authorAdd.textChanged.connect(self.checkInputFields)
        self.ui.input_compAdd.textChanged.connect(self.checkInputFields)
        self.ui.input_yearAdd.dateChanged.connect(self.checkInputFields)
        self.ui.input_quantityAdd.valueChanged.connect(self.checkInputFields)
        self.ui.input_stageAdd.currentIndexChanged.connect(self.checkInputFields)
        
        # Connect signals for validation
        self.ui.input_isbnAdd.textChanged.connect(self.validateISBN)
        self.ui.input_quantityAdd.valueChanged.connect(self.validateQuantity)
        
        self.checkInputFields()

        # Set maximum value for quantity
        self.ui.input_quantityAdd.setMaximum(999999999)

    def getBookInformation(self):
        try:
            isbn = self.ui.input_isbnAdd.text().strip()
            if not isbn:
                QMessageBox.critical(self.ui, "Error", "ISBN is required")
                return
            if len(isbn) != 13:
                QMessageBox.critical(self.ui, "Error", "ISBN must be 13 characters long")
                return

            existing_book, error = self.db_session.getBookByISBN(isbn)
            if existing_book:
                # Book exists in the database, populate fields
                self.populateInputFields(existing_book)
                self.disableBookDetailFields()
                self.setDisabledStyle(self.ui.input_isbnAdd)  # Disable input_isbnAdd
                self.setDisabledStyle(self.ui.enter_btn)      # Disable enter_btn
                self.ui.messageAdd.setText("Existing book found!")
            else:
                # Book does not exist, clear input fields
                self.clearInputFields()
                self.enableInputFields()  # Enable all input fields
                self.ui.messageAdd.setText("Book not found. Please enter book details to add a new book.")
                
            # Disable submit and clear buttons
            self.ui.submit_btn.setEnabled(False)
            # self.ui.clear_btn.setEnabled(False)

        except Exception as e:
            QMessageBox.critical(self.ui, "Error", str(e))
            print(str(e))
            print(3)


    def addBookInformation(self):
        # Check if all fields are empty before proceeding
        if self.checkIfAllFieldsEmpty():
            QMessageBox.information(self.ui, "Warning", "Please fill in the required fields before submitting.")
            return

        try:
            print("Adding book information...")
            
            isbn = self.ui.input_isbnAdd.text().strip()
            quantity = self.ui.input_quantityAdd.value()
            stage = self.ui.input_stageAdd.currentText().strip()

            if not isbn:
                QMessageBox.critical(self.ui, "Error", "ISBN is required")
                return
            if len(isbn) != 13:
                QMessageBox.critical(self.ui, "Error", "ISBN must be 13 characters long")
                return

            if quantity <= 0:
                QMessageBox.critical(self.ui, "Error", "Quantity must be greater than 0")
                return

            # Show confirmation message
            reply = QMessageBox.question(
                self.ui, 'Confirmation',
                "Are you sure you want to submit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.No:
                return  # User clicked No, abort operation
            
            existing_book, error = self.db_session.getBookByISBN(isbn)
            
            if existing_book:
                # Book already exists in the database, update its operational data
                book_id = existing_book.book_id
                bookData = BooksBookData(
                    quantity=quantity,
                    stage=stage,
                    isbn=isbn
                )
                result = self.db_session.addBook(book_id, None, bookData)
            else:
                # Book does not exist, insert new metadata and operational data
                bookMarcData = BooksBookMarcData(
                    title=self.ui.input_titleAdd.text().strip(),
                    author=self.ui.input_authorAdd.text().strip(),
                    public_year=self.ui.input_yearAdd.date().year(),
                    public_comp=self.ui.input_compAdd.text().strip(),
                    isbn=isbn
                )
                bookData = BooksBookData(
                    quantity=quantity,
                    stage=stage,
                    isbn=isbn
                )
                book_id = self.db_session.insertBookMarc(bookMarcData)
                result = self.db_session.addBook(book_id, bookMarcData, bookData)
                
                # Log the addition in history
                admin_id = 1  # Replace with the actual admin ID or fetch dynamically
                if result[0]:
                    self.db_session.logHistory(admin_id, book_id, isbn, None, datetime.now())
            
            if result[0]:
                # Show success message
                QMessageBox.information(self.ui, "Success", "Book added successfully")
                self.clearFieldsAndDisable()
            else:
                QMessageBox.critical(self.ui, "Error", result[1])
                print(result[1])

        except AttributeError:
            QMessageBox.critical(self.ui, "Error", "Book not found")
        except Exception as e:
            QMessageBox.critical(self.ui, "Error", str(e))
            print(str(e))

    
    def clearFieldsAndDisable(self):
        # Clear all input fields and disable relevant buttons
        self.ui.input_isbnAdd.clear()
        self.ui.input_titleAdd.clear()
        self.ui.input_authorAdd.clear()
        self.ui.input_compAdd.clear()
        self.ui.input_yearAdd.setDate(QDate(2000, 1, 1))
        self.ui.input_quantityAdd.setValue(0)
        self.ui.input_stageAdd.setCurrentIndex(0)
        
        self.disableInputFields()
        self.ui.input_isbnAdd.setEnabled(True)   # Enable input_isbnAdd
        self.ui.enter_btn.setEnabled(True)       # Enable enter_btn

    def disableInputFields(self):
        # Disable all input fields and apply style
        self.setDisabledStyle(self.ui.input_titleAdd)
        self.setDisabledStyle(self.ui.input_authorAdd)
        self.setDisabledStyle(self.ui.input_compAdd)
        self.setDisabledStyle(self.ui.input_yearAdd)
        self.setDisabledStyle(self.ui.input_quantityAdd)
        self.setDisabledStyle(self.ui.input_stageAdd)
        self.setDisabledStyle(self.ui.submit_btn)
        self.setDisabledStyle(self.ui.clear_btn)

    def enableInputFields(self):
        # Enable all input fields and reset style
        self.setEnabledStyle(self.ui.input_titleAdd)
        self.setEnabledStyle(self.ui.input_authorAdd)
        self.setEnabledStyle(self.ui.input_compAdd)
        self.setEnabledStyle(self.ui.input_yearAdd)
        self.setEnabledStyle(self.ui.input_quantityAdd)
        self.setEnabledStyle(self.ui.input_stageAdd)
        self.setEnabledStyle(self.ui.submit_btn)
        self.setEnabledStyle(self.ui.clear_btn)

    def disableBookDetailFields(self):
        # Disable specific fields (title, author, and publication company) and apply style
        self.setDisabledStyle(self.ui.input_titleAdd)
        self.setDisabledStyle(self.ui.input_authorAdd)
        self.setDisabledStyle(self.ui.input_compAdd)
        self.setDisabledStyle(self.ui.input_yearAdd)
        self.setEnabledStyle(self.ui.input_quantityAdd)
        self.setEnabledStyle(self.ui.input_stageAdd)
        self.setEnabledStyle(self.ui.submit_btn)
        self.setEnabledStyle(self.ui.clear_btn)

    def clearInputFields(self):
        # Check if all fields are already empty before proceeding
        if self.checkIfAllFieldsEmpty():
            QMessageBox.information(self.ui, "Warning", "All input fields are empty.")
            return

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
            
            # Clear messageAdd field
            self.ui.messageAdd.clear()
            
            # Disable input fields and enter button
            self.disableInputFields()
            self.ui.input_isbnAdd.setEnabled(True)   # Enable input_isbnAdd
            self.ui.enter_btn.setEnabled(True)       # Enable enter_btn
        else:
            # If the user chooses not to clear the fields, do nothing
            return


    def populateInputFields(self, book):
        # Populate input fields with book information
        self.ui.input_titleAdd.setText(book.title)
        self.ui.input_authorAdd.setText(book.author)
        self.ui.input_compAdd.setText(book.public_comp)
        self.ui.input_yearAdd.setDate(QDate(book.public_year, 1, 1))
        
        # Check if the book object has 'quantity' and 'stage' attributes (BooksBookData)
        if isinstance(book, BooksBookData):
            self.ui.input_quantityAdd.setValue(book.quantity)
            self.ui.input_stageAdd.setCurrentText(book.stage)
        else:
            # Default values if it's a BooksBookMarcData object
            self.ui.input_quantityAdd.setValue(0)
            self.ui.input_stageAdd.setCurrentIndex(0)


    def setDisabledStyle(self, widget):
        widget.setStyleSheet("border: 2px solid grey; color: grey;")
        widget.setEnabled(False)

    def setEnabledStyle(self, widget):
        widget.setStyleSheet("border: 2px solid black; color: black;")
        widget.setEnabled(True)

    def checkInputFields(self):
        # Check if all relevant input fields are empty
        all_empty = (
            not self.ui.input_titleAdd.text().strip() and
            not self.ui.input_authorAdd.text().strip() and
            not self.ui.input_compAdd.text().strip() and
            self.ui.input_yearAdd.date() == QDate(2000, 1, 1) and
            self.ui.input_quantityAdd.value() == 0 and
            self.ui.input_stageAdd.currentIndex() == 0
        )
        
        # Enable or disable the reset and submit buttons based on the check
        self.ui.clear_btn.setEnabled(not all_empty)
        self.ui.submit_btn.setEnabled(not all_empty)
    
    def checkIfAllFieldsEmpty(self):
        return (
            not self.ui.input_titleAdd.text().strip() and
            not self.ui.input_authorAdd.text().strip() and
            not self.ui.input_compAdd.text().strip() and
            self.ui.input_yearAdd.date() == QDate(2000, 1, 1) and
            self.ui.input_quantityAdd.value() == 0 and
            self.ui.input_stageAdd.currentIndex() == 0
        )
    
    def validateISBN(self, text):
        if len(text.strip()) != 13:
            self.ui.messageAdd.setText("<font color='red'>ISBN must be 13 characters long</font>")
        else:
            self.ui.messageAdd.clear()
    
    def validateQuantity(self, value):
        if value <= 0:
            self.ui.messageAdd.setText("<font color='red'>Quantity must be greater than 0</font>")
        else:
            self.ui.messageAdd.clear()


