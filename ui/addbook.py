
# FULL NAME: Vũ Thị Minh Quý
# MSSV: 20227257
# CLASS: 150328
# PROJECT: 04 - Library Management System
# DATE: 20/06/2024 

# ----IMPORTS------------------------------------------
from PyQt6.QtWidgets import QPushButton, QMessageBox, QComboBox, QLineEdit, QSpinBox
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator, QIntValidator
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.db_session import DBSession
from db.lms_types import BooksBookMarcData, BooksBookData

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
    cancel_btnAdd      : QPushButton
    enter_btn          : QPushButton
    
    

    def __init__(self, ui, db_session: DBSession):
        self.ui = ui
        self.db_session = db_session

        self.connectSignals()
        self.setupFields()
        self.initialize()

    def initialize(self):
        
        self.isbn_checked = True

        self.hideSubmitButtons(True)
        self.hideInputFields()
        self.setEnabledStyle(self.ui.input_isbnAdd)

    def connectSignals(self):
        self.textChanged() 
        self.ui.enter_btn.clicked.connect(self.enterButtonClicked)
        self.ui.submit_btn.clicked.connect(self.submitButtonClicked)
        self.ui.cancel_btnAdd.clicked.connect(self.cancelButtonClicked)

    def textChanged(self):
        self.ui.input_isbnAdd.textChanged.connect(self.validateISBN)
        
        self.ui.input_titleAdd.textChanged.connect(self.checkInputFieldsEmpty)
        self.ui.input_authorAdd.textChanged.connect(self.checkInputFieldsEmpty)
        self.ui.input_compAdd.textChanged.connect(self.checkInputFieldsEmpty)
        self.ui.input_yearAdd.textChanged.connect(self.checkInputFieldsEmpty)
        self.ui.input_quantityAdd.valueChanged.connect(self.checkInputFieldsEmpty)
        self.ui.input_stageAdd.currentIndexChanged.connect(self.checkInputFieldsEmpty)
        
        self.ui.input_titleAdd.textChanged.connect(self.checkAllInputFieldsEmpty)
        self.ui.input_authorAdd.textChanged.connect(self.checkAllInputFieldsEmpty)
        self.ui.input_compAdd.textChanged.connect(self.checkAllInputFieldsEmpty)
        self.ui.input_yearAdd.textChanged.connect(self.checkAllInputFieldsEmpty)
        self.ui.input_quantityAdd.valueChanged.connect(self.checkAllInputFieldsEmpty)
        self.ui.input_stageAdd.currentIndexChanged.connect(self.checkAllInputFieldsEmpty)

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
            self.ui.isbn.setStyleSheet("color: red;")
            self.ui.input_isbnAdd.setStyleSheet("""
                border: 2px solid red;
                color: red;
            """)
            self.showNotification("ISBN must be 13 digits")

        self.hideSubmitButtons(False)

    def checkAllInputFieldsEmpty(self):
        all_empty = (
            self.ui.input_titleAdd.text().strip() == "" and
            self.ui.input_authorAdd.text().strip() == "" and
            self.ui.input_compAdd.text().strip() == "" and
            self.ui.input_yearAdd.text().strip() == "" and
            self.ui.input_quantityAdd.value() == 0 and
            self.ui.input_stageAdd.currentIndex() == -1
        )
        if all_empty:
            self.hideSubmitButtons(True)
            return True
        
    def setupFields(self):

        self.previous_isbn = ""
            
        self.detail_fields = [
            self.ui.input_isbnAdd,
            self.ui.input_titleAdd,
            self.ui.input_authorAdd,
            self.ui.input_compAdd,
            self.ui.input_yearAdd
        ]

        self.input_fields = {
            "input_titleAdd"    : self.ui.input_titleAdd,
            "input_authorAdd"   : self.ui.input_authorAdd,
            "input_isbnAdd"     : self.ui.input_isbnAdd,
            "input_compAdd"     : self.ui.input_compAdd,
            "input_yearAdd"     : self.ui.input_yearAdd,
            "input_quantityAdd" : self.ui.input_quantityAdd,
            "input_stageAdd"    : self.ui.input_stageAdd
        }

        self.ui.input_isbnAdd.setMaxLength(13)
        isbn_validator = QRegularExpressionValidator(QRegularExpression(r'^\d{1,13}$'), self.ui.input_isbnAdd)
        self.ui.input_isbnAdd.setValidator(isbn_validator)
        self.ui.input_titleAdd.setMaxLength(100)
        self.ui.input_authorAdd.setMaxLength(100)
        self.ui.input_compAdd.setMaxLength(100)
        self.ui.input_yearAdd.setValidator(QIntValidator(1000, 9999))
        self.ui.input_quantityAdd.setMaximum(999999)  



    def hideSubmitButtons(self, all: bool):
        self.ui.submit_btn.hide()
        self.ui.cancel_btnAdd.hide()
        if all:
            self.ui.enter_btn.hide()
        else:
            self.ui.enter_btn.show()

    def hideInputFields(self):
        
        for field in self.input_fields.values():
            if field != self.ui.input_isbnAdd:
                field.hide()

        labels = [
            self.ui.title,
            self.ui.author,
            self.ui.public_comp,
            self.ui.public_year,
            self.ui.quantity,
            self.ui.stage
        ]

        for label in labels:
            label.hide()

    def showInputFields(self):
        for field in self.input_fields.values():
            field.show()
        labels = [
            self.ui.title,
            self.ui.author,
            self.ui.public_comp,
            self.ui.public_year,
            self.ui.quantity,
            self.ui.stage
        ]

        for label in labels:
            label.show()

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

                self.setEnabledStyle(self.ui.input_titleAdd)
                self.setEnabledStyle(self.ui.input_authorAdd)
                self.setEnabledStyle(self.ui.input_compAdd)
                self.setEnabledStyle(self.ui.input_yearAdd)
                self.setEnabledStyle(self.ui.input_quantityAdd)
                self.setEnabledStyle(self.ui.input_stageAdd)
                
            
            self.hideSubmitButtons(all=True)
            self.isbn_checked = True
            self.previous_isbn = isbn
            self.ui.input_isbnAdd.editingFinished.connect(self.isbnEdited)
        

        except Exception as e:
            self.showMessageBox("Error", f"Error: {str(e)}", QMessageBox.Icon.Critical)
            return

    def isbnEdited(self):
        isbn_text = self.ui.input_isbnAdd.text().strip()
        
        # If the ISBN is not 13 digits, reset fields
        if len(isbn_text) != 13:
            for field in self.input_fields.values():
                if field != self.ui.input_isbnAdd:
                    self.setDisabledStyle(field)
            self.isbn_checked = False

        # If the ISBN is changed, prompt the user for confirmation
        if self.isbn_checked and isbn_text != self.previous_isbn:
            result = QMessageBox.question(
                self.ui, 
                "Change ISBN", 
                "You have changed the ISBN. We need to check the new ISBN. Do you want to continue? If the ISBN already exists, the information you have entered will be lost.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if result == QMessageBox.StandardButton.Yes:
                self.isbn_checked = False
                for field in self.input_fields.values():
                    if field != self.ui.input_isbnAdd:
                        self.setEnabledStyle(field)
                self.enterButtonClicked()
            else:
                self.ui.input_isbnAdd.setText(self.previous_isbn)

 
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
  
    def showSubmitButtons(self):
        self.ui.submit_btn.show()
        self.ui.cancel_btnAdd.show()
        self.ui.enter_btn.hide()
    
    def disableDetailFields(self, disabled_field):
        for field in disabled_field:
            if field != self.ui.input_isbnAdd:
                self.setDisabledStyle(field)
                
    def setDisabledStyle(self, field: QLineEdit):
        field.setDisabled(True)
        field.setStyleSheet("""
            background-color: #f0f0f0;
            border: 2px solid grey;
            color: green;
        """)
            
    def setEnabledStyle(self, field: QLineEdit):
        field.setDisabled(False)
        field.setStyleSheet("""
            background-color: white;
            border: 2px solid black;
            color: black;
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
                self.initialize()

            else:
                return

        except Exception as e:
            print(e)
            self.showMessageBox("Error", f"Error: {str(e)}", QMessageBox.Icon.Critical)
            return
        
    def submitBook(self):
        admin_id = self.ui.admin_id.text()
        isbn = self.ui.input_isbnAdd.text()
        existing_book, error = self.db_session.getBookByISBN(isbn)
        print(existing_book)
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
                self.refreshFields()
        else:
            self.showMessageBox("Error", f"Error: {result[1]}", QMessageBox.Icon.Critical)

    def refreshFields(self):
        self.ui.messageAdd.clear()
        self.ui.input_isbnAdd.setReadOnly(False)
        self.hideInputFields()
        for field in self.input_fields.values():
            if field != self.ui.input_stageAdd:
                if field != self.ui.input_quantityAdd:
                    field.clear()
                    field.setStyleSheet("border: 2px solid black;")
                else:
                    field.setValue(0)
            else:
                field.setCurrentIndex(-1)
        self.hideSubmitButtons(all=True)


    def checkInputFieldsEmpty(self):
        empty = (
            not self.ui.input_titleAdd.text().strip() and
            not self.ui.input_authorAdd.text().strip() and
            not self.ui.input_compAdd.text().strip() and
            not self.ui.input_yearAdd.text().strip() and
            self.ui.input_quantityAdd.text() == 0 and
            self.ui.input_stageAdd.currentIndex() == -1
        )

        if not empty:
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
                self.initialize()
            else:
                return
            
        except Exception as e:
            self.showMessageBox("Error", f"Error: {str(e)}", QMessageBox.Icon.Critical)
            return

    def showNotification(self, message: str):
        self.ui.messageAdd.setText(message)
        self.ui.messageAdd.show()

    def showMessageBox(self, title:str, message:str, icon: QMessageBox.Icon):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon)
        msg.exec()

    
    
