# ------IMPORTS------------------------------------------
from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget, QPushButton, QMessageBox, QComboBox, QLabel,QLineEdit,QSpinBox,QStackedWidget
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
    
    edit_stackedWidget      : QStackedWidget
    edit_btn                : QPushButton
    delete_btn              : QPushButton
    save_btn                : QPushButton
    cancel_btn              : QPushButton
    
    
    def __init__(self, ui, db_session: DBSession):
        self.ui         = ui
        self.db_session = db_session
        
        self.buttons_edit = [
            self.ui.edit_btn,
            self.ui.delete_btn,
            self.ui.save_btn,
            self.ui.cancel_btn
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
        
        self.initial_field_values = {}
        
        self.ui.search_table.cellClicked.connect(self.displayBookDetails)
        
        self.ui.edit_btn.clicked.connect(lambda: self.ui.edit_stackedWidget.setCurrentWidget(self.ui.save_page))
        self.ui.cancel_btn.clicked.connect(lambda: self.ui.edit_stackedWidget.setCurrentWidget(self.ui.delete_page))

        self.ui.edit_btn.clicked.connect(self.editButtonClicked)
        self.ui.cancel_btn.clicked.connect(self.cancelButtonClicked)
        
        
    def searchBookInformation(self):
        try:
            # Clear previous search results from the table
            self.ui.search_table.clearContents()
            self.ui.search_table.setRowCount(0)

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

            filter_criteria = self.ui.input_filterSearch.currentText()
            column_name     = column_mapping[filter_criteria]
            search_query    = self.ui.input_findSearch.text().strip()
    
            search_results = list(self.db_session.searchBook(column_name, search_query))
            
            if search_results:
                self.ui.search_table.setRowCount(len(search_results))
                column_count = len(search_results[0]) 
                self.ui.search_table.setColumnCount(column_count)
                
                # Set the header labels
                if filter_criteria in ["Book ID", "Title", "ISBN", "Warehouse ID", ""]:
                    header_labels = ['Book ID', 'Title', 'ISBN', 'Warehouse ID']
                else:
                    header_labels = ['Book ID', 'Title', 'ISBN', 'Warehouse ID', filter_criteria]
                    
                self.ui.search_table.setHorizontalHeaderLabels(header_labels)

                for row_idx, row_data in enumerate(search_results):
                    for col_idx, value in enumerate(row_data):
                        self.ui.search_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

                self.ui.search_table.resizeColumnsToContents()
            else:
                QMessageBox.warning(self.ui, "Search", "No results found.")
        except Exception as e:
            QMessageBox.critical(self.ui, "Error", str(e))

    def displayBookDetails(self, row, column):
        try:
            # Get the book ID from the selected row
            book_id_item = self.ui.search_table.item(row, 0)  
            # Assuming book_id is in the first column
            
            if book_id_item is None:
                return
            
            book_id = int(book_id_item.text())
            print(book_id)

            # Fetch the book details using the book ID
            bookMarcData, bookData = self.db_session.getBookById(book_id)
            
                        
            print(bookMarcData)
            print(bookData)
            if bookMarcData is None or bookData is None:
                QMessageBox.warning(self.ui, "Error", "Book details not found.")
                return
            


            # Update UI components with the book details

            self.ui.input_titleEdit.setText(bookMarcData.title)
            self.ui.input_authorEdit.setText(bookMarcData.author)
            self.ui.input_isbnEdit.setText(bookMarcData.isbn)
            self.ui.input_yearEdit.setText(str(bookMarcData.public_year))
            self.ui.input_compEdit.setText(bookMarcData.public_comp)
            self.ui.input_warehouse_idEdit.setText(str(bookData.warehouse_id))
            self.ui.input_quantityEdit.setValue(bookData.quantity)
            self.ui.input_stageEdit.setCurrentText(bookData.stage)
            
            # Store the initial values of the input fields
            self.initial_field_values = {
                'title': bookMarcData.title,
                'author': bookMarcData.author,
                'isbn': bookMarcData.isbn,
                'public_year': bookMarcData.public_year,
                'public_comp': bookMarcData.public_comp,
                'warehouse_id': bookData.warehouse_id,
                'quantity': bookData.quantity,
                'stage': bookData.stage
            }
            
            self.old_bookMarcData = bookMarcData
            self.old_bookData = bookData

        except Exception as e:
            QMessageBox.critical(self.ui, "Error", str(e))

    def editButtonClicked(self):
        # Enable or disable input fields based on edit button state
        edit_mode = self.ui.edit_btn.isChecked()
        for field_name, field_widget in self.input_fields.items():
            # Enable or disable QLineEdit fields based on edit mode
            if isinstance(field_widget, QLineEdit) or isinstance(field_widget, QSpinBox):
                field_widget.setReadOnly(edit_mode)
            # Enable or disable QSpinBox and QComboBox fields based on edit mode
            elif isinstance(field_widget, (QComboBox)):
                field_widget.setEnabled(not edit_mode)
                
        if edit_mode is False:
            self.storeInitialBookDetails()
            
    def cancelButtonClicked(self):
        # Restore the initial values of the input fields
        for field_name, field_widget in self.input_fields.items():
            if field_name in self.initial_field_values:
                initial_value = self.initial_field_values[field_name]
                if isinstance(field_widget, QLineEdit):
                    field_widget.setText(initial_value)
                elif isinstance(field_widget, QSpinBox):
                    field_widget.setValue(initial_value)
                elif isinstance(field_widget, QComboBox):
                    index = field_widget.findText(initial_value)
                    if index != -1:
                        field_widget.setCurrentIndex(index)
            
    def storeInitialBookDetails(self):
        # Store the initial values of the input fields
        for field_name, field_widget in self.input_fields.items():
            if isinstance(field_widget, QLineEdit):
                self.initial_field_values[field_name] = field_widget.text()
            elif isinstance(field_widget, QSpinBox):
                self.initial_field_values[field_name] = field_widget.value()
            elif isinstance(field_widget, QComboBox):
                self.initial_field_values[field_name] = field_widget.currentText()
                
    def saveButtonClicked(self):
        try:
            updated_bookMarcData = BooksBookMarcData(
                title=self.ui.input_titleEdit.text(),
                author=self.ui.input_authorEdit.text(),
                isbn=self.ui.input_isbnEdit.text(),
                public_year=int(self.ui.input_yearEdit.text()),
                public_comp=self.ui.input_compEdit.text(),
                book_id=self.old_bookMarcData.book_id
            )
            
            updated_bookData = BooksBookData(
                warehouse_id=int(self.ui.input_warehouse_idEdit.text()),
                quantity=self.ui.input_quantityEdit.value(),
                stage=self.ui.input_stageEdit.currentText(),
                book_id=self.old_bookData.book_id,
                isbn=self.input_isbnEdit.text()
            )
            
            success, message = self.db_session.updateBook(updated_bookMarcData, updated_bookData, self.old_bookMarcData, self.old_bookData)
            
            if not success:
                QMessageBox.warning(self.ui, "Error", message)
                return
            
            # Disable the input fields after saving the changes
            for field_widget in self.input_fields.values():
                if isinstance(field_widget, QLineEdit) or isinstance(field_widget, QSpinBox):
                    field_widget.setReadOnly(True)
                elif isinstance(field_widget, QComboBox):
                    field_widget.setEnabled(False)
                    
            # Reset buttons
            self.ui.edit_button.setEnabled(True)
            self.ui.save_button.setEnabled(False)
            self.ui.cancel_button.setEnabled(False)
            
            # Show a success message
            QMessageBox.information(self.ui, "Save", "Changes saved successfully.")
            
        except Exception as e:
            QMessageBox.critical(self.ui, "Error", str(e))
    