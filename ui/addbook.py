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
    messageAdd         : QLineEdit
    input_isbnAdd      : QLineEdit
    input_titleAdd     : QLineEdit
    input_authorAdd    : QLineEdit
    input_compAdd      : QLineEdit
    input_yearAdd      : QLineEdit
    input_quantityAdd  : QSpinBox
    input_stageAdd     : QComboBox
    submit_btn         : QPushButton
    cancel_btnAdd          : QPushButton
    enter_btn          : QPushButton
    
    def __init__(self, ui, db_session: DBSession):
        self.ui = ui
        self.db_session = db_session

        self.connectSignals()
        self.setupFields()
        self.initialize()


        
    
    def connectSignals(self):
        
        self.textChanged()
        self.ui.enter_btn.clicked.connect(self.enterButtonClicked)
        self.ui.submit_btn.clicked.connect(self.submitButtonClicked)
    
    def initialize(self):
        # self.isbn_details_entered = False
        self.hideSubmitButtons(True)
        self.hideInputFields()

    def hideSubmitButtons(self, all: bool):
        self.ui.submit_btn.hide()
        self.ui.cancel_btnAdd.hide()
        if all:
            self.ui.enter_btn.hide()
        else:
            self.ui.enter_btn.show()

    def hideInputFields(self):
        
        self.ui.input_titleAdd.hide()
        self.ui.input_authorAdd.hide()
        self.ui.input_compAdd.hide()
        self.ui.input_yearAdd.hide()
        self.ui.input_quantityAdd.hide()
        self.ui.input_stageAdd.hide()

        self.ui.title.hide()
        self.ui.author.hide()
        self.ui.public_comp.hide()
        self.ui.public_year.hide()
        self.ui.quantity.hide()
        self.ui.stage.hide()

    def setupFields(self):
            
        # Set up the input fields
        self.detail_fields = [
            self.ui.input_isbnAdd,
            self.ui.input_titleAdd,
            self.ui.input_authorAdd,
            self.ui.input_compAdd,
            self.ui.input_yearAdd
        ]

        self.input_fields = {
            "input_titleAdd": self.ui.input_titleAdd,
            "input_authorAdd": self.ui.input_authorAdd,
            "input_isbnAdd": self.ui.input_isbnAdd,
            "input_compAdd": self.ui.input_compAdd,
            "input_yearAdd": self.ui.input_yearAdd,
            "input_quantityAdd": self.ui.input_quantityAdd,
            "input_stageAdd": self.ui.input_stageAdd
        }

        self.ui.input_isbnAdd.setMaxLength(13)
        isbn_validator = QRegularExpressionValidator(QRegularExpression(r'^\d{1,13}$'), self.ui.input_isbnAdd)
        self.ui.input_isbnAdd.setValidator(isbn_validator)

        self.ui.input_titleAdd.setMaxLength(100)
        self.ui.input_authorAdd.setMaxLength(100)
        self.ui.input_compAdd.setMaxLength(100)
        self.ui.input_yearAdd.setValidator(QIntValidator(1000, 9999))
        self.ui.input_quantityAdd.setMaximum(999999)  

    def showNotification(self, message: str):
        self.ui.messageAdd.setText(message)
        self.ui.messageAdd.show()

    def showMessageBox(self, title:str, message:str, icon: QMessageBox.Icon):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon)
        msg.exec()
        
    def textChanged(self):
        
        self.ui.input_isbnAdd.textChanged.connect(self.validateISBN)

        # self.ui.input_isbnAdd.textChanged.connect(self.checkInputFieldsEmpty)
        self.ui.input_titleAdd.textChanged.connect(self.checkInputFieldsEmpty)
        self.ui.input_authorAdd.textChanged.connect(self.checkInputFieldsEmpty)
        self.ui.input_compAdd.textChanged.connect(self.checkInputFieldsEmpty)
        self.ui.input_yearAdd.textChanged.connect(self.checkInputFieldsEmpty)
        self.ui.input_quantityAdd.valueChanged.connect(self.checkInputFieldsEmpty)
        self.ui.input_stageAdd.currentIndexChanged.connect(self.checkInputFieldsEmpty)

    
    def validateISBN(self, text: str):



        if len(text.strip()) == 13:
            self.ui.input_isbnAdd.setStyleSheet("""
                border: 2px solid green;
                color: green;
            """)
            self.ui.isbn.setStyleSheet("color: green;")
            self.showNotification("Click Enter to check the ISBN")
        elif len(text.strip()) == 0:
            self.showNotification("")
            self.ui.isbn.setStyleSheet("color: black;")
            self.ui.input_isbnAdd.setStyleSheet("border: 2px solid black;")
            self.ui.enter_btn.hide()
            return
        else:
            # self.refreshFields()
            self.ui.isbn.setStyleSheet("color: red;")
            self.ui.input_isbnAdd.setStyleSheet("""
                border: 2px solid red;
                color: red;
            """)
            self.showNotification("ISBN must be 13 digits")

        self.hideSubmitButtons(False)

    def enterButtonClicked(self):
        try:

            isbn = self.ui.input_isbnAdd.text().strip()
            

            if not isbn:
                self.showMessageBox("Error", "Please enter the ISBN", QMessageBox.Icon.Warning)
                return
            if len(isbn) != 13:
                self.showMessageBox("Error", "ISBN must be 13 digits", QMessageBox.Icon.Warning)
                return
            
            existing_book, error = self.db_session.getBookByISBN(isbn)

            self.showBookDetail(existing_book)

            if existing_book:
                self.showNotification("Book already exists in the system, your addition will be updated with new warehouse ID")

                self.setDisabledStyle(self.ui.input_isbnAdd)
                self.showBookDetail(existing_book)


            else:
                self.showNotification("Book does not exist in the system, your addition will be added as new entire book")

                self.setPlaceholderText(self.ui.input_titleAdd, "Enter the title")
                self.setPlaceholderText(self.ui.input_authorAdd, "Enter the author")
                self.setPlaceholderText(self.ui.input_compAdd, "Enter the publisher")
                self.setPlaceholderText(self.ui.input_yearAdd, "Enter the publication year")


                # self.ui.input_isbnAdd.mousePressEvent = self.ensureChangeISBN()
                
            
            self.hideSubmitButtons(all=True)
            # self.isbn_details_entered = True

        except Exception as e:
            self.showMessageBox("Error", f"Error: {str(e)}", QMessageBox.Icon.Critical)
            return
        
    def ensureChangeISBN(self):

        reply = QMessageBox.question(self, "Change ISBN", "Do you want to change the ISBN? You have to check ISBN again to make sure the book isn't exist in the system.", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.disableDetailFields(self.input_fields.values())
            self.hideSubmitButtons(all=False)
        else:
            return

 
    def showBookDetail(self, existing_book: BooksBookMarcData):
        try:
            if existing_book:
                self.ui.input_titleAdd.setText(existing_book.title)
                self.ui.input_authorAdd.setText(existing_book.author)
                self.ui.input_compAdd.setText(existing_book.public_comp)
                self.ui.input_yearAdd.setText(str(existing_book.public_year))
                self.disableDetailFields(self.detail_fields)

            self.showInputFields()

        except Exception as e:
            self.showMessageBox("Error", f"Error: {str(e)}", QMessageBox.Icon.Critical)
            return
            
    def showInputFields(self):
        self.ui.input_titleAdd.show()
        self.ui.input_authorAdd.show()
        self.ui.input_compAdd.show()
        self.ui.input_yearAdd.show()
        self.ui.input_quantityAdd.show()
        self.ui.input_stageAdd.show()

        self.ui.title.show()
        self.ui.author.show()
        self.ui.public_comp.show()
        self.ui.public_year.show()
        self.ui.quantity.show()
        self.ui.stage.show()

    def showSubmitButtons(self):
        self.ui.submit_btn.show()
        self.ui.cancel_btnAdd.show()
        self.ui.enter_btn.hide()
    
    def disableDetailFields(self, disabled_field):
        for field in disabled_field:
            if field != self.ui.input_isbnAdd:
                self.setDisabledStyle(field)
                
    def setDisabledStyle(self, field: QLineEdit):
        field.setReadOnly(True)
        field.setStyleSheet("""
            background-color: #f0f0f0;
            border: 2px solid grey;
            color: green;
        """)
            


    def setPlaceholderText(self, field: QLineEdit, text: str):
        field.setPlaceholderText(text)

    def submitButtonClicked(self):
        try:
            empty = self.showErrorEmptyFields()
            if empty == True:
                return
            
            reply = QMessageBox.question(self.ui, "Submit Book", "Do you want to submit the book?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                self.submitBook()
                self.refreshFields()
            else:
                return

        except Exception as e:
            print(e)
            self.showMessageBox("Error", f"Error: {str(e)}", QMessageBox.Icon.Critical)
            return
        
    def submitBook(self):
        admin_id = self.ui.admin_id.text()
        isbn = self.ui.input_isbnAdd.text().strip()
        existing_book, error = self.db_session.getBookByISBN(isbn)
        if existing_book:
            bookData = BooksBookData(
                isbn = isbn,
                quantity = self.ui.input_quantityAdd.value(),
                stage = self.ui.input_stageAdd.currentText()
            )
            result = self.db_session.addBook(admin_id,isbn, None, bookData)
        
        else:
            bookMarcData = BooksBookMarcData(
                isbn = isbn,
                title = self.ui.input_titleAdd.text().strip(),
                author = self.ui.input_authorAdd.text().strip(),
                public_comp = self.ui.input_compAdd.text().strip(),
                public_year = self.ui.input_yearAdd.text().strip()
            )
            bookData = BooksBookData(
                isbn = isbn,
                quantity = self.ui.input_quantityAdd.value(),
                stage = self.ui.input_stageAdd.currentText().strip()
            )
            result = self.db_session.addBook(admin_id,isbn,bookMarcData, bookData)
        
        if result[0]:
                self.showMessageBox("Success", "Book added successfully", QMessageBox.Icon.Information)
        else:
            self.showMessageBox("Error", f"Error: {result[1]}", QMessageBox.Icon.Critical)

    def refreshFields(self):
        for field in self.input_fields.values():
            if field != self.ui.input_stageAdd:
                field.clear()
                field.setStyleSheet("border: 2px solid black;")
        self.ui.messageAdd.clear()
        self.hideSubmitButtons(all=True)
        self.hideInputFields()
        self.ui.input_isbnAdd.setReadOnly(False)
        self.ui.input_stageAdd.setCurrentIndex(-1)


    def checkInputFieldsEmpty(self):
        all_empty = (
            not self.ui.input_titleAdd.text().strip() and
            not self.ui.input_authorAdd.text().strip() and
            not self.ui.input_compAdd.text().strip() and
            not self.ui.input_yearAdd.text().strip() and
            self.ui.input_quantityAdd.text() == 0 and
            self.ui.input_stageAdd.currentText() == -1
        )

        if not all_empty:
            self.showSubmitButtons()
        else:
            self.hideSubmitButtons(False)
            self.showNotification("You need to enter all the fields to submit the book")
            # Dang sai doan nay

    def showErrorEmptyFields(self):

        if not self.ui.input_titleAdd.text().strip():
            self.showMessageBox("Error", "Please enter the title", QMessageBox.Icon.Warning)
            return True
        elif not self.ui.input_authorAdd.text().strip():
            self.showMessageBox("Error", "Please enter the author", QMessageBox.Icon.Warning)
            return True
        elif not self.ui.input_compAdd.text().strip():
            self.showMessageBox("Error", "Please enter the publisher", QMessageBox.Icon.Warning)
            return True
        elif not self.ui.input_yearAdd.text().strip():
            self.showMessageBox("Error", "Please enter the publication year", QMessageBox.Icon.Warning)
            return True
        elif self.ui.input_quantityAdd.value() == 0:
            self.showMessageBox("Error", "Please enter the quantity", QMessageBox.Icon.Warning)
            return True
        elif self.ui.input_stageAdd.currentIndex()==-1:
            self.showMessageBox("Error", "Please select the stage", QMessageBox.Icon.Warning)
            return True

    def cancelButtonClicked(self):
        try:
            reply = QMessageBox.question(self.ui, "Cancel", "Are you sure you want to cancel?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                self.refreshFields()
            else:
                return
            
        except Exception as e:
            self.showMessageBox("Error", f"Error: {str(e)}", QMessageBox.Icon.Critical)
            return
    



    
    
