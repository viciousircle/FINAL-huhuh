from PyQt6.QtWidgets import QPushButton, QMessageBox, QComboBox, QLineEdit, QDateEdit, QSpinBox
from PyQt6.QtCore import QDate, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator, QIntValidator
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
    input_yearAdd      : QLineEdit
    input_quantityAdd  : QSpinBox
    input_stageAdd     : QComboBox
    submit_btn         : QPushButton
    clear_btn          : QPushButton
    enter_btn          : QPushButton
    
    def __init__(self, ui, db_session: DBSession):
        self.ui = ui
        self.db_session = db_session

        self.connectSignals()
        self.initialize()

        # self.checkInputFields()???????

    def initialize(self):
        self.setupFields()
        self.disableInputFields(full=True)

        self.hideDetails()

        self.ui.submit_btn.hide()
        self.ui.clear_btn.hide()

    def hideDetails(self):
        # Hide the labels and input fields for book details
        self.ui.title.hide()
        self.ui.author.hide()
        self.ui.public_comp.hide()
        self.ui.public_year.hide()
        self.ui.quantity.hide()
        self.ui.stage.hide()

        self.ui.input_titleAdd.hide()
        self.ui.input_authorAdd.hide()
        self.ui.input_compAdd.hide()
        self.ui.input_yearAdd.hide()
        self.ui.input_quantityAdd.hide()
        self.ui.input_stageAdd.hide()


    def showDetails(self):
        # Show the labels and input fields for book details
        self.ui.title.show()
        self.ui.author.show()
        self.ui.public_comp.show()
        self.ui.public_year.show()
        self.ui.quantity.show()
        self.ui.stage.show()

        self.ui.input_titleAdd.show()
        self.ui.input_authorAdd.show()
        self.ui.input_compAdd.show()
        self.ui.input_yearAdd.show()
        self.ui.input_quantityAdd.show()
        self.ui.input_stageAdd.show()


    def connectSignals(self):
        self.ui.enter_btn.clicked.connect(self.enterButtonClicked)
        self.ui.submit_btn.clicked.connect(self.submitButtonClicked)
        self.ui.clear_btn.clicked.connect(self.clearButtonClicked)

        # Connect signals to check method
        self.ui.input_isbnAdd.textChanged.connect(self.checkInputFields)
        self.ui.input_titleAdd.textChanged.connect(self.checkInputFields)
        self.ui.input_authorAdd.textChanged.connect(self.checkInputFields)
        self.ui.input_compAdd.textChanged.connect(self.checkInputFields)
        self.ui.input_yearAdd.textChanged.connect(self.checkInputFields)
        self.ui.input_quantityAdd.valueChanged.connect(self.checkInputFields)
        self.ui.input_stageAdd.currentIndexChanged.connect(self.checkInputFields)

        # Connect signals for validation
        self.ui.input_isbnAdd.textChanged.connect(self.validateISBN)
        self.ui.input_quantityAdd.valueChanged.connect(self.validateQuantity)

    def setupFields(self):
            
        # Set up the input fields
        self.detail_fields = [
            self.ui.input_titleAdd,
            self.ui.input_authorAdd,
            self.ui.input_isbnAdd,
            self.ui.input_compAdd,
            self.ui.input_yearAdd,
            self.ui.input_quantityAdd,
            self.ui.input_stageAdd
        ]

        self.ui.input_isbnAdd.setMaxLength(13)
        isbn_validator = QRegularExpressionValidator(QRegularExpression(r'^\d{1,13}$'), self.ui.input_isbnAdd)
        self.ui.input_isbnAdd.setValidator(isbn_validator)
        self.ui.input_titleAdd.setMaxLength(100)
        self.ui.input_authorAdd.setMaxLength(100)
        self.ui.input_compAdd.setMaxLength(100)
        self.ui.input_yearAdd.setValidator(QIntValidator(1000, 9999))
        self.ui.input_quantityAdd.setMaximum(999999)  

        self.input_fields = {
            "input_titleAdd": self.ui.input_titleAdd,
            "input_authorAdd": self.ui.input_authorAdd,
            "input_isbnAdd": self.ui.input_isbnAdd,
            "input_compAdd": self.ui.input_compAdd,
            "input_yearAdd": self.ui.input_yearAdd,
            "input_quantityAdd": self.ui.input_quantityAdd,
            "input_stageAdd": self.ui.input_stageAdd
        }
        
    def showMessageBox(self, title: str, message: str, icon: QMessageBox.Icon):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec()

    def enterButtonClicked(self):
        try:

            isbn = self.ui.input_isbnAdd.text().strip()
            if not isbn:
                self.showMessageBox("Error", "ISBN is required", QMessageBox.Icon.Critical)
                return
            if len(isbn) != 13:
                self.showMessageBox("Error", "ISBN must be 13 characters long", QMessageBox.Icon.Critical)
                return
                

            existing_book, error = self.db_session.getBookByISBN(isbn)
            if existing_book:
                self.ui.messageAdd.setText("Book already exists in the system. Add with new quantity and stage for new warehouse id.")
                self.populateInputFields(existing_book)
                self.disableInputFields(full=False)
            else:
                self.ui.messageAdd.setText("This is a new ISBN. Please enter book details to add a new book.")
                self.enableInputFields()  

            self.showDetails()
            self.ui.submit_btn.show()
            self.ui.clear_btn.show()
            self.ui.enter_btn.hide()
            self.ui.input_isbnAdd.setEnabled(False)   
                
        except Exception as e:
            self.showMessageBox("Error", str(e), QMessageBox.Icon.Critical)
            print(str(e))

    def submitButtonClicked(self):
        # Check if all fields are empty before proceeding
        if self.checkIfAllFieldsEmpty():
            self.showMessageBox("Warning", "All input fields are empty.", QMessageBox.Icon.Warning)
            return

        try:
            
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
            if stage == "":
                QMessageBox.critical(self.ui, "Error", "Stage must be selected")
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
                
                admin_id = self.ui.admin_id.text()  # Replace with the actual admin ID or fetch dynamically
                result = self.db_session.addBook(admin_id,book_id, None, bookData)
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

    def disableInputFields(self, full=True):
        # Disable all input fields and apply style
        self.setDisabledStyle(self.ui.input_titleAdd)
        self.setDisabledStyle(self.ui.input_authorAdd)
        self.setDisabledStyle(self.ui.input_compAdd)
        self.setDisabledStyle(self.ui.input_yearAdd)

        if full:
            self.setDisabledStyle(self.ui.input_quantityAdd)
            self.setDisabledStyle(self.ui.input_stageAdd)
        else:
            self.setEnabledStyle(self.ui.input_quantityAdd)
            self.setEnabledStyle(self.ui.input_stageAdd)

    def enableInputFields(self):
        self.setEnabledStyle(self.ui.input_titleAdd)
        self.setEnabledStyle(self.ui.input_authorAdd)
        self.setEnabledStyle(self.ui.input_compAdd)
        self.setEnabledStyle(self.ui.input_yearAdd)
        self.setEnabledStyle(self.ui.input_quantityAdd)
        self.setEnabledStyle(self.ui.input_stageAdd)

    



    def clearButtonClicked(self):
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
        self.ui.input_titleAdd.setText(book.title)
        self.ui.input_authorAdd.setText(book.author)
        self.ui.input_compAdd.setText(book.public_comp)
        self.ui.input_yearAdd.setText(str(book.public_year))
        self.ui.input_quantityAdd.setValue(0)
        self.ui.input_stageAdd.setCurrentIndex(-1)


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
            self.ui.input_yearAdd.text().strip() and
            self.ui.input_quantityAdd.value() == 0 and
            self.ui.input_stageAdd.currentIndex() == -1
        )
        
        # Enable or disable the reset and submit buttons based on the check
        self.ui.clear_btn.setEnabled(not all_empty)
        self.ui.submit_btn.setEnabled(not all_empty)
    
    def checkIfAllFieldsEmpty(self):
        return (
            not self.ui.input_titleAdd.text().strip() and
            not self.ui.input_authorAdd.text().strip() and
            not self.ui.input_compAdd.text().strip() and
            not self.ui.input_yearAdd.text().strip() and
            self.ui.input_quantityAdd.value() == 0 and
            self.ui.input_stageAdd.currentIndex() == -1
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


