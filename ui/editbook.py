# ------IMPORTS------------------------------------------
from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget, QPushButton, QMessageBox, QComboBox, QLabel,QLineEdit,QSpinBox,QStackedWidget,QHeaderView,QDateEdit,QFrame
from PyQt6.QtCore import Qt,QDate, QRegularExpression
from PyQt6.QtGui import QFont, QColor, QIntValidator, QRegularExpressionValidator
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_session import DBSession
from lms_types import BooksBookMarcData, BooksBookData

# ------EDITBOOK_UI CLASS---------------------------------
class EditBook_UI:

    input_warehouse_idEdit  : QLineEdit
    input_titleEdit         : QLineEdit
    input_authorEdit        : QLineEdit
    input_isbnEdit          : QLineEdit
    input_compEdit          : QLineEdit
    input_yearEdit          : QLineEdit
    input_quantityEdit      : QSpinBox
    input_stageEdit         : QComboBox
    
    edit_btn                : QPushButton
    delete_btn              : QPushButton
    save_btn                : QPushButton
    cancel_btn              : QPushButton
    check_btn               : QPushButton

    detail_box              : QFrame

    message_edit            : QLabel

    def __init__(self, ui, db_session: DBSession):
        self.ui         = ui
        self.db_session = db_session

        self.connectSignals()
        self.initialize()


    def connectSignals(self):

        self.ui.cancel_btn.clicked.connect(self.cancelButtonClicked)
        self.ui.edit_btn.clicked.connect(self.editButtonClicked)
        self.ui.save_btn.clicked.connect(self.saveButtonClicked)
        self.ui.delete_btn.clicked.connect(self.deleteButtonClicked)
        self.ui.check_btn.pressed.connect(self.checkButtonClicked)
    
    def initialize(self):
        # self.hideButtons(all=True)
        self.ui.check_btn.hide()
        self.setupFields()
        
        self.initial_field_values = {}

    def setupFields(self):
            
        self.detail_fields = [
            self.ui.input_warehouse_idEdit,
            self.ui.input_titleEdit,
            self.ui.input_authorEdit,
            self.ui.input_isbnEdit,
            self.ui.input_compEdit,
            self.ui.input_yearEdit,
            self.ui.input_quantityEdit,
            self.ui.input_stageEdit
        ]

        self.input_fields = {
            "input_titleEdit": self.ui.input_titleEdit,
            "input_authorEdit": self.ui.input_authorEdit,
            "input_isbnEdit": self.ui.input_isbnEdit,
            "input_compEdit": self.ui.input_compEdit,
            "input_yearEdit": self.ui.input_yearEdit,
            "input_quantityEdit": self.ui.input_quantityEdit,
            "input_stageEdit": self.ui.input_stageEdit
        }

        self.ui.input_isbnEdit.setMaxLength(13)
        isbn_validator = QRegularExpressionValidator(QRegularExpression(r'^\d{1,13}$'), self.ui.input_isbnEdit)
        self.ui.input_isbnEdit.setValidator(isbn_validator)
        self.ui.input_titleEdit.setMaxLength(100)
        self.ui.input_authorEdit.setMaxLength(100)
        self.ui.input_compEdit.setMaxLength(100)
        self.ui.input_yearEdit.setValidator(QIntValidator(1000, 9999))
        self.ui.input_quantityEdit.setMaximum(999999)  

    def hideButtons(self, all: bool):
        self.ui.delete_btn.hide()
        self.ui.save_btn.hide()
        self.ui.cancel_btn.hide()
        if all:
            self.ui.edit_btn.hide()
        else:
            self.ui.edit_btn.show()

    def showButtons(self, all: bool):
        self.ui.delete_btn.show()
        self.ui.save_btn.show()
        self.ui.cancel_btn.show()
        if all:
            self.ui.edit_btn.show()
        else:
            self.ui.edit_btn.hide()
        

    def editButtonClicked(self):
        self.checkISBNChanged()


        self.showNotification("You are now in edit mode. You can now edit the fields.")

        selected_row = self.ui.search_table.currentRow()
        if selected_row == -1:
            return
        
        self.highlightSelectedRow(selected_row)

        self.showButtons(all=False)
        self.enableEditFields()
        self.disableSearchBar()
        self.getInitialFieldValues()

    def disableSearchBar(self):
        self.ui.input_findSearch.setDisabled(True)
        self.ui.input_filterSearch.setDisabled(True)
        self.ui.find_btn.setDisabled(True)

        self.ui.input_findSearch.setStyleSheet("""
            background-color: lightgrey;
            color: grey;
            border: 2px solid grey;
            padding: 5px 10px 5px 10px ;
            """)
        
        self.ui.input_filterSearch.setStyleSheet("""
            background-color: lightgrey;
            color: grey;
            border: 2px solid grey;
            padding: 5px 10px 5px 10px ;
            """)
        
        self.ui.find_btn.setStyleSheet("""
            background-color: lightgrey;
            color: grey;
            border: 2px solid grey;
            padding: 5px 10px 5px 10px ;
            """)
        
    def enableSearchBar(self):
        self.ui.input_findSearch.setDisabled(False)
        self.ui.input_filterSearch.setDisabled(False)
        self.ui.find_btn.setDisabled(False)

        self.ui.input_findSearch.setStyleSheet("""
            background-color: white;
            color: black;
            border: 2px solid black;
            padding: 5px 10px 5px 10px;
            """)
        
        self.ui.input_filterSearch.setStyleSheet("""
            background-color: white;
            color: black;
            border: 2px solid black;
            padding: 5px 10px 5px 10px;
            """)
        
        self.ui.find_btn.setStyleSheet("""
            background-color: white;
            color: black;
            border: 2px solid black;
            padding: 5px 10px 5px 10px;
            """)
        


    def highlightSelectedRow(self, selected_row):
        row_count = self.ui.search_table.rowCount()
        column_count = self.ui.search_table.columnCount()

        for row_idx in range(row_count):
            for col_idx in range(column_count):
                item = self.ui.search_table.item(row_idx, col_idx)
                if item:
                    item.setBackground(QColor("#D3D3D3"))

        for col_idx in range(column_count):
            item = self.ui.search_table.item(selected_row, col_idx)
            if item:
                item.setBackground(QColor("#FFFF00"))  

        self.ui.search_table.setDisabled(True)
    
        
    def cancelButtonClicked(self):
        try:
            current_field_values = self.getCurrentFieldValues()

            
            if not self.areChangesMade(current_field_values):
                self.showMessageBox("Message", "No changes were made.", QMessageBox.Icon.Information)
                
                self.uneditSelectedRow()
                self.disableEditFields(full=True)
                self.showNotification("")
                self.hideButtons(all=False)
                self.enableSearchBar()
                self.showNotification("")

                return

            if QMessageBox.question(self.ui, "Message", "Are you sure you want to cancel and discard changes?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
                self.reverseChanges()
                self.uneditSelectedRow()
                self.disableEditFields(full=True)
                self.showNotification("")
                self.hideButtons(all=False)
                self.enableSearchBar()
                self.ui.check_btn.hide()
                
            

                
        except Exception as e:
            print("Error cancelling changes:", e)
            self.showMessageBox("Error", str(e), QMessageBox.Icon.Critical)

    



    def getInitialFieldValues(self):
        self.initial_field_values = self.getCurrentFieldValues()

    def getCurrentFieldValues(self):
        current_field_values = {
            'input_titleEdit'           : self.ui.input_titleEdit.text(),
            'input_authorEdit'          : self.ui.input_authorEdit.text(),
            'input_isbnEdit'            : self.ui.input_isbnEdit.text(),
            'input_yearEdit'            : self.ui.input_yearEdit.text(),  # No need for str() conversion
            'input_compEdit'            : self.ui.input_compEdit.text(),
            'input_warehouse_idEdit'    : self.ui.input_warehouse_idEdit.text(),  # No need for str() conversion
            'input_quantityEdit'        : self.ui.input_quantityEdit.value(),
            'input_stageEdit'           : self.ui.input_stageEdit.currentText()
        }
        return current_field_values

    
    def areChangesMade(self, current_field_values):
        return self.initial_field_values != current_field_values


    def unhighlightSelectedRow(self):
        row_count = self.ui.search_table.rowCount()
        column_count = self.ui.search_table.columnCount()

        for row_idx in range(row_count):
            for col_idx in range(column_count):
                item = self.ui.search_table.item(row_idx, col_idx)
                if item:
                    item.setBackground(QColor("white"))

        self.ui.search_table.setDisabled(False)

    def reverseChanges(self):

        

        for field_name, field_widget in self.input_fields.items():
            if field_name in self.initial_field_values:
                initial_value = self.initial_field_values[field_name]
                
                if isinstance(field_widget, QLineEdit):
                    field_widget.setText(initial_value)
                    
                elif isinstance(field_widget, QSpinBox):
                    field_widget.setValue(int(initial_value))
                    
                elif isinstance(field_widget, QComboBox):
                    index = field_widget.findText(initial_value)
                    
                    if index != -1:
                        field_widget.setCurrentIndex(index)

    def uneditSelectedRow(self):
        
        self.ui.search_table.setDisabled(False)
        self.ui.input_findSearch.setDisabled(False)
        self.ui.input_filterSearch.setDisabled(False)
        self.ui.find_btn.setDisabled(False)

        self.ui.search_table.clearSelection()

        # Iterate through all rows to clear any highlighted rows
        for row_idx in range(self.ui.search_table.rowCount()):
            for col_idx in range(self.ui.search_table.columnCount()):
                
                item = self.ui.search_table.item(row_idx, col_idx)
                
                if item:
                    item.setBackground(QColor(Qt.GlobalColor.white))  # Set background color back to white

        self.hideButtons(False)

    def checkButtonClicked(self):
        try:
            self.checkISBNChanged()
            isbn = self.ui.input_isbnEdit.text().strip()
            if len(isbn) != 13:
                self.showMessageBox("Error", "ISBN must be 13 digits long.", QMessageBox.Icon.Critical)
                return

            bookMarcData, message = self.db_session.getBookByISBN(isbn)

            if bookMarcData is None:
                self.showNotification("No book found in system with this ISBN. Now you can continue edit with this ISBN.")
                self.enableEditFields()
                self.showButtons(all=False)
                self.ui.check_btn.hide()
                return
            elif bookMarcData.isbn == self.initial_field_values['input_isbnEdit']:
                self.showNotification("ISBN is the same as the original. You can now edit the fields.")
                self.enableEditFields()
                self.showButtons(all=False)
                self.ui.check_btn.hide()
                return
            else:
                result = QMessageBox.question(self.ui, "Conflict", "A book with this ISBN already exists in the system. \nClick YES to load the book details of this ISBN, or NO to continue with the edit without changing the ISBN.", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

                if result == QMessageBox.StandardButton.Yes:
                    self.loadBookDetails(bookMarcData)
                    self.showButtons(all=False)
                    self.ui.check_btn.hide()
                    self.showNotification("You can edit quantity and stage fields only. Or you can input a new ISBN.")
                    self.ui.message_edit.setStyleSheet("""
                        color: red;
                    """)
                    self.enableEditFields()
                    self.disableDetailsFields()
                    return
                else:
                    self.showNotification("You can now edit the fields.")
                    self.ui.input_isbnEdit.setText(self.initial_field_values['input_isbnEdit'])
                    self.enableEditFields()
                    self.showButtons(all=False)
                    self.ui.check_btn.hide()
                    return

        except Exception as e:
            print("Error checking ISBN:", e)
            self.showMessageBox("Error", str(e), QMessageBox.Icon.Critical)

    def disableDetailsFields(self):
        self.ui.input_titleEdit.setDisabled(True)
        self.ui.input_authorEdit.setDisabled(True)
        self.ui.input_compEdit.setDisabled(True)
        self.ui.input_yearEdit.setDisabled(True)
        # self.ui.input_isbnEdit.setDisabled(True)

        self.ui.input_titleEdit.setStyleSheet("""
            background-color: lightgrey;
            color: red;
            border: 2px solid red;
            padding: 5px 10px 5px 10px ;
        """)
        self.ui.input_authorEdit.setStyleSheet("""
            background-color: lightgrey;
            color: red;
            border: 2px solid red;
            padding: 5px 10px 5px 10px ;    
        """)
        self.ui.input_compEdit.setStyleSheet("""
            background-color: lightgrey;
            color: red;
            border: 2px solid red;
            padding: 5px 10px 5px 10px ;
        """)
        self.ui.input_yearEdit.setStyleSheet("""
            background-color: lightgrey;
            color: red;
            border: 2px solid red;
            padding: 5px 10px 5px 10px ;
        """)
        self.ui.input_isbnEdit.setStyleSheet("""
            border: 2px solid red;
            padding: 5px 10px 5px 10px ;
        """)
        labels = [self.ui.isbn_edit, self.ui.title_edit, self.ui.author_edit, self.ui.public_comp_edit, self.ui.public_year_edit]
        for label in labels:
            label.setStyleSheet("""
                color: red;
            """)

        
        

   
    def loadBookDetails(self, bookMarcData):
        self.ui.input_titleEdit.setText(bookMarcData.title)
        self.ui.input_authorEdit.setText(bookMarcData.author)
        self.ui.input_compEdit.setText(bookMarcData.public_comp)
        self.ui.input_yearEdit.setText(str(bookMarcData.public_year))
        
    def checkISBNChanged(self):
        # self.showNotification("You must check the ISBN first before continuing with the edit.")
        self.ui.input_isbnEdit.textChanged.connect(self.validateISBN)
        # self.disableEditFields()
        

    def validateISBN(self, text: str):
        if text == self.initial_field_values['input_isbnEdit']:
            self.ui.check_btn.hide()
            self.showNotification("You can now edit the fields.")
            self.enableEditFields()
            self.ui.input_isbnEdit.textChanged.disconnect(self.validateISBN)
        if len(text) == 13:
            self.ui.check_btn.show()
            self.showNotification("ISBN looks good. You can now check the ISBN.")
        else:
            self.ui.check_btn.hide()
            self.showNotification("ISBN must be 13 digits long.")

        self.disableEditFields(full=False)
        self.hideButtons(all=True)
        self.ui.check_btn.show()

        

    def saveButtonClicked(self):
        try:
            current_field_values = self.getCurrentFieldValues()

            if not self.areChangesMade(current_field_values):
                self.showMessageBox("Message", "You must make changes first before saving.", QMessageBox.Icon.Information)
                return

            if QMessageBox.question(self.ui, "Message", "Are you sure you want to save changes?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
                self.saveChanges(current_field_values)
                self.disableEditFields(full=True)
                self.showNotification("")
                self.hideButtons(all=False)
                self.enableSearchBar()

        except Exception as e:
            print("Error saving changes:", e)
            self.showMessageBox("Error", str(e), QMessageBox.Icon.Critical)

    def saveChanges(self, current_field_values):
        try:

            admin_id = self.ui.admin_id.text().strip()
            bookMarcData = self.getBookMarcData(current_field_values)
            bookData = self.getBookData(current_field_values)
            old_bookMarcData = self.getBookMarcData(self.initial_field_values)
            old_bookData = self.getBookData(self.initial_field_values)

            success, message = self.db_session.updateBook(admin_id, bookMarcData, bookData, old_bookMarcData, old_bookData)

            if not success:
                self.showMessageBox("Error", message, QMessageBox.Icon.Critical)
                return
                
            self.showMessageBox("Success", "Changes saved successfully.", QMessageBox.Icon.Information)
            
            self.unhighlightSelectedRow()
            self.disableEditFields(full=True)
            self.enableSearchBar()
            
            # from ui import ShowFile_UI
            # showfile = ShowFile_UI(self.ui, self.db_session)
            # showfile.updateBookMarcTable()
            
            # from ui import SearchBook_UI   
            # searchbook = SearchBook_UI(self.ui, self.db_session)
            # searchbook.updateSearchTable()

            from ui import SearchBook_UI
            searchbook = SearchBook_UI(self.ui, self.db_session)
            searchbook.findButtonClicked()

        except Exception as e:
            print("Error saving changes:", e)
            self.showMessageBox("Error", str(e), QMessageBox.Icon.Critical)

    

    def getBookMarcData(self, current_field_values):
        bookMarcData = BooksBookMarcData(
            title = current_field_values['input_titleEdit'],
            author = current_field_values['input_authorEdit'],
            isbn = current_field_values['input_isbnEdit'],
            public_comp= current_field_values['input_compEdit'],
            public_year= current_field_values['input_yearEdit'],
        )
        return bookMarcData
    def getBookData(self, current_field_values):
        bookData = BooksBookData(
            quantity = current_field_values['input_quantityEdit'],
            stage = current_field_values['input_stageEdit'],
            isbn= current_field_values['input_isbnEdit'],
            warehouse_id = current_field_values['input_warehouse_idEdit']
        )
        return bookData

    def deleteButtonClicked(self):
        
        if QMessageBox.question(self.ui, "Message", "Are you sure you want to delete this book with this warehouse ID? This action cannot be undone and the edit will be cancelled.",
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            self.deleteBook()
    
    def deleteBook(self):
        try:
            selected_row = self.ui.search_table.currentRow()
            if selected_row == -1:
                return

            admin_id = self.ui.admin_id.text().strip()
            bookMarcData = self.getBookMarcData(self.initial_field_values)
            bookData = self.getBookData(self.initial_field_values)

            success, message = self.db_session.deleteBook(admin_id, bookMarcData, bookData)

            if not success:
                self.showMessageBox("Error", message, QMessageBox.Icon.Critical)
                return

            self.showMessageBox("Success", "Book deleted successfully.", QMessageBox.Icon.Information)
            
            self.unhighlightSelectedRow()
            self.ui.detail_box.hide()
            self.enableSearchBar()
            
            self.ui.search_table.removeRow(selected_row)
            # from ui import ShowFile_UI
            # showfile = ShowFile_UI(self.ui, self.db_session)
            # showfile.updateBookMarcTable()
            # showfile.updateBookTable()

        except Exception as e:
            print("Error deleting book:", e)
            self.showMessageBox("Error", str(e), QMessageBox.Icon.Critical)


    def enableEditFields(self):
        for field in self.input_fields.values():
            field.setDisabled(False)
            field.setStyleSheet("""
                background-color: white;
                color: black;
                border: 2px solid black;
                                """)

    def disableEditFields(self,full: bool):
        for field in self.detail_fields:
            if full:
                field.setDisabled(True)
                field.setStyleSheet("""
                    background-color: lightgrey;
                    color: grey;
                    border: 2px solid grey;
                    padding: 5px 10px 5px 10px ;
                """)
            else:
                if field != self.ui.input_isbnEdit:
                    field.setDisabled(True)
                    field.setStyleSheet("""
                        background-color: lightgrey;
                        color: grey;
                        border: 2px solid grey;
                        padding: 5px 10px 5px 10px ;
                    """)
                else:
                    field.setDisabled(False)
                    field.setStyleSheet("""
                        background-color: white;
                        color: black;
                        border: 2px solid black;
                        padding: 5px 10px 5px 10px ;
                    """)
        labels = [self.ui.isbn_edit, self.ui.title_edit, self.ui.author_edit, self.ui.public_comp_edit, self.ui.public_year_edit]
        for label in labels:
            label.setStyleSheet("""
                color: black;
            """)

    def showNotification(self, message: str):
        self.ui.message_edit.setText(message)
        self.ui.message_edit.show()
        self.ui.message_edit.repaint()
        
    def showMessageBox(self, title: str, message: str, icon: QMessageBox.Icon):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec()