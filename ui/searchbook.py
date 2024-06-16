# ------IMPORTS------------------------------------------
from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget, QPushButton, QMessageBox, QComboBox, QLabel,QLineEdit,QSpinBox,QStackedWidget,QHeaderView,QDateEdit 
from PyQt6.QtCore import Qt,QDate, QRegularExpression
from PyQt6.QtGui import QFont, QColor, QIntValidator, QRegularExpressionValidator
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_session import DBSession
from lms_types import BooksBookMarcData, BooksBookData
# ---------------------------------------------------------

# ------SEARCHBOOK_UI CLASS---------------------------------
class SearchBook_UI:
    # List of objects in .ui file related to this module
    input_filterSearch      : QComboBox
    input_findSearch        : QLineEdit
    
    find_btn                : QPushButton
    search_table            : QTableWidget
    
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
    
    
    def __init__(self, ui, db_session: DBSession):
        
        # Connect to the database session
        self.ui         = ui
        self.db_session = db_session

        self.connectSignals()
        self.initialize()
        
        

    def initialize(self):
        self.hideButtons(True)
        self.setupFields()
        self.initial_field_values = {}

    def setupFields(self):
            
        # Set up the input fields
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

        self.ui.input_isbnEdit.setMaxLength(13)
        isbn_validator = QRegularExpressionValidator(QRegularExpression(r'^\d{1,13}$'), self.ui.input_isbnEdit)
        self.ui.input_isbnEdit.setValidator(isbn_validator)
        self.ui.input_titleEdit.setMaxLength(100)
        self.ui.input_authorEdit.setMaxLength(100)
        self.ui.input_compEdit.setMaxLength(100)
        self.ui.input_yearEdit.setValidator(QIntValidator(1000, 9999))
        self.ui.input_quantityEdit.setMaximum(999999)  

        self.input_fields = {
            "input_titleEdit": self.ui.input_titleEdit,
            "input_authorEdit": self.ui.input_authorEdit,
            "input_isbnEdit": self.ui.input_isbnEdit,
            "input_compEdit": self.ui.input_compEdit,
            "input_yearEdit": self.ui.input_yearEdit,
            "input_quantityEdit": self.ui.input_quantityEdit,
            "input_stageEdit": self.ui.input_stageEdit
        }
        
    def hideButtons(self, check):

        self.buttons_edit = [
            self.ui.edit_btn,
            self.ui.delete_btn,
            self.ui.save_btn,
            self.ui.cancel_btn
        ]

        if check == False:
            for button in self.buttons_edit:
                if button == self.ui.edit_btn:
                    button.show()
                else:
                    button.hide()
        else:
            for button in self.buttons_edit:
                button.hide()

    def connectSignals(self):
        self.ui.search_table.cellClicked.connect(self.displayBookDetails)
        self.ui.edit_btn.clicked.connect(self.editButtonClicked)
        self.ui.cancel_btn.clicked.connect(self.cancelButtonClicked)
        self.ui.save_btn.clicked.connect(self.saveButtonClicked)
        self.ui.delete_btn.clicked.connect(self.deleteButtonClicked)
        self.ui.find_btn.pressed.connect(self.searchBookInformation)
        
    def searchBookInformation(self, clear: bool = True):
        try:
            if clear:
                self.clearTableAndDetailFields()
            
            search_query = self.ui.input_findSearch.text().strip()
            
            if not search_query:

                self.showMessageBox("Search", "Please enter a search query.", QMessageBox.Icon.Warning)
                
                self.ui.input_filterSearch.setCurrentIndex(-1)
                self.hideButtons(True)

                return
            
            # Continue with normal search process
            
            filter_criteria = self.ui.input_filterSearch.currentText()
            column_name     = self.getColumnFromFilter(filter_criteria)

            search_results = list(self.db_session.searchBook(column_name, search_query))

            if search_results:
                self.populateTableWithResults(search_results, filter_criteria)
                
            else:
                self.showMessageBox("Search", "No results found.", QMessageBox.Icon.Warning)
                
        except Exception as e:
            print("Error searching book information:", e)
            self.showMessageBox("Error", str(e), QMessageBox.Icon.Critical)

    def populateTableWithResults(self, search_results, filter_criteria):
        # Display search results in the table
        self.ui.search_table.setRowCount(len(search_results))
        column_count = len(search_results[0]) if search_results else 0
        self.ui.search_table.setColumnCount(column_count)
        header_labels = self.getHeaderLabels(filter_criteria)
        self.setTableHeaders(header_labels)
        self.fillTableWithData(search_results)
        self.adjustColumnWidths(self.ui.search_table)

    def getHeaderLabels(self, filter_criteria: str) -> list[str]:
        if filter_criteria in ["Book ID", "Title", "ISBN", "Warehouse ID", ""]:
            return ['Book ID', 'Title', 'ISBN', 'Warehouse ID']
        else:
            return ['Book ID', 'Title', 'ISBN', 'Warehouse ID', filter_criteria]
        
    def setTableHeaders(self, header_labels: list[str]):
        for col_idx, header in enumerate(header_labels):
            item = QTableWidgetItem(header)
            font = item.font()
            font.setBold(True)
            item.setFont(font)
            self.ui.search_table.setHorizontalHeaderItem(col_idx, item)

    def fillTableWithData(self, search_results: list[tuple]):
        for row_idx, row_data in enumerate(search_results):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ui.search_table.setItem(row_idx, col_idx, item)

    def getColumnFromFilter(self, filter_criteria: str) -> str:
        column_mapping = {
            "Book ID"       : "book_id",
            "Warehouse ID"  : "warehouse_id",
            "Title"         : "title",
            "Author"        : "author",
            "Public Year"   : "public_year",
            "Public Company": "public_comp",
            "ISBN"          : "isbn",
            "Quantity"      : "quantity",
            "Stage"         : "stage",
            "All"           : None,
            ""              : None
        }

        return column_mapping.get(filter_criteria, None)

    def clearTableAndDetailFields(self):
        self.ui.search_table.clearContents()
        self.ui.search_table.setRowCount(0)
        self.clearDetailFields()

    def showMessageBox(self, title: str, message: str, icon: QMessageBox.Icon):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec()

    def displayBookDetails(self, row, column):
        try:
            book_id_item = self.ui.search_table.item(row, 0)  

            if book_id_item is None:
                return
            
            book_id = int(book_id_item.text())
            warehouse_id_item = self.ui.search_table.item(row, 3)  

            if warehouse_id_item is None:
                self.showMessageBox("Error", "Warehouse ID not found.", QMessageBox.Icon.Warning)
                return

            warehouse_id = int(warehouse_id_item.text())

            bookMarcData, bookData = self.db_session.getBookByIdAndWarehouseId(book_id, warehouse_id)
            
            if bookMarcData is None or bookData is None:
                self.showMessageBox("Error", "Book not found.", QMessageBox.Icon.Warning)
                return
            
            self.setDataFields(bookMarcData, bookData, warehouse_id)

            self.hideButtons(False)

        except Exception as e:
            self.showMessageBox("Error", str(e), QMessageBox.Icon.Critical)

    def setDataFields(self, bookMarcData: BooksBookMarcData, bookData: BooksBookData, warehouse_id: int):

        self.ui.input_titleEdit.setText(bookMarcData.title)
        self.ui.input_authorEdit.setText(bookMarcData.author)
        self.ui.input_isbnEdit.setText(bookMarcData.isbn)
        self.ui.input_yearEdit.setText(str(bookMarcData.public_year))
        self.ui.input_compEdit.setText(bookMarcData.public_comp)
        self.ui.input_warehouse_idEdit.setText(str(warehouse_id))
        self.ui.input_quantityEdit.setValue(bookData.quantity)
        self.ui.input_stageEdit.setCurrentText(bookData.stage)
    
        self.initial_field_values = {
            'input_titleEdit': bookMarcData.title,
            'input_authorEdit': bookMarcData.author,
            'input_isbnEdit': bookMarcData.isbn,
            'input_yearEdit': str(bookMarcData.public_year),
            'input_compEdit': bookMarcData.public_comp,
            'input_warehouse_idEdit': str(warehouse_id),
            'input_quantityEdit': bookData.quantity,
            'input_stageEdit': bookData.stage
        }

        self.old_bookMarcData = bookMarcData
        self.old_bookData = bookData

    def editButtonClicked(self):
        try:
            self.ui.search_table.clearSelection()
            
            selected_row = self.ui.search_table.currentRow()
            
            if selected_row == -1:
                return
            
            self.highlightSelectedRow(selected_row)
            self.enableDetailFields()
            self.showEditOptions()
            
        except Exception as e:
            print("Error editing book details:", e)
            
            self.showMessageBox("Error", str(e), QMessageBox.Icon.Critical)

    def highlightSelectedRow(self, selected_row):
        column_count = self.ui.search_table.columnCount()
            
        for col_idx in range(column_count):
            
            item = self.ui.search_table.item(selected_row, col_idx)
            
            if item:
                
                item.setBackground(QColor("#FFFF00"))  # Set background color to yellow


    def showEditOptions(self):
        self.ui.edit_btn.hide()
        self.ui.save_btn.show()
        self.ui.cancel_btn.show()
        self.ui.delete_btn.show()
        self.ui.search_table.setDisabled(True)
        self.ui.input_findSearch.setDisabled(True)
        self.ui.input_filterSearch.setDisabled(True)
        self.ui.find_btn.setDisabled(True)
            
    def cancelButtonClicked(self):
        try:
            print("Cancelling changes...")

            current_field_values = self.getCurrentFieldValues()
            
            if not self.areChangesMade(current_field_values):
                
                self.showMessageBox("Message", "No changes were made.", QMessageBox.Icon.Information)
                self.resetUI()
                self.disableDetailFields()

                return

            if QMessageBox.question(self.ui, 'Message', "Are you sure you want to cancel and discard changes?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
                
                self.resetUI()
                self.disableDetailFields()
                
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

                        

        except Exception as e:
            print("Error cancelling changes:", e)
            self.showMessageBox("Error", str(e), QMessageBox.Icon.Critical)

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
        return current_field_values != self.initial_field_values

    def disableDetailFields(self):
        for field_widget in self.input_fields.values():
            if isinstance(field_widget, QLineEdit) or isinstance(field_widget, QSpinBox):
                field_widget.setReadOnly(True)

            elif isinstance(field_widget, QComboBox):
                field_widget.setEnabled(False)

    def enableDetailFields(self):
        for field_widget in self.input_fields.values():
            if isinstance(field_widget, QLineEdit) or isinstance(field_widget, QSpinBox):
                field_widget.setReadOnly(False)

            elif isinstance(field_widget, QComboBox):
                field_widget.setEnabled(True)

    def resetUI(self):
        
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

    def saveButtonClicked(self):
        try:
            
            current_field_values = self.getCurrentFieldValues()
        
            if not self.areChangesMade(current_field_values):
                
                self.showMessageBox("Message", "You need to edit the fields to make changes.", QMessageBox.Icon.Information)

                return
            
            confirm_save = QMessageBox.question(self.ui, "Save Changes", "Are you sure you want to save the changes?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                                QMessageBox.StandardButton.No)

            if confirm_save == QMessageBox.StandardButton.Yes:
                
                admin_id = self.ui.admin_id.text()                  
                updated_bookMarcData = self.createUpdatedBookMarcData() 
                updated_bookData = self.createUpdatedBookData()

                success, message = self.db_session.updateBook(admin_id,updated_bookMarcData, updated_bookData, self.old_bookMarcData, self.old_bookData)

                if not success:
                    print("Error saving changes:", message)
                    self.showMessageBox("Error", message, QMessageBox.Icon.Critical)        
                    return

                self.disableDetailFields()
                self.showMessageBox("Save Changes", "Changes saved successfully.", QMessageBox.Icon.Information)
                
                self.resetUI()
                self.searchBookInformation(clear=False)
                

                from ui.showfile import ShowFile_UI
                showfile = ShowFile_UI(self.ui, self.db_session)
                showfile.updateBookMarcTable()
                showfile.updateBookTable()
                
                
            elif confirm_save == QMessageBox.StandardButton.No:                
                return

        except Exception as e:
            print("Error saving changes:", e)
            
            QMessageBox.critical(self.ui, "Error", str(e))

    def createUpdatedBookMarcData(self):
        return BooksBookMarcData(
                title       =self.ui.input_titleEdit.text(),
                author      =self.ui.input_authorEdit.text(),
                isbn        =self.ui.input_isbnEdit.text(),
                public_year =int(self.ui.input_yearEdit.text()),
                public_comp =self.ui.input_compEdit.text(),
                book_id     =self.old_bookMarcData.book_id
            )
    
    def createUpdatedBookData(self):
        return BooksBookData(
                warehouse_id=int(self.ui.input_warehouse_idEdit.text()),
                quantity    =self.ui.input_quantityEdit.value(),
                stage       =self.ui.input_stageEdit.currentText(),
                book_id     =self.old_bookData.book_id,
                isbn        =self.ui.input_isbnEdit.text()
            )
    
    def deleteButtonClicked(self):
        try:
            
            selected_row = self.ui.search_table.currentRow()
            if selected_row == -1:
                self.showMessageBox("Error", "Please select a book to delete.", QMessageBox.Icon.Warning)
                return

            book_id_item = self.ui.search_table.item(selected_row, 0)
            book_id     = int(book_id_item.text())
            if book_id is None:
                return
            
            admin_id    = self.ui.admin_id.text()

            confirmation = QMessageBox.question(self.ui, 'Message', "Are you sure you want to delete this book?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if confirmation == QMessageBox.StandardButton.Yes:
                warehouse_id = self.ui.input_warehouse_idEdit.text()

                success, message = self.db_session.deleteBook(warehouse_id,book_id, admin_id)
                if not success:
                    print("Error deleting book:", message)
                    self.showMessageBox("Error", message, QMessageBox.Icon.Critical)                    
                    return

                self.showMessageBox("Delete Book", "Book deleted successfully.", QMessageBox.Icon.Information)

                self.searchBookInformation()
                self.disableDetailFields()
                self.hideButtons(True)
                self.ui.input_findSearch.setDisabled(False)
                self.ui.input_filterSearch.setDisabled(False)
                self.ui.search_table.setDisabled(False)
                self.ui.find_btn.setDisabled(False)

                from ui.showfile import ShowFile_UI
                showfile = ShowFile_UI(self.ui, self.db_session)
                showfile.updateBookMarcTable()
                showfile.updateBookTable()
                
            elif confirmation == QMessageBox.StandardButton.No:
                return                

        except Exception as e:
            print("Error deleting book:", e)
            self.showMessageBox("Error", str(e), QMessageBox.Icon.Critical)
    
    def adjustColumnWidths(self, table):
        table.resizeColumnsToContents()
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
    def clearDetailFields(self):
        """Clear the book detail input fields."""
        for field in self.detail_fields:
            if isinstance(field, QLineEdit):
                field.clear()
            elif isinstance(field, QSpinBox):
                field.setValue(0)
            elif isinstance(field, QComboBox):
                field.setCurrentIndex(-1)